import sqlite3
import pandas as pd

conn = sqlite3.connect('nykaa.db')

with open('queries.sql', 'r') as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(';') if q.strip()]


# 👇 Paste whichever query you want to test here
query = """


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
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()