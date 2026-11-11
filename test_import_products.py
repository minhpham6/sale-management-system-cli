
from database.mongodb import MongoDB
from services.product_service import ProductService


mongodb = MongoDB()

try:
    products_collection = mongodb.get_collection("products")

    product_service = ProductService(products_collection)

    result = product_service.import_products()

    print("Import result:")
    print(result)

finally:
    mongodb.close_connection()
