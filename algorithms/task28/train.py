import numpy as np
import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint


# Загрузка и подготовка данных
def load_and_prepare_data(db_path='data/air_quality.db', time_step=100):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(
        "SELECT * FROM tiantan_data WHERE `PM2.5` IS NOT NULL AND `TEMP` IS NOT NULL AND `PRES` IS NOT NULL AND `DEWP` IS NOT NULL AND `RAIN` IS NOT NULL AND `WSPM` IS NOT NULL",
        conn)
    conn.close()

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler.fit_transform(df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].values)

    X, Y = [], []
    for i in range(len(scaled_features) - time_step - 1):
        a = scaled_features[i:(i + time_step), :]
        X.append(a)
        Y.append(scaled_features[i + time_step, 0])
    return np.array(X), np.array(Y)


time_step = 100
X, y = load_and_prepare_data()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Построение модели
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(time_step, X.shape[2])),
    LSTM(50),
    Dense(25),
    Dense(1)
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mean_squared_error')

# Обучение модели
checkpoint_path = "mymodel/checkpoint.ckpt"
cp_callback = ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

model.fit(X_train, y_train, epochs=50, batch_size=64, validation_data=(X_test, y_test), callbacks=[cp_callback])

# Сохранение модели
model.save('mymodel/my_rnn_model')

print("Модель успешно обучена и сохранена.")
