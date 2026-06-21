import sqlite3
import random
from datetime import datetime, timedelta
import numpy as np

random.seed(42)
np.random.seed(42)

conn = sqlite3.connect('nykaa.db')
cursor = conn.cursor()

# ---------- CREATE TABLES ----------
cursor.executescript('''
DROP TABLE IF EXISTS campaigns;
DROP TABLE IF EXISTS ad_events;

CREATE TABLE campaigns (
    campaign_id INTEGER PRIMARY KEY,
    campaign_name TEXT,
    ad_type TEXT,
    channel TEXT,
    start_date DATE,
    end_date DATE,
    budget REAL
);

CREATE TABLE ad_events (
    event_id INTEGER PRIMARY KEY,
    campaign_id INTEGER,
    customer_id INTEGER,
    event_type TEXT,
    event_date DATE,
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
''')

# ---------- CAMPAIGNS ----------
# Different ad types have realistically different performance baked in
campaign_configs = [
    # (name, ad_type, channel, ctr_rate, conversion_rate, budget)
    ("Diwali Sale - Influencer Push",      "Influencer", "Instagram",  0.065, 0.12, 150000),
    ("New Year Glow - Banner",             "Banner",     "Display Network", 0.018, 0.06, 80000),
    ("Skincare Routine - Email Blast",     "Email",      "Email",      0.045, 0.18, 20000),
    ("Lipstick Launch - Search Ads",       "Search",     "Google Ads", 0.055, 0.22, 100000),
    ("Summer Sale - Banner",               "Banner",     "Display Network", 0.015, 0.05, 75000),
    ("Festive Combo - Influencer",         "Influencer", "Instagram",  0.072, 0.14, 160000),
    ("Haircare Awareness - Email",         "Email",      "Email",      0.038, 0.15, 18000),
    ("Perfume Collection - Search Ads",    "Search",     "Google Ads", 0.048, 0.19, 90000),
    # A/B TEST PAIR — same campaign, two creative versions
    ("Monsoon Sale - Version A (Bold)",    "Banner",     "Display Network", 0.022, 0.07, 50000),
    ("Monsoon Sale - Version B (Minimal)", "Banner",     "Display Network", 0.031, 0.09, 50000),
]

campaigns = []
start_base = datetime(2025, 1, 1)
for i, (name, ad_type, channel, ctr, conv, budget) in enumerate(campaign_configs, 1):
    start = start_base + timedelta(days=random.randint(0, 300))
    end = start + timedelta(days=random.randint(14, 45))
    campaigns.append((i, name, ad_type, channel, start.date(), end.date(), budget))

cursor.executemany('INSERT INTO campaigns VALUES (?,?,?,?,?,?,?)', campaigns)

# ---------- AD EVENTS (the funnel: impression -> click -> purchase) ----------
ad_events = []
event_id = 1

# Get real customer IDs from your existing customers table
cursor.execute("SELECT customer_id FROM customers")
all_customer_ids = [row[0] for row in cursor.fetchall()]

for idx, (name, ad_type, channel, ctr_rate, conv_rate, budget) in enumerate(campaign_configs, 1):
    campaign_id = idx
    start_date, end_date = campaigns[idx-1][4], campaigns[idx-1][5]
    
    # Number of impressions scales roughly with budget
    num_impressions = int(budget / random.uniform(8, 15))  # cost per impression-ish
    
    # Pick random customers to show the ad to (with repeats - same person can see ad multiple times)
    impression_customers = random.choices(all_customer_ids, k=num_impressions)
    
    for cust_id in impression_customers:
        event_date = datetime.combine(start_date, datetime.min.time()) + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        # Impression always happens
        ad_events.append((event_id, campaign_id, cust_id, 'impression', event_date.date()))
        event_id += 1
        
        # Click happens probabilistically based on campaign's CTR
        if random.random() < ctr_rate:
            click_date = event_date + timedelta(hours=random.randint(0, 48))
            ad_events.append((event_id, campaign_id, cust_id, 'click', click_date.date()))
            event_id += 1
            
            # Purchase happens probabilistically based on conversion rate (only if clicked)
            if random.random() < conv_rate:
                purchase_date = click_date + timedelta(days=random.randint(0, 5))
                ad_events.append((event_id, campaign_id, cust_id, 'purchase', purchase_date.date()))
                event_id += 1

cursor.executemany('INSERT INTO ad_events VALUES (?,?,?,?,?)', ad_events)

conn.commit()
conn.close()

print(f"✅ Module 2 data created")
print(f"Campaigns: {len(campaigns)}")
print(f"Total ad events: {len(ad_events)}")