from models.product import Product
from models.order import Order
from database.mongodb import MongoDB
from services.product_service import ProductService
from services.order_service import OrderService

def add_product_cli(product_service):
    print("\n===== ADD NEW PRODUCT =====")

    product_code = input("Product code: ").strip()
    name = input("Product name: ").strip()
    category = input("Category: ").strip()
    brand = input("Brand: ").strip()
    unit = input("Unit: ").strip()

    try:
        unit_price = float(input("Unit price: "))
        stock = int(input("Stock: "))
    except ValueError:
        print("Price or stock is invalid!")
        return

    if not all([product_code, name, category, brand, unit]):
        print("Product information cannot be empty!")
        return

    if unit_price <= 0 or stock < 0:
        print("Price must be greater than 0 and stock cannot be negative!")
        return

    product = Product(
        product_code=product_code,
        name=name,
        category=category,
        brand=brand,
        unit=unit,
        unit_price=unit_price,
        stock=stock
    )

    if product_service.add_product(product):
        print("Product added successfully!")
    else:
        print("Product code already exists!")

def update_product_price_cli(product_service):
    print("\n===== UPDATE PRODUCT PRICE =====")

    product_code = input("Product code: ").strip()
    if not product_code:
        print("Product code cannot be empty!")
        return

    if not product_service.is_product_code_exist(product_code):
        print("Product not found!")
        return

    try:
        new_price = float(input("New unit price: "))
    except ValueError:
        print("Invalid price!")
        return

    if new_price <= 0:
        print("Price must be greater than 0!")
        return

    if product_service.update_product_price(product_code, new_price):
        print("Product price updated successfully!")
    else:
        print("Failed to update product price!")

def create_order_cli(product_service, order_service):
    print("\n===== CREATE ORDER =====")

    customer_name = input("Customer name: ").strip()
    if not customer_name:
        print("Customer name cannot be empty!")
        return

    items = []
    total_amount = 0

    while True:
        product_code = input("Product code: ").strip()
        product = product_service.get_product_by_code(product_code)

        if not product:
            print("Product not found!")
            return

        print(f"Product: {product['name']}")
        print(f"Unit price: {product['unit_price']:,}")
        print(f"Available stock: {product['stock']}")

        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Invalid quantity!")
            return

        if quantity <= 0:
            print("Quantity must be greater than 0!")
            return

        if quantity > product['stock']:
            print("Quantity exceeds available stock!")
            return

        subtotal = quantity * product["unit_price"]

        item = {
            "product_code": product["product_code"],
            "name": product["name"],
            "quantity": quantity,
            "unit_price": product["unit_price"],
            "subtotal": subtotal
        }

        items.append(item)
        total_amount += subtotal
        print(f"Subtotal: {subtotal:,}")

        choice = input("Add another product? (y/n): ").strip().lower()

        if choice != "y":
            break

    print(f"Total amount: {total_amount:,}")

def main():
    mongodb = MongoDB()
    try:
        mongodb.check_connection()
        product_collection = mongodb.get_collection("products")
        product_service = ProductService(product_collection)
        # add_product_cli(product_service)
        # update_product_price_cli(product_service)

        order_collection = mongodb.get_collection("orders")
        order_service = OrderService(
            mongodb.client,
            order_collection,
            product_collection
        )
        create_order_cli(product_service, order_service)
    except Exception as e:
        print(f"An error occurred!: {e}")

    finally:
        mongodb.close_connection()

if __name__ == "__main__":
    main()

