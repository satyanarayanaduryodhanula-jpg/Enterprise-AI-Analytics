import os
from pathlib import Path

from dotenv import load_dotenv
import psycopg2


# ==========================================
# Load Environment Variables
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env", override=True)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is missing. Check your .env file."
    )


# ==========================================
# Connect to PostgreSQL
# ==========================================

print("Connecting to PostgreSQL...")

connection = psycopg2.connect(DATABASE_URL)

cursor = connection.cursor()

print("Database connected successfully.")


# ==========================================
# Create Products Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0
)
""")


# ==========================================
# Create Customers Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150),
    phone VARCHAR(20),
    city VARCHAR(100)
)
""")


# ==========================================
# Create Orders Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id SERIAL PRIMARY KEY,

    customer_id INT REFERENCES customers(customer_id),

    product_id INT REFERENCES products(product_id),

    quantity INT NOT NULL,

    order_date DATE NOT NULL
)
""")


# ==========================================
# Create Inventory Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id SERIAL PRIMARY KEY,

    product_id INT REFERENCES products(product_id),

    available_stock INT DEFAULT 0
)
""")


# ==========================================
# Create AI Insights Table
# ==========================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_insights (
    id SERIAL PRIMARY KEY,

    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    business_health INT,

    best_product VARCHAR(100),

    worst_product VARCHAR(100),

    total_revenue DECIMAL(15,2),

    average_revenue DECIMAL(15,2),

    inventory_risk TEXT,

    recommendation TEXT
)
""")


connection.commit()

print("All tables created successfully.")


# ==========================================
# Insert Products
# ==========================================

cursor.execute("SELECT COUNT(*) FROM products")

product_count = cursor.fetchone()[0]

if product_count == 0:

    products = [
        ("Laptop", "Electronics", 65000, 20),
        ("Mouse", "Electronics", 600, 150),
        ("Keyboard", "Electronics", 1800, 70),
        ("Monitor", "Electronics", 15000, 25),
        ("Headphones", "Electronics", 2500, 80),
        ("Printer", "Electronics", 12000, 15),
        ("Tablet", "Electronics", 30000, 30),
        ("Mobile Phone", "Electronics", 45000, 40),
        ("Smart Watch", "Electronics", 12000, 35),
        ("Speaker", "Electronics", 3500, 60)
    ]

    cursor.executemany("""
        INSERT INTO products
        (
            product_name,
            category,
            price,
            stock
        )
        VALUES (%s, %s, %s, %s)
    """, products)

    print("Products inserted.")

else:

    print("Products already exist.")


# ==========================================
# Insert Customers
# ==========================================

cursor.execute("SELECT COUNT(*) FROM customers")

customer_count = cursor.fetchone()[0]

if customer_count == 0:

    customers = [
        ("Rahul", "rahul@gmail.com", "9876543210", "Hyderabad"),
        ("Priya", "priya@gmail.com", "9876543211", "Bangalore"),
        ("Amit", "amit@gmail.com", "9876543212", "Chennai"),
        ("Sneha", "sneha@gmail.com", "9876543213", "Mumbai"),
        ("Ravi", "ravi@gmail.com", "9876543214", "Delhi"),
        ("Anjali", "anjali@gmail.com", "9876543215", "Pune"),
        ("Kiran", "kiran@gmail.com", "9876543216", "Hyderabad"),
        ("Deepak", "deepak@gmail.com", "9876543217", "Kolkata"),
        ("Neha", "neha@gmail.com", "9876543218", "Jaipur"),
        ("Arjun", "arjun@gmail.com", "9876543219", "Visakhapatnam")
    ]

    cursor.executemany("""
        INSERT INTO customers
        (
            customer_name,
            email,
            phone,
            city
        )
        VALUES (%s, %s, %s, %s)
    """, customers)

    print("Customers inserted.")

else:

    print("Customers already exist.")


# ==========================================
# Insert Orders
# ==========================================

cursor.execute("SELECT COUNT(*) FROM orders")

order_count = cursor.fetchone()[0]

if order_count == 0:

    orders = [
        (1, 1, 1, "2026-07-01"),
        (2, 3, 2, "2026-07-02"),
        (3, 2, 1, "2026-07-02"),
        (4, 5, 3, "2026-07-03"),
        (5, 4, 1, "2026-07-03"),
        (6, 6, 2, "2026-07-04"),
        (7, 7, 1, "2026-07-05"),
        (8, 8, 2, "2026-07-06"),
        (9, 9, 1, "2026-07-07"),
        (10, 10, 2, "2026-07-08"),
        (1, 2, 5, "2026-07-09"),
        (2, 1, 1, "2026-07-10"),
        (3, 5, 2, "2026-07-11"),
        (4, 7, 1, "2026-07-12"),
        (5, 8, 2, "2026-07-13")
    ]

    cursor.executemany("""
        INSERT INTO orders
        (
            customer_id,
            product_id,
            quantity,
            order_date
        )
        VALUES (%s, %s, %s, %s)
    """, orders)

    print("Orders inserted.")

else:

    print("Orders already exist.")


# ==========================================
# Insert Inventory
# ==========================================

cursor.execute("SELECT COUNT(*) FROM inventory")

inventory_count = cursor.fetchone()[0]

if inventory_count == 0:

    inventory = [
        (1, 20),
        (2, 150),
        (3, 70),
        (4, 25),
        (5, 80),
        (6, 15),
        (7, 30),
        (8, 40),
        (9, 35),
        (10, 60)
    ]

    cursor.executemany("""
        INSERT INTO inventory
        (
            product_id,
            available_stock
        )
        VALUES (%s, %s)
    """, inventory)

    print("Inventory inserted.")

else:

    print("Inventory already exists.")


connection.commit()


# ==========================================
# Verify Database
# ==========================================

cursor.execute("SELECT COUNT(*) FROM products")
products_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM customers")
customers_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM orders")
orders_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM inventory")
inventory_total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM ai_insights")
ai_total = cursor.fetchone()[0]


print("\n======================================")
print("Enterprise Cloud Database Ready")
print("======================================")
print("Products     :", products_total)
print("Customers    :", customers_total)
print("Orders       :", orders_total)
print("Inventory    :", inventory_total)
print("AI Insights  :", ai_total)
print("======================================")


cursor.close()
connection.close()

print("Database connection closed.")