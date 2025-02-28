from datetime import datetime, timedelta

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["online_store"]
collection_products = db["products"]
collection_orders = db["orders"]


products_list = [
    {"name": "кроссовки", "price": 1000, "category": "Adidas", "quantity": 1},
    {"name": "ботинки", "price": 1500, "category": "Nike", "quantity": 20},
    {"name": "пальто", "price": 2000, "category": "Levis", "quantity": 15},
    {"name": "куртка", "price": 3000, "category": "Zara", "quantity": 25},
    {"name": "штаны", "price": 500, "category": "H&M", "quantity": 40},
]


orders_list = [
    {
        "orderNumber": 1,
        "date": datetime.now(),
        "customer": "Иван Петров",
        "products": [
            {"name": "кроссовки", "quantity": 2},
            {"name": "ботинки", "quantity": 1},
        ],
        "total": 3500,
    },
    {
        "orderNumber": 2,
        "date": datetime.now(),
        "customer": "Светлана Иванова",
        "products": [
            {"name": "пальто", "quantity": 3},
            {"name": "штаны", "quantity": 1},
        ],
        "total": 2000,
    },
]


collection_products.insert_many(products_list)
collection_orders.insert_many(orders_list)

collection_products.update_one({"name": "кроссовки"}, {"$inc": {"quantity": -1}})
collection_products.delete_many({"quantity": {"$eq": 0}})

for product in collection_products.find():
    print(f"Информация о товаре: {product}")

list_orders = list(collection_orders.find({"total": {"$gte": 3000}}))

for order in list_orders:
    print(f"Список заказов с суммой более 3000 гривен: {order}")


def calculate_items_sold_in_n_days(n: int) -> list:
    """Calculate the total quantity of each item sold in the last n days.

    This function queries a MongoDB collection of orders to determine the total quantity of each item sold within the specified number of days.

    Args:
        n (int): The number of days to look back from the current date.

    Returns:
        list: A list of dictionaries, where each dictionary represents
        an item and its total quantity sold. Each dictionary has the keys "_id" (item name) and "total" (quantity sold)."""
    days_ago = datetime.now() - timedelta(days=n)
    last_days_orders = [
        {"$match": {"date": {"$gte": days_ago}}},
        {"$unwind": "$products"},
        {"$group": {"_id": "$products.name", "total": {"$sum": "$products.quantity"}}},
    ]
    return list(collection_orders.aggregate(last_days_orders))


def calculate_sum_all_orders_customer(name: str) -> float:
    """Calculate the total sum of all orders for a given customer.

    This function queries a MongoDB collection of orders and calculates the sum of the 'total' field for all orders matching a specific customer name.

    Args:
        name (str): The name of the customer.

    Returns:
        float: The total sum of all orders for the given customer.
    """
    try:
        calculate_sum_orders = [
            {"$match": {"customer": name}},
            {"$group": {"_id": 1, "total": {"$sum": "$total"}}},
        ]
        result = list(collection_orders.aggregate(calculate_sum_orders))

        return result[0].get("total", 0.0) if result else 0.0

    except Exception as er:
        print(f"Error: {er}")
        return 0.0


if __name__ == "__main__":
    try:
        day = 2
        total = calculate_items_sold_in_n_days(day)
        print(f"Товары, проданные за последние {day} дня: \n {total} ")
        name_customer = "Иван Петров"
        calculate_sum_all_orders_customer(name_customer)
        print(
            f"Сумма всех заказов клиента {name_customer}: {calculate_sum_all_orders_customer(name_customer)} гривен"
        )

        collection_products.create_index("category")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client.close()
