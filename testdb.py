from database.mongodb import MongoDB

mongodb = MongoDB()

try:
    if mongodb.check_connection():
        print("Connected")

finally:
    mongodb.close_connection()
