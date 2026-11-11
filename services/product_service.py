from models.product import Product
from services.excel_service import read_products_excel

class ProductService:
    def __init__(self, product_collection):
        self.product_collection = product_collection

    def import_products(self):
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
