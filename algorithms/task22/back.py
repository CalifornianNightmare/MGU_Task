import pymysql
import pandas as pd
from math import pi

from keys import HOST, ENGINE, DB_NAME, EXCEL_NAME, TABLE_NAME, PASSWORD, USERNAME, PORT


class Connection:
    connection = None

    def __init__(self, recreate=True):
        con = pymysql.connect(host=HOST, port=PORT, user=USERNAME, password=PASSWORD, database=DB_NAME)
        self.connection = con
        if recreate:
            self.recreate_db()

    def get_connection(self):
        return self.connection

    def recreate_db(self, db_name=DB_NAME):
        with self.connection.cursor() as cursor:
            sel = f'CREATE DATABASE IF NOT EXISTS {db_name};'
            cursor.execute(sel)
            self.connection.commit()

    def check_for_table(self):
        with self.connection.cursor() as cursor:
            sel = f"""SHOW TABLES LIKE '{TABLE_NAME}'"""
            cursor.execute(sel)
            result = cursor.fetchall()
            return bool(result)

    def trunkate_table(self):
        with self.connection.cursor() as cursor:
            sel = f"""TRUNCATE {DB_NAME}.{TABLE_NAME}"""
            cursor.execute(sel)
            self.connection.commit()

    def drop_db(self):
        with self.connection.cursor() as cursor:
            sel = f"""DROP DATABASE {DB_NAME}"""
            cursor.execute(sel)
            self.connection.commit()

    def execute(self, sel):
        with self.connection.cursor() as cursor:
            cursor.execute(sel)
            self.connection.commit()


class PandasConnection:

    @staticmethod
    def to_excel(sel, index_col=None):
        dp = pd.read_sql(sel, con=ENGINE, index_col=index_col)
        dp.to_excel(EXCEL_NAME)

    @staticmethod
    def from_excel(index_col=None):
        dp = pd.read_excel(EXCEL_NAME, index_col=index_col)
        return dp

    @staticmethod
    def read_df(index_col=None):
        df = pd.read_sql(f"""SELECT * FROM {DB_NAME}.{TABLE_NAME} LIMIT 100;""", con=ENGINE, index_col=index_col)
        return df

    @staticmethod
    def show_dbs():
        df = pd.read_sql(f"""SHOW DATABASES""", con=ENGINE)
        return df

    @staticmethod
    def show_tables():
        df = pd.read_sql(f"""SHOW TABLES""", con=ENGINE)
        return df


class myFunctions():
    @staticmethod
    def radians_to_degrees():
        df = PandasConnection.read_df()
        df['angle'] = df['radians'] * (180/pi)
        df.to_sql(name=TABLE_NAME, if_exists='replace', con=ENGINE, index=False)


def main():
    connection = Connection()

    exit_loop = False
    while not exit_loop:
        print('Выберите пункт:\n'
              '\tСоздать базу данных: 1\n'
              '\tСоздать таблицу: 2\n'
              '\tВыйти: 0\n'
              '\tОчистить таблицу: #1\n'
              '\tУдалить БД: #2')
        menu_input = input('Пункт: ')
        print('\n')

        if menu_input == '1':
            connection.recreate_db()
        elif menu_input == '2':
            # connection.create_table('')
            pass
        elif menu_input == '0':
            exit_loop = True
        elif menu_input == '#1':
            connection.trunkate_table()
        elif menu_input == '#2':
            connection.drop_db()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Something went wrong...\n')
        print(e)
