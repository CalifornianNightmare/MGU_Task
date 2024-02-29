import pymongo
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pickle


def train():
    client = pymongo.MongoClient("localhost:27017")
    db = client["itmongo"]
    collection = db["air_quality"]
    data = pd.DataFrame(collection.find())
    data.drop("_id", axis=1, inplace=True)
    data = data.iloc[:-50]
    data.dropna(inplace=True)

    features = [col for col in data.columns if pd.api.types.is_numeric_dtype(data[col])]
    target = "CO"

    X_train, X_test, y_train, y_test = train_test_split(data[features], data[target], test_size=0.2)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    pipe = Pipeline([
        ("poly", PolynomialFeatures(degree=2)),
        ("linear", LinearRegression())
    ])

    pipe.fit(X_train_scaled, y_train)

    with open("polinomial.pkl", "wb") as f:
        pickle.dump(pipe, f)


if __name__ == '__main__':
    train()
    print('Model trained!')
