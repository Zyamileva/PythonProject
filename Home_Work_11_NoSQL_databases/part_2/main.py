import psycopg2
from datetime import datetime, timedelta


conn = psycopg2.connect(
    dbname="mydatabase",
    user="zyamileva",
    password="123456789",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()


def delete():
    cursor.execute("DROP TABLE orders CASCADE")
    cursor.execute("DROP TABLE products CASCADE")
    cursor.execute("DROP TABLE order_items CASCADE")
    conn.commit()


delete()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        price DECIMAL NOT NULL,
        category TEXT,
        quantity INT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        order_number TEXT UNIQUE NOT NULL,
        customer TEXT NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount DECIMAL NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id SERIAL PRIMARY KEY,
        order_id INT REFERENCES orders(id),
        product_id INT REFERENCES products(id),
        quantity INT NOT NULL
    )
""")

conn.commit()


def add_product(name, price, category, quantity):
    cursor.execute(
        "INSERT INTO products (name, price, category, quantity) VALUES (%s, %s, %s, %s)",
        (name, price, category, quantity),
    )
    conn.commit()


def create_order(order_number, customer, items):
    total_amount = sum(item["price"] * item["quantity"] for item in items)
    cursor.execute(
        """
        INSERT INTO orders (order_number, customer, total_amount)
        VALUES (%s, %s, %s) RETURNING id
    """,
        (order_number, customer, total_amount),
    )

    order_id = cursor.fetchone()[0]

    for item in items:
        cursor.execute(
            """
            INSERT INTO order_items (order_id, product_id, quantity) 
            VALUES (%s,%s,%s)""",
            (order_id, item["id"], item["quantity"]),
        )

        cursor.execute(
            """
            UPDATE products SET quantity = quantity- %s where id =%s""",
            (item["quantity"], item["id"]),
        )

    conn.commit()


def get_orders_30_days():
    delta_days = datetime.now() - timedelta(days=30)
    cursor.execute("SELECT * FROM orders WHERE order_date >= %s", (delta_days,))
    return cursor.fetchall()


def delete_unavailable_products():
    cursor.execute("DELETE FROM products WHERE quantity <= 0")
    conn.commit()


def calculate_items_sold_in_n_days(n: int) -> list:
    days_ago = datetime.now() - timedelta(days=n)
    cursor.execute(
        """
        SELECT SUM(order_items.quantity) FROM order_items
        JOIN orders ON orders.id = order_items.order_id
        WHERE orders.order_date >= %s""",
        (days_ago,),
    )
    result = cursor.fetchone()
    return result[0] if result and result[0] else 0


def total_amount_by_customer(customer):
    cursor.execute(
        "SELECT SUM(total_amount) FROM orders WHERE customer = %s", (customer,)
    )
    result = cursor.fetchone()
    return result[0] if result and result[0] else 0


cursor.execute(
    "CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);"
)
conn.commit()

if __name__ == "__main__":
    add_product("Product 1", 10.99, "Electronics", 100)
    add_product("Product 2", 29.99, "Clothing", 50)

    create_order("order-12345", "John Doe", [{"id": 1, "price": 10.99, "quantity": 2}])
    create_order(
        "order-67890", "Jane Smith", [{"id": 2, "price": 29.99, "quantity": 1}]
    )

    for order in get_orders_30_days():
        print(f"Order - {order[0]} - {order[1]} - {order[3]}")

    sold = calculate_items_sold_in_n_days(2)
    print(f"Number of items sold in 2 days: {sold}")

    total_sum = total_amount_by_customer("John Doe")
    print(f"Total amount for customer John Doe: {total_sum}")

    delete_unavailable_products()
cursor.close()
conn.close()
