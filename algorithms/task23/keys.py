from sqlalchemy import create_engine

HOST = '127.127.127.3'
USERNAME = 'root'
PASSWORD = 'rootroot'
DB_NAME = 'task23'
TABLE_NAME = 'main'
EXCEL_NAME = 'output.xlsx'
ENGINE = create_engine(f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}")
PORT = 3306
