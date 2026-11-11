from services.excel_service import read_products_excel

df = read_products_excel()

print(df.head().to_dict())
print(df.shape)
print(df.columns)
print(df.dtypes)