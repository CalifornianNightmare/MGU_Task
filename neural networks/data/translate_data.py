import sqlite3
from pymongo import MongoClient


def translate_to_mongo():
    conn = sqlite3.connect("air_quality.db")
    cursor = conn.cursor()
    sql_query = "SELECT * FROM tiantan_data"
    cursor.execute(sql_query)

    data = []
    for row in cursor.fetchall():
        data.append(dict(zip([col[0] for col in cursor.description], row)))
        
    conn.close()

    client = MongoClient("mongodb://localhost:27017/")  # Replace with your connection string
    db = client["itmongo"]
    collection = db["air_quality"]
    for item in data:
        collection.insert_one(item)

    client.close()


if __name__ == '__main__':
    translate_to_mongo()
    print('Success!')
