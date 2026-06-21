# 💄 Nykaa Customer Intelligence & Beauty Recommendation System

An end-to-end e-commerce analytics project simulating a beauty retail 
platform — covering customer behavior analytics, ad campaign performance, 
and a product recommendation engine. Built to mirror the SQL-heavy, 
business-driven analytics work done at companies like Nykaa.

## 🎯 Project Overview

This project answers three core business questions a retail analytics 
team would tackle:

1. **Who are our customers, and who's at risk of churning?**
2. **Which marketing channels actually drive profitable growth?**
3. **What should we recommend to customers to increase cross-sell?**

Each module is self-contained but shares the same underlying dataset — 
a simulated beauty e-commerce platform with 5,000 customers, 80 products, 
20,000+ orders, and 70,000+ ad events.

## 📊 Module 1: Customer Behavior Analytics

SQL-driven analysis covering churn detection, RFM segmentation, cohort 
retention, and repeat purchase rates.

**Key findings:**
- 84.4% repeat purchase rate
- Customer base is polarized: 60% fall into either "Champions" or "Lost" 
  segments, with few in between
- Churn risk is concentrated almost entirely in the first month after 
  signup — customers who survive past month 1 retain at a stable ~20% 
  rate long-term

**Skills demonstrated:** SQL (window functions, CTEs, subqueries), 
RFM segmentation, cohort analysis, Python/Pandas, data visualization

[→ Full Module 1 writeup](./module1_customer_analytics/README.md)

## 📈 Module 2: Ad Campaign & Marketing Analytics

Simulated ad funnel (impressions → clicks → purchases) across 10 
campaigns, with revenue attribution and A/B testing.

**Key findings:**
- Search and Influencer campaigns deliver 2.6x–4.4x ROAS; every Banner 
  campaign loses money (ROAS < 1.0)
- A/B test confirmed a statistically significant CTR difference between 
  creative versions (p < 0.0001)
- Channel selection matters more than creative design — even the 
  A/B-test "winner" remained unprofitable due to its channel

**Skills demonstrated:** SQL (funnel metrics, attribution joins), 
statistical hypothesis testing (two-proportion z-test), Python/statsmodels

[→ Full Module 2 writeup](./module2_ad_campaign_analytics/README.md)

## 🤖 Module 3: Product Recommendation Engine

Two complementary recommendation approaches: collaborative filtering 
(purchase behavior) and content-based filtering (product attributes).

**Key findings:**
- Collaborative filtering surfaces cross-category recommendations based 
  on real co-purchase patterns
- Content-based filtering stays within category with much sharper 
  confidence scores (0.999 vs 0.22)
- A production system would blend both — content-based for new products, 
  collaborative for established ones

**Skills demonstrated:** Scikit-learn (cosine similarity), feature 
engineering (one-hot encoding, normalization), recommendation systems

[→ Full Module 3 writeup](./module3_recommendation_engine/README.md)

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Database | SQLite |
| Data manipulation | Python, Pandas, NumPy |
| Statistics/ML | Scikit-learn, Statsmodels |
| Visualization | Matplotlib, Seaborn |

## 📁 Repository Structure
