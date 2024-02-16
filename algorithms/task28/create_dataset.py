import pandas as pd
import sqlite3

# Чтение данных
df = pd.read_csv('data/PRSA_Data_Tiantan_20130301-20170228.csv')

# Предварительная обработка и очистка данных
# Удаление строк с недостающими значениями
df.dropna(subset=['PM2.5'], inplace=True)

# Конвертация столбца 'date' в формат datetime, если он есть
if 'date' not in df.columns:
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

# Сохранение в SQLite базу данных
conn = sqlite3.connect('data/air_quality.db')
df.to_sql('tiantan_data', conn, if_exists='replace', index=False)
conn.close()

print('Датасет успешно подготовлен и сохранен в базу данных.')
