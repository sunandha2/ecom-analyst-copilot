
  
    
    

    create  table
      "ecom"."main"."weekly_top_category__dbt_tmp"
  
    as (
      WITH orders AS (
    SELECT * FROM "ecom"."main"."stg_orders"
),

category_weekly AS (
    SELECT
        week_label,
        week_start,
        category,
        SUM(revenue)    AS category_revenue,
        COUNT(order_id) AS category_orders
    FROM orders
    GROUP BY week_label, week_start, category
),

ranked AS (
    SELECT
        week_label,
        week_start,
        category,
        category_revenue,
        category_orders,
        ROW_NUMBER() OVER (
            PARTITION BY week_label
            ORDER BY category_revenue DESC
        ) AS rank
    FROM category_weekly
)

SELECT
    week_label,
    week_start,
    category        AS top_category,
    category_revenue AS top_category_revenue,
    category_orders  AS top_category_orders
FROM ranked
WHERE rank = 1
ORDER BY week_start
    );
  
  