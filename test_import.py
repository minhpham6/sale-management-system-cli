from services.excel_service import read_products_excel
from database.mongodb import MongoDB

mongodb = MongoDB()

try:
    collection = mongodb.get_collection("products")
    collection.create_index("product_code", unique=True)
    products = read_products_excel().to_dict(orient='records')

    for product in products:
        result = collection.update_one(
            {"product_code": product["product_code"]},
            {"$set": product},
            upsert=True
        )
        print(result)

    print("Imported products")
finally:
    mongodb.close_connection()