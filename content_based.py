import sqlite3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

conn = sqlite3.connect('nykaa.db')

products_df = pd.read_sql_query("SELECT product_id, product_name, category, brand, price FROM products", conn)
products_df = products_df.set_index('product_id')

# ---------- ONE-HOT ENCODE CATEGORY AND BRAND ----------
category_dummies = pd.get_dummies(products_df['category'], prefix='cat')
brand_dummies = pd.get_dummies(products_df['brand'], prefix='brand')

# ---------- NORMALIZE PRICE (0 to 1 range) ----------
scaler = MinMaxScaler()
price_scaled = pd.DataFrame(
    scaler.fit_transform(products_df[['price']]), 
    columns=['price_scaled'], 
    index=products_df.index
)

# ---------- COMBINE INTO ONE FEATURE MATRIX ----------
feature_matrix = pd.concat([category_dummies, brand_dummies, price_scaled], axis=1)

print(f"Feature matrix shape: {feature_matrix.shape}")
print(f"Features used: {list(feature_matrix.columns)}\n")

# ---------- COMPUTE CONTENT-BASED SIMILARITY ----------
content_similarity = cosine_similarity(feature_matrix)
content_similarity_df = pd.DataFrame(
    content_similarity, 
    index=feature_matrix.index, 
    columns=feature_matrix.index
)

content_similarity_df.to_pickle('content_similarity.pkl')
print("✅ Saved: content_similarity.pkl")

# ---------- RECOMMENDATION FUNCTION ----------
def recommend_content_based(product_id, top_n=5):
    if product_id not in content_similarity_df.index:
        return f"Product ID {product_id} not found."
    scores = content_similarity_df[product_id].sort_values(ascending=False)
    scores = scores.drop(product_id)
    top_matches = scores.head(top_n)
    result = products_df.loc[top_matches.index].copy()
    result['similarity_score'] = top_matches.values.round(3)
    return result[['product_name', 'category', 'brand', 'price', 'similarity_score']]

# ---------- TEST ON THE SAME PRODUCT AS COLLABORATIVE FILTERING ----------
sample_id = 51  # MCaffeine Hair Oil - same one you already tested
sample_name = products_df.loc[sample_id, 'product_name']

print(f"\nContent-based recommendations for: '{sample_name}' (ID: {sample_id})\n")
print(recommend_content_based(sample_id, top_n=5))

conn.close()