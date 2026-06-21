import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('nykaa.db')

# ---------- PULL PURCHASE DATA ----------
query = """
SELECT 
    o.customer_id,
    oi.product_id,
    SUM(oi.quantity) AS total_quantity
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.customer_id, oi.product_id
"""
df = pd.read_sql_query(query, conn)
print(f"Total customer-product purchase pairs: {len(df)}")

# ---------- BUILD THE CUSTOMER x PRODUCT MATRIX ----------
# Rows = customers, Columns = products, Values = quantity purchased (0 if never bought)
matrix = df.pivot_table(
    index='customer_id', 
    columns='product_id', 
    values='total_quantity', 
    fill_value=0
)

print(f"Matrix shape: {matrix.shape[0]} customers x {matrix.shape[1]} products")

# ---------- COMPUTE PRODUCT-TO-PRODUCT SIMILARITY ----------
# Transpose so each ROW is a product (with its column = customer purchase pattern)
# Cosine similarity tells us: how similar are two products based on WHO buys them
product_matrix = matrix.T  # now rows=products, columns=customers
similarity_matrix = cosine_similarity(product_matrix)

similarity_df = pd.DataFrame(
    similarity_matrix, 
    index=product_matrix.index, 
    columns=product_matrix.index
)

print(f"Similarity matrix shape: {similarity_df.shape}")

# Save for reuse (so we don't recompute every time)
similarity_df.to_pickle('product_similarity.pkl')
print("✅ Saved: product_similarity.pkl")

conn.close()

# ... (existing code: build matrix, compute similarity, save pickle, conn.close()) ...

# ===== NEW SECTION BELOW =====
import sqlite3
import pandas as pd

conn = sqlite3.connect('nykaa.db')
similarity_df = pd.read_pickle('product_similarity.pkl')

products_df = pd.read_sql_query("SELECT product_id, product_name, category, brand, price FROM products", conn)
products_df = products_df.set_index('product_id')

def recommend_similar_products(product_id, top_n=5):
    if product_id not in similarity_df.index:
        return f"Product ID {product_id} not found."
    scores = similarity_df[product_id].sort_values(ascending=False)
    scores = scores.drop(product_id)
    top_matches = scores.head(top_n)
    result = products_df.loc[top_matches.index].copy()
    result['similarity_score'] = top_matches.values.round(3)
    return result[['product_name', 'category', 'brand', 'price', 'similarity_score']]

sample_product_id = products_df.index[0]
sample_product_name = products_df.loc[sample_product_id, 'product_name']

print(f"\nIf a customer bought: '{sample_product_name}' (ID: {sample_product_id})")
print(f"\nTop 5 'Customers who bought this also bought:'\n")
print(recommend_similar_products(sample_product_id, top_n=5))

conn.close()


# ---------- TEST A FEW MORE PRODUCTS ----------
test_ids = [products_df.index[10], products_df.index[30], products_df.index[50]]

for pid in test_ids:
    pname = products_df.loc[pid, 'product_name']
    print(f"\n{'='*50}")
    print(f"If a customer bought: '{pname}' (ID: {pid})")
    print('='*50)
    print(recommend_similar_products(pid, top_n=5))