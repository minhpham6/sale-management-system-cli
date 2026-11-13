from datetime import datetime

from prettytable import PrettyTable

from database.mongodb import MongoDB
from models.order import Order
from models.product import Product
from services.excel_service import (
    export_orders_excel,
    export_products_excel,
    read_products_excel,
)
from services.order_service import OrderService
from services.product_service import ProductService


def read_products_excel_cli():
    print("\n===== READ PRODUCTS FROM EXCEL =====")

    try:
        df = read_products_excel()

        if df.empty:
            print("Excel file contains no products!")
            return

        table = PrettyTable()
        table.field_names = list(df.columns)

        for row in df.itertuples(index=False, name=None):
            table.add_row(row)

        print(table)
        print(f"Total products in Excel: {len(df)}")

    except Exception as e:
        print(f"Failed to read Excel file: {e}")


def display_products_cli(product_service):
    print("\n===== PRODUCT LIST =====")

    products = product_service.get_all_products()

    if not products:
        print("No products found!")
        return

    table = PrettyTable()
    table.field_names = [
        "Product Code", "Name", "Category", "Brand",
        "Unit", "Unit Price", "Stock"
    ]

    for product in products:
        table.add_row([
            product["product_code"],
            product["name"],
            product["category"],
            product["brand"],
            product["unit"],
            f"{product['unit_price']:,.0f}",
            product["stock"]
        ])

    print(table)


def search_products_cli(product_service):
    print("\n===== SEARCH PRODUCTS =====")

    keyword = input("Enter product code, name, brand or category: ").strip()

    if not keyword:
        print("Search keyword cannot be empty!")
        return

    products = product_service.search_products(keyword)

    if not products:
        print("No matching products found!")
        return

    table = PrettyTable()
    table.field_names = [
        "Product Code", "Name", "Category", "Brand",
        "Unit", "Unit Price", "Stock"
    ]

    for product in products:
        table.add_row([
            product["product_code"],
            product["name"],
            product["category"],
            product["brand"],
            product["unit"],
            f"{product['unit_price']:,.0f}",
            product["stock"]
        ])

    print(table)


def import_products_cli(product_service):
    print("\n===== IMPORT PRODUCTS TO MONGODB =====")

    try:
        result = product_service.import_products_mongodb()

        print("Product import completed!")
        print(f"Total products: {result['total']}")
        print(f"Inserted: {result['inserted']}")
        print(f"Updated: {result['updated']}")
        print(f"Unchanged: {result['unchanged']}")

    except Exception as e:
        print(f"Failed to import products: {e}")


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

        table = PrettyTable()
        table.field_names = ["Product Code", "Product", "Unit Price", "Stock"]
        table.add_row([
            product["product_code"],
            product["name"],
            f"{product['unit_price']:,.0f}",
            product["stock"]
        ])
        print(table)

        try:
            quantity = int(input("Quantity: "))
        except ValueError:
            print("Invalid quantity!")
            return

        if quantity <= 0:
            print("Quantity must be greater than 0!")
            return

        if quantity > product["stock"]:
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
        print(f"Subtotal: {subtotal:,.0f}")

        choice = input("Add another product? (y/n): ").strip().lower()

        if choice != "y":
            break

    print(f"Total amount: {total_amount:,.0f}")

    order_code = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"
    order = Order(
        order_code=order_code,
        customer_name=customer_name,
        items=items,
        total_amount=total_amount
    )

    confirm = input("Confirm order? (y/n): ").strip().lower()

    if confirm != "y":
        print("Order cancelled!")
        return

    try:
        if order_service.create_order(order):
            print("Order created successfully!")
            display_invoice_cli(order_service, order_code)
    except ValueError as e:
        print(f"Failed to create order: {e}")


def display_invoice_cli(order_service):
    print("\n===== DISPLAY INVOICE =====")

    order_code = input("Enter order code: ").strip()

    if not order_code:
        print("Order code cannot be empty!")
        return

    order = order_service.get_order_by_code(order_code)

    if not order:
        print("Order not found!")
        return

    print("\n========== INVOICE ==========")
    print(f"Order code: {order['order_code']}")
    print(f"Customer: {order['customer_name']}")
    print(f"Order date: {order['order_date'].strftime('%d/%m/%Y %H:%M:%S')}")

    table = PrettyTable()
    table.field_names = ["Product", "Quantity", "Unit Price", "Subtotal"]

    for item in order["items"]:
        table.add_row([
            item["name"],
            item["quantity"],
            f"{item['unit_price']:,.0f}",
            f"{item['subtotal']:,.0f}"
        ])

    print(table)
    print(f"TOTAL AMOUNT: {order['total_amount']:,.0f}")
    print("=============================")


