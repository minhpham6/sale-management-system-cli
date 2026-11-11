class Product:
    def __init__(self, product_code, name, category, brand, unit, unit_price, stock):
        self.product_code = product_code
        self.name = name
        self.category = category
        self.brand = brand
        self.unit = unit
        self.unit_price = unit_price
        self.stock = stock

    def to_dict(self):
        return {
            "product_code": self.product_code,
            "name": self.name,
            "category": self.category,
            "brand": self.brand,
            "unit": self.unit,
            "unit_price": self.unit_price,
            "stock": self.stock
        }