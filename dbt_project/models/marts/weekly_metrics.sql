WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

weekly AS (
    SELECT
        week_label,
        week_start,
        COUNT(order_id)                                     AS total_orders,
        SUM(revenue)                                        AS total_revenue,
        ROUND(AVG(revenue), 2)                              AS avg_order_value,
        SUM(CASE WHEN is_returned THEN 1 ELSE 0 END)       AS total_returns,
        ROUND(
            SUM(CASE WHEN is_returned THEN 1 ELSE 0 END) * 100.0
            / COUNT(order_id), 2
        )                                                   AS return_rate_pct,
        SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END)  AS total_cancellations,
        ROUND(
            SUM(CASE WHEN is_cancelled = 1 THEN 1 ELSE 0 END) * 100.0
            / COUNT(order_id), 2
        )                                                   AS cancellation_rate_pct
    FROM orders
    GROUP BY week_label, week_start
),

with_growth AS (
    SELECT
        week_label,
        week_start,
        total_orders,
        total_revenue,
        avg_order_value,
        total_returns,
        return_rate_pct,
        total_cancellations,
        cancellation_rate_pct,
        LAG(total_revenue) OVER (ORDER BY week_start)      AS prev_week_revenue,
        ROUND(
            (total_revenue - LAG(total_revenue) OVER (ORDER BY week_start))
            * 100.0
            / NULLIF(LAG(total_revenue) OVER (ORDER BY week_start), 0),
        2)                                                  AS revenue_wow_growth_pct
    FROM weekly
)

SELECT * FROM with_growth
ORDER BY week_start