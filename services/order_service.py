from models.order import Order

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



"""
{
    "order_code": "ORD001",
    "customer_name": "Nguyen Van A",
    "order_date": datetime.now(),
    "items": [
        {
            "product_code": "P1001",
            "name": "iPhone 15",
            "quantity": 2,
            "unit_price": 10000000,
            "subtotal": 20000000
        }
    ],
    "total_amount": 20000000
}
"""
