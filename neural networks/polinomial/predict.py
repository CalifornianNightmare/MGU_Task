import pickle
import pandas as pd
import pymongo


def predict():
    with open("polinomial.pkl", "rb") as f:
        model = pickle.load(f)

    client = pymongo.MongoClient("localhost:27017")
    db = client["itmongo"]
    collection = db["air_quality"]
    data = pd.DataFrame(collection.find())
    data.drop("_id", axis=1, inplace=True)
    data = data.iloc[-50:]
    data.dropna(inplace=True)

    numerical_columns = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
    X = data[numerical_columns]

    new_predictions = list(model.predict(X))

    return new_predictions


def list_to_mongo(list_of_values):
    client = pymongo.MongoClient("localhost:27017")
    db = client["itmongo"]
    collection = db["air_quality_result"]

    document_count = collection.count_documents({})
    if document_count == 0:
        collection.insert_one({"data": list_of_values})

    collection.update_one({}, {"$set": {"data": list_of_values}})
    client.close()


def read_mongo():
    client = pymongo.MongoClient("localhost:27017")
    db = client["itmongo"]
    collection = db["air_quality_result"]
    cursor = collection.find({})
    data_list = list(cursor)[0]['data']
    client.close()

    return data_list


if __name__ == '__main__':
    prediction = predict()
    list_to_mongo(prediction)

    print(read_mongo())
