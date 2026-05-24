import os
import duckdb
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_rag_context():
    """Load business context for RAG"""
    with open("rag/context.md", "r") as f:
        return f.read()

def load_metrics(weeks=8):
    """Load recent weekly metrics from DuckDB"""
    con = duckdb.connect("ecom.db")
    
    metrics = con.execute(f"""
        SELECT 
            w.week_label,
            w.total_orders,
            w.total_revenue,
            w.avg_order_value,
            w.return_rate_pct,
            w.cancellation_rate_pct,
            w.revenue_wow_growth_pct,
            t.top_category,
            t.top_category_revenue
        FROM weekly_metrics w
        LEFT JOIN weekly_top_category t 
            ON w.week_label = t.week_label
        ORDER BY w.week_start DESC
        LIMIT {weeks}
    """).df()
    
    con.close()
    return metrics.iloc[::-1].reset_index(drop=True)  # chronological order

def detect_anomalies(metrics_df):
    """Rule-based anomaly detection"""
    anomalies = []
    
    for _, row in metrics_df.iterrows():
        week_anomalies = []
        
        if pd.notna(row['revenue_wow_growth_pct']):
            if row['revenue_wow_growth_pct'] < -15:
                week_anomalies.append(
                    f"Revenue dropped {abs(row['revenue_wow_growth_pct'])}% vs last week"
                )
            if row['revenue_wow_growth_pct'] > 25:
                week_anomalies.append(
                    f"Revenue spiked {row['revenue_wow_growth_pct']}% vs last week"
                )
        
        if row['return_rate_pct'] > 15:
            week_anomalies.append(
                f"Return rate {row['return_rate_pct']}% — above 15% threshold"
            )
        
        if row['cancellation_rate_pct'] > 10:
            week_anomalies.append(
                f"Cancellation rate {row['cancellation_rate_pct']}% — above 10% threshold"
            )
        
        if row['avg_order_value'] < 1500:
            week_anomalies.append(
                f"AOV ₹{row['avg_order_value']} — below ₹1,500 minimum"
            )
        
        if week_anomalies:
            anomalies.append({
                'week': row['week_label'],
                'flags': week_anomalies
            })
    
    return anomalies

def generate_weekly_insight(week_data, anomalies, rag_context):
    """Use Groq LLM to generate insight for a specific week"""
    
    anomaly_text = ""
    week_anomalies = [a for a in anomalies if a['week'] == week_data['week_label']]
    if week_anomalies:
        anomaly_text = "ANOMALIES DETECTED:\n" + "\n".join(
            f"- {flag}" for flag in week_anomalies[0]['flags']
        )
    else:
        anomaly_text = "No anomalies detected this week."
    
    prompt = f"""You are a senior data analyst at EcomCo, an Indian e-commerce company.
    
BUSINESS CONTEXT:
{rag_context}

WEEK: {week_data['week_label']}
METRICS:
- Revenue: ₹{week_data['total_revenue']:,.0f}
- Orders: {week_data['total_orders']}
- Avg Order Value: ₹{week_data['avg_order_value']:,.0f}
- Return Rate: {week_data['return_rate_pct']}%
- Cancellation Rate: {week_data['cancellation_rate_pct']}%
- WoW Revenue Growth: {week_data['revenue_wow_growth_pct']}%
- Top Category: {week_data['top_category']} (₹{week_data['top_category_revenue']:,.0f})

{anomaly_text}

Write a 3-sentence analyst insight for this week:
1. What happened (key metrics summary)
2. What is concerning or positive (anomaly explanation if any)
3. What action the business should take

Be specific, use the numbers, sound like a real analyst. No bullet points — write in prose."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    
    return response.choices[0].message.content.strip()

def generate_full_report(weeks=8):
    """Generate complete weekly report with LLM insights"""
    print(" Loading metrics...")
    metrics = load_metrics(weeks)
    
    print(" Loading business context...")
    rag_context = load_rag_context()
    
    print(" Detecting anomalies...")
    anomalies = detect_anomalies(metrics)
    
    print(f"\n⚠️  Anomalies found in {len(anomalies)} weeks:")
    for a in anomalies:
        print(f"  {a['week']}: {', '.join(a['flags'])}")
    
    print("\n Generating LLM insights...")
    report = []
    
    for i, row in metrics.iterrows():
        print(f"  Analyzing {row['week_label']}...")
        insight = generate_weekly_insight(row, anomalies, rag_context)
        
        report.append({
            'week': row['week_label'],
            'revenue': row['total_revenue'],
            'orders': row['total_orders'],
            'return_rate': row['return_rate_pct'],
            'wow_growth': row['revenue_wow_growth_pct'],
            'top_category': row['top_category'],
            'anomaly_flags': len([a for a in anomalies if a['week'] == row['week_label']]) > 0,
            'llm_insight': insight
        })
    
    report_df = pd.DataFrame(report)
    
    # Save report
    os.makedirs('outputs', exist_ok=True)
    report_df.to_csv('outputs/weekly_report.csv', index=False)
    print("\n Report saved to outputs/weekly_report.csv")
    
    return report_df

if __name__ == "__main__":
    report = generate_full_report(weeks=8)
    
    print("\n" + "="*60)
    print("WEEKLY ANALYST REPORT — Last 8 Weeks")
    print("="*60)
    
    for _, row in report.iterrows():
        flag = "⚠️" if row['anomaly_flags'] else "✅"
        print(f"\n{flag} {row['week']}")
        print(f"   Revenue: ₹{row['revenue']:,.0f} | Orders: {row['orders']} | Returns: {row['return_rate']}%")
        print(f"   {row['llm_insight']}")