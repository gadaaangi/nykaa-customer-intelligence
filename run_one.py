import sqlite3
import pandas as pd

conn = sqlite3.connect('nykaa.db')

with open('queries.sql', 'r') as f:
    sql_script = f.read()

queries = [q.strip() for q in sql_script.split(';') if q.strip()]


# 👇 Paste whichever query you want to test here
query = """

SELECT 
    c.campaign_name,
    c.budget,
    COUNT(ae.order_id) AS attributed_purchases,
    ROUND(SUM(o.total_amount), 2) AS attributed_revenue,
    ROUND(SUM(o.total_amount) / c.budget, 2) AS roas
FROM campaigns c
LEFT JOIN ad_events ae ON c.campaign_id = ae.campaign_id AND ae.event_type = 'purchase'
LEFT JOIN orders o ON ae.order_id = o.order_id
GROUP BY c.campaign_id, c.campaign_name, c.budget
ORDER BY roas DESC;
"""

df = pd.read_sql_query(query, conn)
print(df)

conn.close()