def display_orders_cli(order_service):
    print("\n===== ORDER LIST =====")

    orders = order_service.get_all_orders()

    if not orders:
        print("No orders found!")
        return

    table = PrettyTable()
    table.field_names = [
        "Order Code", "Customer", "Order Date", "Product Types", "Total Amount"
    ]

    for order in orders:
        table.add_row([
            order["order_code"],
            order["customer_name"],
            order["order_date"].strftime("%d/%m/%Y %H:%M:%S"),
            len(order["items"]),
            f"{order['total_amount']:,.0f}"
        ])

    print(table)


def revenue_statistics_cli(order_service):
    print("\n===== REVENUE STATISTICS =====")

    orders = order_service.get_all_orders()

    if not orders:
        print("No orders found!")
        return

    total_orders = len(orders)
    total_revenue = sum(order["total_amount"] for order in orders)
    average_revenue = total_revenue / total_orders

    monthly_revenue = {}

    for order in orders:
        month = order["order_date"].strftime("%Y-%m")

        if month not in monthly_revenue:
            monthly_revenue[month] = 0

        monthly_revenue[month] += order["total_amount"]

    print(f"Total orders: {total_orders}")
    print(f"Total revenue: {total_revenue:,.0f}")
    print(f"Average order value: {average_revenue:,.0f}")

    table = PrettyTable()
    table.field_names = ["Month", "Revenue"]

    for month, revenue in sorted(monthly_revenue.items()):
        table.add_row([month, f"{revenue:,.0f}"])

    print("\n===== MONTHLY REVENUE =====")
    print(table)


def export_products_cli(product_service):
    print("\n===== EXPORT PRODUCTS TO EXCEL =====")

    products = product_service.get_all_products()

    if not products:
        print("No products found!")
        return

    try:
        file_path = export_products_excel(products)
        print(f"Products exported successfully: {file_path}")
    except Exception as e:
        print(f"Failed to export products: {e}")


def export_orders_cli(order_service):
    print("\n===== EXPORT ORDERS TO EXCEL =====")

    orders = order_service.get_all_orders()

    if not orders:
        print("No orders found!")
        return

    try:
        file_path = export_orders_excel(orders)
        print(f"Orders exported successfully: {file_path}")
    except Exception as e:
        print(f"Failed to export orders: {e}")


def display_menu():
    print("\n========== SALES MANAGEMENT SYSTEM ==========")
    print("1.  Read products from Excel")
    print("2.  Import products to MongoDB")
    print("3.  Display products")
    print("4.  Search products")
    print("5.  Add new product")
    print("6.  Update product price")
    print("7.  Create order")
    print("8.  Display invoice")
    print("9.  Display orders")
    print("10. Revenue statistics")
    print("11. Export products to Excel")
    print("12. Export orders to Excel")
    print("0.  Exit")
    print("=============================================")


def main():
    mongodb = MongoDB()

    try:
        mongodb.check_connection()
        print("Connected to MongoDB successfully!")

        product_collection = mongodb.get_collection("products")
        order_collection = mongodb.get_collection("orders")

        product_service = ProductService(product_collection)
        order_service = OrderService(
            mongodb.client,
            order_collection,
            product_collection
        )

        while True:
            display_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                read_products_excel_cli()
            elif choice == "2":
                import_products_cli(product_service)
            elif choice == "3":
                display_products_cli(product_service)
            elif choice == "4":
                search_products_cli(product_service)
            elif choice == "5":
                add_product_cli(product_service)
            elif choice == "6":
                update_product_price_cli(product_service)
            elif choice == "7":
                create_order_cli(product_service, order_service)
            elif choice == "8":
                display_invoice_cli(order_service)
            elif choice == "9":
                display_orders_cli(order_service)
            elif choice == "10":
                revenue_statistics_cli(order_service)
            elif choice == "11":
                export_products_cli(product_service)
            elif choice == "12":
                export_orders_cli(order_service)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please enter a number from 0 to 12.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        mongodb.close_connection()


if __name__ == "__main__":
    main()
