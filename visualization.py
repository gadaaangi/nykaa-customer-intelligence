import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('nykaa.db')
sns.set_style("whitegrid")

# ============================================
# VISUAL 1: Repeat vs One-Time Customers (Pie)
# ============================================
query1 = """
SELECT customer_id, COUNT(order_id) AS order_count
FROM orders
GROUP BY customer_id
"""
df1 = pd.read_sql_query(query1, conn)
df1['type'] = df1['order_count'].apply(lambda x: 'Repeat Customer' if x > 1 else 'One-Time Customer')

plt.figure(figsize=(6,6))
df1['type'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#E91E63', '#F8BBD0'], startangle=90)
plt.title('Repeat vs One-Time Customers', fontsize=14, fontweight='bold')
plt.ylabel('')
plt.tight_layout()
plt.savefig('1_repeat_vs_onetime.png', dpi=150)
plt.close()
print("✅ Saved: 1_repeat_vs_onetime.png")

# ============================================
# VISUAL 2: RFM Segment Distribution (Bar)
# ============================================
rfm_query = """
WITH rfm_raw AS (
    SELECT 
        c.customer_id,
        JULIANDAY('2025-12-31') - JULIANDAY(MAX(o.order_date)) AS recency_days,
        COUNT(o.order_id) AS frequency,
        SUM(o.total_amount) AS monetary
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id
),
rfm_scored AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,
        NTILE(4) OVER (ORDER BY frequency ASC) AS f_score,
        NTILE(4) OVER (ORDER BY monetary ASC) AS m_score
    FROM rfm_raw
)
SELECT *,
    CASE 
        WHEN r_score >= 3 AND f_score >= 3 AND m_score >= 3 THEN 'Champions'
        WHEN r_score >= 3 AND f_score <= 2 THEN 'New/Promising'
        WHEN r_score <= 2 AND f_score >= 3 AND m_score >= 3 THEN 'At Risk (High Value)'
        WHEN r_score <= 2 AND f_score <= 2 THEN 'Lost'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM rfm_scored
"""
df_rfm = pd.read_sql_query(rfm_query, conn)

plt.figure(figsize=(9,5))
segment_counts = df_rfm['customer_segment'].value_counts()
sns.barplot(x=segment_counts.values, y=segment_counts.index, palette='RdPu_r')
plt.title('Customer Segments (RFM Analysis)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Customers')
plt.ylabel('')
plt.tight_layout()
plt.savefig('2_rfm_segments.png', dpi=150)
plt.close()
print("✅ Saved: 2_rfm_segments.png")

# Save RFM table too — you'll want this for your writeup
df_rfm.to_csv('rfm_results.csv', index=False)
print("✅ Saved: rfm_results.csv")

# ============================================
# VISUAL 3: Cohort Retention Heatmap
# ============================================
cohort_query = """
WITH first_purchase AS (
    SELECT customer_id, MIN(STRFTIME('%Y-%m', order_date)) AS cohort_month
    FROM orders GROUP BY customer_id
),
order_months AS (
    SELECT o.customer_id, f.cohort_month, STRFTIME('%Y-%m', o.order_date) AS order_month
    FROM orders o JOIN first_purchase f ON o.customer_id = f.customer_id
),
cohort_index AS (
    SELECT customer_id, cohort_month, order_month,
        (CAST(SUBSTR(order_month,1,4) AS INTEGER) - CAST(SUBSTR(cohort_month,1,4) AS INTEGER)) * 12 +
        (CAST(SUBSTR(order_month,6,2) AS INTEGER) - CAST(SUBSTR(cohort_month,6,2) AS INTEGER)) AS month_number
    FROM order_months
)
SELECT cohort_month, month_number, COUNT(DISTINCT customer_id) AS active_customers
FROM cohort_index
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number
"""
df_cohort = pd.read_sql_query(cohort_query, conn)

cohort_pivot = df_cohort.pivot(index='cohort_month', columns='month_number', values='active_customers')
cohort_size = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_size, axis=0) * 100

plt.figure(figsize=(14,8))
sns.heatmap(retention, annot=True, fmt='.0f', cmap='RdPu', cbar_kws={'label': 'Retention %'})
plt.title('Customer Cohort Retention Heatmap (%)', fontsize=14, fontweight='bold')
plt.xlabel('Months Since First Purchase')
plt.ylabel('Signup Cohort (Month)')
plt.tight_layout()
plt.savefig('3_cohort_retention.png', dpi=150)
plt.close()
print("✅ Saved: 3_cohort_retention.png")

# ============================================
# VISUAL 4: Category Revenue Contribution
# ============================================
cat_query = """
SELECT p.category, SUM(oi.quantity * oi.price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC
"""
df_cat = pd.read_sql_query(cat_query, conn)

plt.figure(figsize=(8,5))
sns.barplot(data=df_cat, x='total_revenue', y='category', palette='RdPu_r')
plt.title('Revenue by Product Category', fontsize=14, fontweight='bold')
plt.xlabel('Total Revenue (₹)')
plt.ylabel('')
plt.tight_layout()
plt.savefig('4_category_revenue.png', dpi=150)
plt.close()
print("✅ Saved: 4_category_revenue.png")

conn.close()
print("\n🎉 All visuals generated!")