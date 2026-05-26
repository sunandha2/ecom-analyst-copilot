import duckdb
import pandas as pd
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

con = duckdb.connect('ecom.db')

# Export metrics to CSV for deployment
metrics = con.execute("""
    SELECT w.*, t.top_category, t.top_category_revenue
    FROM weekly_metrics w
    LEFT JOIN weekly_top_category t ON w.week_label = t.week_label
    ORDER BY w.week_start
""").df()

metrics.to_csv('outputs/weekly_metrics.csv', index=False)
print(f"✅ Exported {len(metrics)} weeks of metrics")
con.close()