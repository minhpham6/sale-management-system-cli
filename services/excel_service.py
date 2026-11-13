from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
EXCEL_FILE_DIR = BASE_DIR / "data" / "products.xlsx"

def read_products_excel():
    df = pd.read_excel(
        EXCEL_FILE_DIR,
        sheet_name="Products",
        engine="openpyxl"
    )

    return df

def export_products_excel(products):
    export_dir = BASE_DIR / "data" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    filepath = export_dir / "products.xlsx"
    df = pd.DataFrame(products)

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    df.to_excel(filepath, index=False, engine="openpyxl")
    return filepath

def export_orders_excel(orders):
    rows = []

    for order in orders:
        for item in order["items"]:
            rows.append({
                "Order Code": order["order_code"],
                "Customer": order["customer_name"],
                "Order Date": order["order_date"],
                "Product Code": item["product_code"],
                "Product Name": item["name"],
                "Quantity": item["quantity"],
                "Unit Price": item["unit_price"],
                "Subtotal": item["subtotal"],
                "Total Amount": order["total_amount"]
            })

    df = pd.DataFrame(rows)

    export_dir = BASE_DIR / "data" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    file_path = export_dir / "orders.xlsx"
    df.to_excel(file_path, index=False, engine="openpyxl")

    return file_path