import numpy as np
import pandas as pd
import pymongo
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN
from sklearn.preprocessing import MinMaxScaler
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

    X = data[features].values.astype(np.float32)
    y = data[target].values.astype(np.float32)

    X = X.reshape(X.shape[0], 1, X.shape[1])
    print(X)

    model = Sequential()
    model.add(SimpleRNN(50, input_shape=(X.shape[1], X.shape[2]), activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X, y, epochs=10, batch_size=32, verbose=1)

    with open("reccurent.pkl", "wb") as f:
        pickle.dump(model, f)


if __name__ == '__main__':
    train()
    print('Model trained!')
