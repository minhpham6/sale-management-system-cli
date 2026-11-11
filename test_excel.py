from services.excel_service import read_products_excel

df = read_products_excel()

products = df.to_dict(orient="records")

print(type(products))
print(type(products[0]))
print(len(products))