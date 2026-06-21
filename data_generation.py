import sqlite3
import random
from datetime import datetime, timedelta
from faker import Faker
import numpy as np

fake = Faker('en_IN')  # Indian names/locale - fits Nykaa's customer base
random.seed(42)
np.random.seed(42)

conn = sqlite3.connect('nykaa.db')
cursor = conn.cursor()

# ---------- CREATE TABLES ----------
cursor.executescript('''
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS reviews;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    signup_date DATE,
    city TEXT,
    age_group TEXT
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    brand TEXT,
    price REAL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE reviews (
    review_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product_id INTEGER,
    rating INTEGER,
    review_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
''')

# ---------- CUSTOMERS ----------
cities = ['Mumbai', 'Delhi', 'Bangalore', 'Pune', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
age_groups = ['18-24', '25-34', '35-44', '45-54']

customers = []
start_date = datetime(2023, 1, 1)
for i in range(1, 5001):
    signup = start_date + timedelta(days=random.randint(0, 700))
    customers.append((
        i, fake.name(), signup.date(), random.choice(cities), random.choice(age_groups)
    ))

cursor.executemany('INSERT INTO customers VALUES (?,?,?,?,?)', customers)

# ---------- PRODUCTS ----------
categories = {
    'Skincare': ['Face Wash', 'Moisturizer', 'Sunscreen', 'Serum', 'Face Mask'],
    'Makeup': ['Lipstick', 'Foundation', 'Kajal', 'Mascara', 'Compact'],
    'Haircare': ['Shampoo', 'Conditioner', 'Hair Oil', 'Hair Serum'],
    'Fragrance': ['Perfume', 'Deodorant', 'Body Mist'],
    'Bath & Body': ['Body Lotion', 'Body Wash', 'Hand Cream']
}
brands = ['Nykaa Cosmetics', 'Lakme', 'Maybelline', 'MCaffeine', 'Plum', 'WOW Skin Science', 'Biotique', 'Mamaearth']

products = []
pid = 1
for cat, items in categories.items():
    for item in items:
        for _ in range(4):  # ~4 variants per item type
            products.append((
                pid,
                f"{random.choice(brands)} {item}",
                cat,
                random.choice(brands),
                round(random.uniform(149, 1999), 2)
            ))
            pid += 1

cursor.executemany('INSERT INTO products VALUES (?,?,?,?,?)', products)
num_products = len(products)

# ---------- ORDERS + ORDER ITEMS (realistic, skewed behavior) ----------
# Customer "types" so data isn't uniformly random:
# 15% loyal/frequent, 35% occasional, 30% one-time, 20% churned-after-multiple

orders = []
order_items = []
order_id = 1
order_item_id = 1
today = datetime(2025, 12, 31)

for cust_id in range(1, 5001):
    roll = random.random()
    if roll < 0.15:
        num_orders = random.randint(8, 20)       # loyal customers
        last_order_recent = True
    elif roll < 0.50:
        num_orders = random.randint(3, 7)        # occasional
        last_order_recent = random.random() < 0.5
    elif roll < 0.80:
        num_orders = random.randint(1, 2)        # one-time/light
        last_order_recent = random.random() < 0.3
    else:
        num_orders = random.randint(4, 10)       # churned: active in past, quiet now
        last_order_recent = False

    cust_signup = customers[cust_id - 1][2]
    cust_signup_dt = datetime.combine(cust_signup, datetime.min.time())

    order_dates = []
    for _ in range(num_orders):
        if last_order_recent:
            days_ago = random.randint(0, 85)  # within last ~3 months
        else:
            days_ago = random.randint(100, 700)  # older, not recent
        order_dates.append(today - timedelta(days=days_ago))

    order_dates.sort()

    for od in order_dates:
        if od < cust_signup_dt:
            continue
        num_items = random.randint(1, 4)
        chosen_products = random.sample(range(1, num_products + 1), num_items)
        order_total = 0
        for p in chosen_products:
            qty = random.randint(1, 3)
            price = products[p - 1][4]
            order_total += qty * price
            order_items.append((order_item_id, order_id, p, qty, price))
            order_item_id += 1

        orders.append((order_id, cust_id, od.date(), round(order_total, 2)))
        order_id += 1

cursor.executemany('INSERT INTO orders VALUES (?,?,?,?)', orders)
cursor.executemany('INSERT INTO order_items VALUES (?,?,?,?,?)', order_items)

# ---------- REVIEWS ----------
reviews = []
review_id = 1
for cust_id, _, order_date, _ in orders:
    if random.random() < 0.4:  # 40% of orders get reviewed
        p = random.randint(1, num_products)
        rating = np.random.choice([5,4,3,2,1], p=[0.40,0.30,0.15,0.10,0.05])
        review_date = order_date + timedelta(days=random.randint(1, 14))
        reviews.append((review_id, cust_id, p, int(rating), review_date))
        review_id += 1

cursor.executemany('INSERT INTO reviews VALUES (?,?,?,?,?)', reviews)

conn.commit()
conn.close()

print(f"✅ Database created: nykaa.db")
print(f"Customers: {len(customers)} | Products: {len(products)} | Orders: {len(orders)} | Order Items: {len(order_items)} | Reviews: {len(reviews)}")