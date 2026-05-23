WITH source AS (
    SELECT * FROM raw_orders
),

cleaned AS (
    SELECT
        order_id,
        customer_id,
        CAST(order_date AS DATE)                     AS order_date,
        DATE_TRUNC('week', CAST(order_date AS DATE)) AS week_start,
        STRFTIME(CAST(order_date AS DATE), '%Y-W%W') AS week_label,
        product_name,
        category,
        quantity,
        unit_price,
        revenue,
        city,
        is_returned,
        COALESCE(return_reason, 'No Return')         AS return_reason,
        status,
        CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END AS is_cancelled
    FROM source
    WHERE order_id IS NOT NULL
)

SELECT * FROM cleaned