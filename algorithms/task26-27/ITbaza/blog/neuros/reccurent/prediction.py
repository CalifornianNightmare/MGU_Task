import numpy as np
import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from datetime import datetime, timedelta

# Загрузка модели
model = tf.keras.models.load_model('mymodel/my_rnn_model')


# Функция для запроса параметров прогноза
def get_forecast_parameters():
    start_date_str = input("Введите дату начала прогноза (например, 2021-03-01 19:00): ")
    forecast_hours = int(input("Сколько часов предсказать после этой даты? "))
    return start_date_str, forecast_hours


# Функция для загрузки и подготовки данных
def load_and_prepare_data(start_date_str, db_path='air_quality.db', time_step=100):
    start_date = pd.to_datetime(start_date_str)
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM tiantan_data WHERE date <= ? ORDER BY date DESC LIMIT ?", conn,
                           params=(start_date_str, time_step))
    conn.close()
    if df.empty:
        raise ValueError("Нет доступных данных для указанной даты.")
    return df


# Функция для выполнения прогноза
def predict_hours_ahead(model, df, forecast_hours, time_step=100):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_features = scaler.fit_transform(df[['PM2.5', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']])
    X_last = scaled_features[-time_step:].reshape(1, time_step, 6)

    predictions = []
    for _ in range(forecast_hours):
        pred = model.predict(X_last)[0][0]
        predictions.append([pred])
        X_last = np.roll(X_last, -1, axis=1)
        X_last[0, -1, :] = np.append(pred, X_last[0, -2, 1:])

    predictions_scaled = scaler.inverse_transform(np.hstack([predictions, np.zeros((len(predictions), 5))]))[:, 0]
    return predictions_scaled

def predict(start_date_str, forecast_hours):
    time_step = 100
    try:
        df = load_and_prepare_data(start_date_str, 'air_quality.db', time_step)
        predictions = predict_hours_ahead(model, df, forecast_hours, time_step)

        return predictions
    except ValueError as e:
        print(e)


if __name__ == '__main__':
    start_date_str = input("Введите дату начала прогноза (например, 2021-03-01 19:00): ")
    forecast_hours = int(input("Сколько часов предсказать после этой даты? "))

    predictions = predict(start_date_str, forecast_hours)

    start_date = pd.to_datetime(start_date_str)
    print("Прогнозируемый уровень PM2.5:")
    db_path = 'air_quality.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Создаем таблицу, если ее еще нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS forecasts (
            timestamp TEXT PRIMARY KEY,
            pm25_level REAL
        )
    ''')

    # Вставляем прогнозы в таблицу
    for i, pred in enumerate(predictions):
        timestamp = (start_date + timedelta(hours=i + 1)).strftime('%Y-%m-%d %H:%M')
        cursor.execute('INSERT INTO forecasts (timestamp, pm25_level) VALUES (?, ?)', (timestamp, pred))

    # Сохраняем изменения и закрываем соединение
    conn.commit()
    conn.close()
