import re

from models.product import Product
from services.excel_service import read_products_excel

class ProductService:
    def __init__(self, product_collection):
        self.product_collection = product_collection

    def import_products_mongodb(self):
        df = read_products_excel()

        # Chuyển DataFrame thành danh sách dictionary. Thay các giá trị NaN bằng None
        records = (
            df.astype(object)
            .where(df.notna(), None)
            .to_dict(orient="records")
        )

        # Đảm bảo product_code không bị trùng trong MongoDB
        self.product_collection.create_index(
            "product_code",
            unique=True
        )

        inserted_count = 0
        updated_count = 0
        unchanged_count = 0

        for record in records:
            product = Product(**record)

            result = self.product_collection.update_one(
                {"product_code": product.product_code},
                {"$set": product.to_dict()},
                upsert=True
            )

            if result.upserted_id is not None:
                inserted_count += 1
            elif result.modified_count > 0:
                updated_count += 1
            else:
                unchanged_count += 1

        return {
            "total": len(records),
            "inserted": inserted_count,
            "updated": updated_count,
            "unchanged": unchanged_count
        }

    def get_all_products(self):
        products = self.product_collection.find({})
        return list(products)

    def search_products(self, keyword):
        keyword = keyword.strip()

        if not keyword:
            return []

        escaped_keyword = re.escape(keyword)

        query = {
            "$or": [
                { "product_code": { "$regex": escaped_keyword, "$options": "i" } },
                { "name": { "$regex": escaped_keyword, "$options": "i" } },
                { "brand": { "$regex": escaped_keyword, "$options": "i" } },
                { "category": { "$regex": escaped_keyword, "$options": "i" } },
            ]
        }

        products = self.product_collection.find(query)
        return list(products)

    def is_product_code_exist(self, product_code):
        existing_product = self.product_collection.find_one({
            "product_code": product_code
        })

        return existing_product is not None

    def add_product(self, product):
        if self.is_product_code_exist(product.product_code):
            return False

        self.product_collection.insert_one(product.to_dict())
        return True

    def update_product_price(self, product_code, new_price):
        result = self.product_collection.update_one(
            {"product_code": product_code},
            {"$set": {"unit_price": new_price}}
        )

        return result.matched_count > 0

    def get_product_by_code(self, product_code):
        return self.product_collection.find_one({
            "product_code": product_code
        })
