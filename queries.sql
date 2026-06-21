SELECT 
    COUNT(DISTINCT customer_id) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(DISTINCT customer_id), 2) AS repeat_purchase_rate_pct
FROM (
    SELECT customer_id, COUNT(order_id) AS order_count
    FROM orders
    GROUP BY customer_id
);


SELECT 
    c.customer_id,
    c.name,
    COUNT(o.order_id) AS orders_last_year,
    MAX(o.order_date) AS last_order_date,
    JULIANDAY('2025-12-31') - JULIANDAY(MAX(o.order_date)) AS days_since_last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_date >= DATE('2025-12-31', '-365 days')
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) >= 2
   AND MAX(o.order_date) < DATE('2025-12-31', '-90 days')
ORDER BY days_since_last_order DESC;



SELECT 
    product_id,
    STRFTIME('%Y-%m', review_date) AS review_month,
    ROUND(AVG(rating), 2) AS avg_rating,
    COUNT(*) AS num_reviews
FROM reviews
GROUP BY product_id, STRFTIME('%Y-%m', review_date)
ORDER BY product_id, review_month;




SELECT 
    c.customer_id,
    c.name,
    JULIANDAY('2025-12-31') - JULIANDAY(MAX(o.order_date)) AS recency_days,
    COUNT(o.order_id) AS frequency,
    SUM(o.total_amount) AS monetary
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;

WITH rfm_raw AS (
    SELECT 
        c.customer_id,
        c.name,
        JULIANDAY('2025-12-31') - JULIANDAY(MAX(o.order_date)) AS recency_days,
        COUNT(o.order_id) AS frequency,
        SUM(o.total_amount) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.name
),
rfm_scored AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- lower recency_days = better = higher score
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_raw
)
SELECT 
    customer_id, name, recency_days, frequency, monetary,
    r_score, f_score, m_score,
    (r_score + f_score + m_score) AS rfm_total,
    CASE 
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'New/Promising'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk (High Value)'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM rfm_scored
ORDER BY rfm_total DESC;




SELECT 
    p.category,
    SUM(oi.quantity * oi.price) AS total_revenue,
    ROUND(100.0 * SUM(oi.quantity * oi.price) / (SELECT SUM(quantity * price) FROM order_items), 2) AS pct_of_total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;



WITH first_purchase AS (
    SELECT customer_id, MIN(STRFTIME('%Y-%m', order_date)) AS cohort_month
    FROM orders
    GROUP BY customer_id
),
order_months AS (
    SELECT 
        o.customer_id,
        f.cohort_month,
        STRFTIME('%Y-%m', o.order_date) AS order_month
    FROM orders o
    JOIN first_purchase f ON o.customer_id = f.customer_id
),
cohort_index AS (
    SELECT 
        customer_id,
        cohort_month,
        order_month,
        (CAST(STRFTIME('%Y', order_month) AS INTEGER) - CAST(STRFTIME('%Y', cohort_month) AS INTEGER)) * 12 +
        (CAST(STRFTIME('%m', order_month) AS INTEGER) - CAST(STRFTIME('%m', cohort_month) AS INTEGER)) AS month_number
    FROM order_months
)
SELECT 
    cohort_month,
    month_number,
    COUNT(DISTINCT customer_id) AS active_customers
FROM cohort_index
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;