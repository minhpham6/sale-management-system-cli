import pymongo


class OrderService:
    def __init__(self, client, order_collection, product_collection):
        self.client = client
        self.order_collection = order_collection
        self.product_collection = product_collection

    def create_order(self, order):
        with self.client.start_session() as session:
            with session.start_transaction():
                for item in order.items:
                    result = self.product_collection.update_one(
                        {
                            "product_code": item["product_code"],
                            "stock": {"$gte": item["quantity"]}
                        },
                        {
                            "$inc": {"stock": -item["quantity"]}
                        },
                        session=session
                    )

                    if result.matched_count == 0:
                        raise ValueError("Product not found or insufficient stock")

                self.order_collection.insert_one(
                    order.to_dict(),
                    session=session
                )

        return True

    def get_order_by_code(self, order_code):
        return self.order_collection.find_one({
            "order_code": order_code
        })

    def get_all_orders(self):
        return self.order_collection.find({}).sort("order_date", pymongo.DESCENDING)