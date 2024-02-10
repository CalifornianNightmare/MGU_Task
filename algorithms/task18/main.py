import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from back import Connection, PandasConnection

def main():

    root = tk.Tk()
    root.geometry('360x140')
    root.resizable = False
    root.maxsize(360, 140)
    root.minsize(260, 130)
    connection = Connection()
    root.title("Мебельная база данных")

    texts = ['Создать базу данных', 'Создать таблицу', 'Ввести данные', 'Вывести данные', 'Экспорт в Excel']
    commands = [lambda: (db_name_window(root, connection)),
                lambda: (table_window(root, connection)),
                lambda: (insert_window(root, connection)),
                lambda: (display_dataframe_table(PandasConnection.read_df())),
                lambda: (PandasConnection.to_excel('''SELECT ID as 'id', delivery_date as 'Дата доставки', department as 'Отдел', type as 'Тип мебели', price as 'Цена' FROM task18.main;'''), messagebox.showinfo(title='Инфо', message='Успешно сохранено в Excel!'))]

    for button_text, command in zip(texts, commands):
        create_database_btn = tk.Button(root, text=button_text, command=command)
        create_database_btn.pack()

    root.mainloop()

def display_dataframe_table(df):

    '''Opens a window with a table made from a pandas dataframe'''

    root = tk.Tk()
    root.title("Таблица")

    tree = ttk.Treeview(root, columns=list(df.columns), show="headings")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True)

    root.mainloop()


def table_window(root, connection):
    table_window = tk.Toplevel(root)
    table_window.title("Ввод данных")

    table_window.maxsize(360, 100)
    table_window.minsize(260, 70)

    tk.Label(table_window, text='Введите имя таблицы').pack()
    entry = tk.Entry(table_window)
    entry.insert(0, "main")
    entry.pack()

    insert_btn = tk.Button(table_window, text="Выбрать имя", command=lambda: (connection.execute(f'''CREATE TABLE IF NOT EXISTS `task18`.{entry.get()} (`ID` INT UNSIGNED NOT NULL AUTO_INCREMENT,`delivery_date` DATETIME NULL,`department` VARCHAR(45) NULL,`type` VARCHAR(45) NULL,`price` VARCHAR(45) NULL,PRIMARY KEY (`ID`));'''), table_window.destroy(), messagebox.showinfo(title='Инфо', message='Успешно создана таблица!'), display_dataframe_table(PandasConnection.show_tables())))
    insert_btn.pack()


def db_name_window(root, connection):

    db_name_window = tk.Toplevel(root)
    db_name_window.title("Ввод данных")

    db_name_window.maxsize(360, 100)
    db_name_window.minsize(260, 70)

    tk.Label(db_name_window, text='Введите имя БД').pack()
    entry = tk.Entry(db_name_window)
    entry.insert(0, "task18")
    entry.pack()

    insert_btn = tk.Button(db_name_window, text="Выбрать имя", command=lambda: (connection.recreate_db(db_name=entry.get()), db_name_window.destroy(), messagebox.showinfo(title='Инфо', message='Успешно создана база данных!'), display_dataframe_table(PandasConnection.show_dbs())))
    insert_btn.pack()


def insert_window(root, connection):

    insert_window = tk.Toplevel(root)
    insert_window.title("Ввод данных")

    insert_window.maxsize(360, 280)
    insert_window.minsize(260, 220)

    texts = ['Дата ввоза мебели:', 'Отдел:', 'Вид мебели:', 'Цена мебели:']
    buttons = []
    for text in texts:
        tk.Label(insert_window, text=text).pack()
        entry = tk.Entry(insert_window)
        entry.pack()
        buttons.append(entry)

    insert_btn = tk.Button(insert_window, text="Добавить данные", command=lambda: (connection.execute(f'''INSERT INTO `task18`.`main` (`delivery_date`, `department`, `type`, `price`) VALUES ('{buttons[0].get()}', '{buttons[1].get()}', '{buttons[2].get()}', '{buttons[3].get()}');'''), insert_window.destroy()))
    insert_btn.pack()


if __name__ == '__main__':
    main()
