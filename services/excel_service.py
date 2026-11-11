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