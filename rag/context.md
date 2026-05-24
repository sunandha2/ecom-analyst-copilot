# EcomCo Business Context

## Company Overview
EcomCo is an Indian e-commerce company selling across 5 categories: 
Electronics, Fashion, Home & Kitchen, Beauty, and Sports.
Operating in 7 cities: Hyderabad, Bangalore, Mumbai, Delhi, 
Chennai, Pune, Kolkata.

## Key Metrics Definitions

**total_revenue**: Total INR revenue from all delivered and shipped orders 
that week. Excludes cancelled orders.

**total_orders**: Count of all orders placed that week including all statuses.

**avg_order_value (AOV)**: Average revenue per order. Healthy range: ₹1,800-₹2,500.
Below ₹1,500 signals customers buying cheaper items or fewer quantities.

**return_rate_pct**: Percentage of orders returned. Industry benchmark is 10-12%.
Above 15% is a red flag requiring immediate investigation.
Electronics returns are typically higher (15-18%) due to defects.
Fashion returns are typically lower (8-10%) due to size issues being predictable.

**cancellation_rate_pct**: Percentage of orders cancelled before delivery.
Healthy range: 5-8%. Above 10% signals pricing or delivery issues.

**revenue_wow_growth_pct**: Week-over-week revenue growth percentage.
Healthy growth: 5-15% per week. Above 20% may indicate a sale event.
Below -10% requires investigation.

## Business Calendar
- Festival season: October-November (Diwali, Dussehra) — expect 30-50% revenue spikes
- Summer slowdown: May-June — expect 10-15% revenue dip
- Weekend effect: Saturday-Sunday orders are 15-20% higher than weekdays

## Anomaly Thresholds
Flag these as anomalies requiring investigation:
- Revenue drops more than 15% week over week
- Return rate above 15%
- Cancellation rate above 10%
- AOV drops below ₹1,500
- Revenue grows more than 25% without a known sale event

## Recommended Actions by Anomaly Type
- High returns in Electronics: Review supplier quality, check defect reports
- High cancellations: Check delivery partner SLAs, review pricing vs competitors
- Revenue drop: Check inventory levels, marketing spend, competitor promotions
- AOV drop: Review product mix, check if premium products are out of stock