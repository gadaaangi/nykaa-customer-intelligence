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
    order_id INTEGER,  -- NEW: links a 'purchase' event to a real order
    FOREIGN KEY (campaign_id) REFERENCES campaigns(campaign_id),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
''')

# ---------- CAMPAIGNS ----------
campaign_configs = [
    ("Diwali Sale - Influencer Push",      "Influencer", "Instagram",  0.065, 0.12, 150000),
    ("New Year Glow - Banner",             "Banner",     "Display Network", 0.018, 0.06, 80000),
    ("Skincare Routine - Email Blast",     "Email",      "Email",      0.045, 0.18, 20000),
    ("Lipstick Launch - Search Ads",       "Search",     "Google Ads", 0.055, 0.22, 100000),
    ("Summer Sale - Banner",               "Banner",     "Display Network", 0.015, 0.05, 75000),
    ("Festive Combo - Influencer",         "Influencer", "Instagram",  0.072, 0.14, 160000),
    ("Haircare Awareness - Email",         "Email",      "Email",      0.038, 0.15, 18000),
    ("Perfume Collection - Search Ads",    "Search",     "Google Ads", 0.048, 0.19, 90000),
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

# ---------- GET EXISTING DATA WE NEED ----------
cursor.execute("SELECT customer_id FROM customers")
all_customer_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id, price FROM products")
products = cursor.fetchall()  # [(product_id, price), ...]

# Find current max order_id and order_item_id so we don't clash with Module 1 data
cursor.execute("SELECT MAX(order_id) FROM orders")
next_order_id = (cursor.fetchone()[0] or 0) + 1

cursor.execute("SELECT MAX(order_item_id) FROM order_items")
next_order_item_id = (cursor.fetchone()[0] or 0) + 1

# ---------- AD EVENTS + REAL LINKED ORDERS ----------
ad_events = []
new_orders = []
new_order_items = []
event_id = 1

for idx, (name, ad_type, channel, ctr_rate, conv_rate, budget) in enumerate(campaign_configs, 1):
    campaign_id = idx
    start_date, end_date = campaigns[idx-1][4], campaigns[idx-1][5]
    
    num_impressions = int(budget / random.uniform(8, 15))
    impression_customers = random.choices(all_customer_ids, k=num_impressions)
    
    for cust_id in impression_customers:
        event_date = datetime.combine(start_date, datetime.min.time()) + timedelta(
            days=random.randint(0, (end_date - start_date).days)
        )
        
        ad_events.append((event_id, campaign_id, cust_id, 'impression', event_date.date(), None))
        event_id += 1
        
        if random.random() < ctr_rate:
            click_date = event_date + timedelta(hours=random.randint(0, 48))
            ad_events.append((event_id, campaign_id, cust_id, 'click', click_date.date(), None))
            event_id += 1
            
            if random.random() < conv_rate:
                purchase_date = click_date + timedelta(days=random.randint(0, 5))
                
                # ---- Create a REAL order for this ad-driven purchase ----
                num_items = random.randint(1, 3)
                chosen_products = random.sample(products, num_items)
                order_total = 0
                for p_id, p_price in chosen_products:
                    qty = random.randint(1, 2)
                    order_total += qty * p_price
                    new_order_items.append((next_order_item_id, next_order_id, p_id, qty, p_price))
                    next_order_item_id += 1
                
                new_orders.append((next_order_id, cust_id, purchase_date.date(), round(order_total, 2)))
                
                # Link this ad-event purchase to the real order_id
                ad_events.append((event_id, campaign_id, cust_id, 'purchase', purchase_date.date(), next_order_id))
                event_id += 1
                next_order_id += 1

cursor.executemany('INSERT INTO ad_events VALUES (?,?,?,?,?,?)', ad_events)
cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', new_orders)
cursor.executemany('INSERT INTO order_items VALUES (?,?,?,?,?)', new_order_items)

conn.commit()
conn.close()

print(f"✅ Module 2 data regenerated with real linked orders")
print(f"Campaigns: {len(campaigns)}")
print(f"Total ad events: {len(ad_events)}")
print(f"New orders created from ad purchases: {len(new_orders)}")