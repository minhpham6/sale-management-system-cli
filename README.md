# Sales Management System CLI

A command-line application built with Python for managing products, orders, and sales revenue. The application uses MongoDB for data storage and Excel files for importing and exporting data.

## Features

- Import products from Excel files.
- Store and manage products in MongoDB.
- Display and search products.
- Add new products.
- Update product prices.
- Create customer orders.
- Display order invoices.
- View order history.
- Calculate sales revenue statistics.
- Export product data to Excel.
- Export order data to Excel.

## Technologies

- **Python** – Main programming language
- **MongoDB Atlas** – Database
- **PyMongo** – MongoDB integration
- **Pandas** – Data processing
- **OpenPyXL** – Excel file handling
- **PrettyTable** – Console table formatting
- **Python-dotenv** – Environment variable management

## Project Structure

```text
sales_management/
│
├── data/
│   └── products.xlsx
│
├── database/
│   └── mongodb.py
│
├── models/
│   ├── product.py
│   └── order.py
│
├── services/
│   ├── excel_service.py
│   ├── product_service.py
│   └── order_service.py
│
├── exports/
│
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.10 or later
- MongoDB Atlas account or a MongoDB instance
- Git

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/minhpham6/sale-management-system-cli.git
cd sale-management-system-cli
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root directory.

Add your MongoDB connection string:

```env
MONGODB_URI=your_mongodb_connection_string
```

Replace `your_mongodb_connection_string` with your actual MongoDB connection string.

Make sure your IP address is allowed in MongoDB Atlas Network Access.

### 5. Run the application

```bash
python main.py
```

## Usage

After starting the application, the following menu will be displayed:

```text
========== SALES MANAGEMENT SYSTEM ==========
1.  Read products from Excel
2.  Import products to MongoDB
3.  Display products
4.  Search products
5.  Add new product
6.  Update product price
7.  Create order
8.  Display invoice
9.  Display orders
10. Revenue statistics
11. Export products to Excel
12. Export orders to Excel
0.  Exit
=============================================
Enter your choice:
```

Enter the corresponding number to select a function.

## Excel Files

- The source product file is stored in `data/products.xlsx`.
- Exported product and order files are saved in the `exports/` directory.
- Exported Excel files are generated automatically when the corresponding export functions are executed.

## Notes

- MongoDB connection settings must be configured in `.env` before running the application.
- Do not commit your `.env` file or expose your MongoDB credentials.
- The `exports/` directory is used to store generated Excel files.

## License

This project is developed for learning and educational purposes.
