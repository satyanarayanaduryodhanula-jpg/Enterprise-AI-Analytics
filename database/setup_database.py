import psycopg2

HOST = "localhost"
USER = "postgres"
PASSWORD = "saibaba"
DATABASE = "enterprise_analytics"

# -----------------------------------
# STEP 1 : Connect to PostgreSQL
# -----------------------------------

connection = psycopg2.connect(
    host=HOST,
    database="postgres",
    user=USER,
    password=PASSWORD
)

connection.autocommit = True
cursor = connection.cursor()

# -----------------------------------
# STEP 2 : Create Database If Needed
# -----------------------------------

cursor.execute("""
SELECT 1
FROM pg_database
WHERE datname=%s
""", (DATABASE,))

if cursor.fetchone() is None:
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    print("Database Created")
else:
    print("Database Already Exists")

cursor.close()
connection.close()

# -----------------------------------
# STEP 3 : Connect to Enterprise Database
# -----------------------------------

connection = psycopg2.connect(
    host=HOST,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)

cursor = connection.cursor()

# -----------------------------------
# STEP 4 : Create Tables
# -----------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(100),
    price DECIMAL(10,2),
    stock INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(150),
    phone VARCHAR(20),
    city VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    order_date DATE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory(
    inventory_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    available_stock INT
)
""")

connection.commit()

print("Tables Created Successfully")

# -----------------------------------
# STEP 5 : Insert Products
# -----------------------------------

cursor.execute("SELECT COUNT(*) FROM products")
count = cursor.fetchone()[0]

if count == 0:

    products = [
        ("Laptop","Electronics",65000,20),
        ("Mouse","Electronics",600,150),
        ("Keyboard","Electronics",1800,70),
        ("Monitor","Electronics",15000,25),
        ("Headphones","Electronics",2500,80),
        ("Printer","Electronics",12000,15),
        ("Tablet","Electronics",30000,30),
        ("Mobile Phone","Electronics",45000,40),
        ("Smart Watch","Electronics",12000,35),
        ("Speaker","Electronics",3500,60)
    ]

    cursor.executemany("""
    INSERT INTO products
    (product_name,category,price,stock)
    VALUES(%s,%s,%s,%s)
    """, products)

    print("Products Inserted")

# -----------------------------------
# STEP 6 : Insert Customers
# -----------------------------------

cursor.execute("SELECT COUNT(*) FROM customers")
count = cursor.fetchone()[0]

if count == 0:

    customers = [
        ("Rahul","rahul@gmail.com","9876543210","Hyderabad"),
        ("Priya","priya@gmail.com","9876543211","Bangalore"),
        ("Amit","amit@gmail.com","9876543212","Chennai"),
        ("Sneha","sneha@gmail.com","9876543213","Mumbai"),
        ("Ravi","ravi@gmail.com","9876543214","Delhi"),
        ("Anjali","anjali@gmail.com","9876543215","Pune"),
        ("Kiran","kiran@gmail.com","9876543216","Hyderabad"),
        ("Deepak","deepak@gmail.com","9876543217","Kolkata"),
        ("Neha","neha@gmail.com","9876543218","Jaipur"),
        ("Arjun","arjun@gmail.com","9876543219","Visakhapatnam")
    ]

    cursor.executemany("""
    INSERT INTO customers
    (customer_name,email,phone,city)
    VALUES(%s,%s,%s,%s)
    """, customers)

    print("Customers Inserted")

# -----------------------------------
# STEP 7 : Insert Orders
# -----------------------------------

cursor.execute("SELECT COUNT(*) FROM orders")
count = cursor.fetchone()[0]

if count == 0:

    orders = [
        (1,1,1,'2026-07-01'),
        (2,3,2,'2026-07-02'),
        (3,2,1,'2026-07-02'),
        (4,5,3,'2026-07-03'),
        (5,4,1,'2026-07-03'),
        (6,6,2,'2026-07-04'),
        (7,7,1,'2026-07-05'),
        (8,8,2,'2026-07-06'),
        (9,9,1,'2026-07-07'),
        (10,10,2,'2026-07-08'),
        (1,2,5,'2026-07-09'),
        (2,1,1,'2026-07-10'),
        (3,5,2,'2026-07-11'),
        (4,7,1,'2026-07-12'),
        (5,8,2,'2026-07-13')
    ]

    cursor.executemany("""
    INSERT INTO orders
    (customer_id,product_id,quantity,order_date)
    VALUES(%s,%s,%s,%s)
    """, orders)

    print("Orders Inserted")

# -----------------------------------
# STEP 8 : Insert Inventory
# -----------------------------------

cursor.execute("SELECT COUNT(*) FROM inventory")
count = cursor.fetchone()[0]

if count == 0:

    inventory = [
        (1,20),
        (2,150),
        (3,70),
        (4,25),
        (5,80),
        (6,15),
        (7,30),
        (8,40),
        (9,35),
        (10,60)
    ]

    cursor.executemany("""
    INSERT INTO inventory
    (product_id,available_stock)
    VALUES(%s,%s)
    """, inventory)

    print("Inventory Inserted")

# -----------------------------------
# STEP 9 : Save Everything
# -----------------------------------

connection.commit()

print("\n===================================")
print("Enterprise Database Ready")
print("Products      : OK")
print("Customers     : OK")
print("Orders        : OK")
print("Inventory     : OK")
print("===================================")

cursor.close()
connection.close()