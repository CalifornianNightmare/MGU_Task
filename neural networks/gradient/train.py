import pymongo
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import pickle


def train():
    client = pymongo.MongoClient("localhost:27017")
    db = client["itmongo"]
    collection = db["air_quality"]
    data = pd.DataFrame(collection.find())
    data.drop("_id", axis=1, inplace=True)
    data = data.iloc[:-50]
    data.dropna(inplace=True)

    numerical_columns = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
    X = data[numerical_columns]
    y = data["CO"]

    model = GradientBoostingRegressor()
    model.fit(X, y)
    with open("gradient.pkl", "wb") as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    train()
    print('Model trained!')

