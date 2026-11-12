from datetime import datetime

class Order:
    def __init__(self, order_code, customer_name, items, total_amount):
        self.order_code = order_code
        self.customer_name = customer_name
        self.order_date = datetime.now()
        self.items = items
        self.total_amount = total_amount

    def to_dict(self):
        return {
            "order_code": self.order_code,
            "customer_name": self.customer_name,
            "order_date": self.order_date,
            "items": self.items,
            "total_amount": self.total_amount
        }
