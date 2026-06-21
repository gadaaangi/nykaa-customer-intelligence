import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect('nykaa.db')
sns.set_style("whitegrid")

# ============================================
# VISUAL 1: CTR & Conversion Rate by Campaign
# ============================================
funnel_query = """
SELECT 
    c.campaign_name,
    c.ad_type,
    SUM(CASE WHEN ae.event_type = 'impression' THEN 1 ELSE 0 END) AS impressions,
    SUM(CASE WHEN ae.event_type = 'click' THEN 1 ELSE 0 END) AS clicks,
    SUM(CASE WHEN ae.event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases,
    ROUND(100.0 * SUM(CASE WHEN ae.event_type = 'click' THEN 1 ELSE 0 END) / 
          NULLIF(SUM(CASE WHEN ae.event_type = 'impression' THEN 1 ELSE 0 END), 0), 2) AS ctr_pct
FROM campaigns c
JOIN ad_events ae ON c.campaign_id = ae.campaign_id
GROUP BY c.campaign_id, c.campaign_name, c.ad_type
ORDER BY ctr_pct DESC
"""
df_funnel = pd.read_sql_query(funnel_query, conn)

plt.figure(figsize=(10,6))
colors = {'Influencer': '#E91E63', 'Search': '#AB47BC', 'Email': '#F8BBD0', 'Banner': '#CE93D8'}
bar_colors = df_funnel['ad_type'].map(colors)
plt.barh(df_funnel['campaign_name'], df_funnel['ctr_pct'], color=bar_colors)
plt.xlabel('CTR (%)')
plt.title('Click-Through Rate by Campaign', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
# legend
handles = [plt.Rectangle((0,0),1,1, color=c) for c in colors.values()]
plt.legend(handles, colors.keys(), title='Ad Type', loc='lower right')
plt.tight_layout()
plt.savefig('5_ctr_by_campaign.png', dpi=150)
plt.close()
print("✅ Saved: 5_ctr_by_campaign.png")

# ============================================
# VISUAL 2: ROAS by Campaign
# ============================================
roas_query = """
SELECT 
    c.campaign_name,
    c.ad_type,
    c.budget,
    ROUND(SUM(o.total_amount), 2) AS attributed_revenue,
    ROUND(SUM(o.total_amount) / c.budget, 2) AS roas
FROM campaigns c
LEFT JOIN ad_events ae ON c.campaign_id = ae.campaign_id AND ae.event_type = 'purchase'
LEFT JOIN orders o ON ae.order_id = o.order_id
GROUP BY c.campaign_id, c.campaign_name, c.ad_type, c.budget
ORDER BY roas DESC
"""
df_roas = pd.read_sql_query(roas_query, conn)
df_roas['roas'] = df_roas['roas'].fillna(0)

plt.figure(figsize=(10,6))
bar_colors2 = df_roas['ad_type'].map(colors)
bars = plt.barh(df_roas['campaign_name'], df_roas['roas'], color=bar_colors2)
plt.axvline(x=1.0, color='black', linestyle='--', linewidth=1, label='Breakeven (ROAS = 1.0)')
plt.xlabel('ROAS (Revenue / Spend)')
plt.title('Return on Ad Spend (ROAS) by Campaign', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig('6_roas_by_campaign.png', dpi=150)
plt.close()
print("✅ Saved: 6_roas_by_campaign.png")

# ============================================
# VISUAL 3: Conversion Funnel (Overall, all campaigns combined)
# ============================================
overall_funnel_query = """
SELECT 
    SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END) AS impressions,
    SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) AS clicks,
    SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) AS purchases
FROM ad_events
"""
df_overall = pd.read_sql_query(overall_funnel_query, conn)
stages = ['Impressions', 'Clicks', 'Purchases']
values = [df_overall['impressions'][0], df_overall['clicks'][0], df_overall['purchases'][0]]

plt.figure(figsize=(8,6))
bars = plt.bar(stages, values, color=['#F8BBD0', '#E91E63', '#880E4F'], width=0.5)
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01, 
              f'{val:,}', ha='center', fontweight='bold')
plt.title('Overall Ad Funnel: Impressions → Clicks → Purchases', fontsize=14, fontweight='bold')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig('7_overall_funnel.png', dpi=150)
plt.close()
print("✅ Saved: 7_overall_funnel.png")

# ============================================
# VISUAL 4: A/B Test Comparison (Monsoon Sale)
# ============================================
ab_data = pd.DataFrame({
    'Version': ['Version A (Bold)', 'Version B (Minimal)'],
    'CTR': [1.92, 3.57]
})

plt.figure(figsize=(6,5))
bars = plt.bar(ab_data['Version'], ab_data['CTR'], color=['#CE93D8', '#E91E63'], width=0.5)
for bar, val in zip(bars, ab_data['CTR']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
              f'{val}%', ha='center', fontweight='bold')
plt.title('A/B Test: Monsoon Sale CTR\n(p < 0.0001, statistically significant)', fontsize=13, fontweight='bold')
plt.ylabel('CTR (%)')
plt.tight_layout()
plt.savefig('8_ab_test_result.png', dpi=150)
plt.close()
print("✅ Saved: 8_ab_test_result.png")

conn.close()
print("\n🎉 All Module 2 visuals generated!")