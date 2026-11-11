# from database.mongodb import MongoDB
#
# mongodb = MongoDB()
#
# try:
#     # collection = mongodb.get_collection("products")
#     # # products = collection.find({}).limit(5).sort("unit_price", -1)
#     # # products = collection.find({"product_code": "P1005"})
#     # # products = collection.find({"brand": "Apple"})
#     # keyword = input("Enter product name: ").strip()
#     # if not keyword:
#     #     print("Keyword cannot be empty")
#     # else:
#     #     products = collection.find({
#     #         "name": {"$regex": keyword, "$options": "i"}
#     #     })
#     #     found = False
#     #     for product in products:
#     #         found = True
#     #         print("Product code: ", product["product_code"])
#     #         print("Name: ", product["name"])
#     #         print("Category: ", product["category"])
#     #         print("Brand: ", product["brand"])
#     #         print("Price: ", product["unit_price"])
#     #         print("Stock: ", product["stock"])
#     #         print("-----------------------------\n")
#     #
#     #     if not found:
#     #         print("Product not found")
#
#     product_code = input("Enter product code: ").strip()
#     name = input("Enter product name: ").strip()
#     category = input("Enter product category: ").strip()
#     brand = input("Enter product brand: ").strip()
#     unit = input("Enter product unit: ").strip()
#
#     if not all([product_code, name, category, brand, unit]):
#         raise ValueError("Product information cannot be empty")
#     unit_price = int(input("Enter product unit price: ").strip())
#     stock = int(input("Enter product stock: ").strip())
#
#     if unit_price <= 0:
#         raise ValueError("Unit price must be greater than 0")
#
#     if stock < 0:
#         raise ValueError("Stock cannot be negative")
#
#     product = {
#         "product_code": product_code,
#         "name": name,
#         "category": category,
#         "brand": brand,
#         "unit": unit,
#         "unit_price": unit_price,
#         "stock": stock
#     }
#
#     print("Product information is valid:")
#     print(product)
#
#     collection = mongodb.get_collection("products")
#
#     existing_product = collection.find_one({
#         "product_code": product_code
#     })
#
#     if existing_product:
#         print("Product code already exists")
#     else:
#         print("Product code is available")
# except Exception as e:
#     print(e)
#
# finally:
#     mongodb.close_connection()


from models.product import Product

product = Product(
    "P1001",
    "iPhone 15 Pro Max",
    "Điện thoại",
    "Apple",
    "Chiếc",
    29990000,
    45
)

print(product.name)
print(product.unit_price)

print(product.to_dict())

