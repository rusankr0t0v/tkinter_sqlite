import os
import sqlite3
from tkinter import *
from tkinter import ttk



def create_db(database):
    #функция создает таблицу person в БД и записывает тестовые данные
    conn = sqlite3.connect(database)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS person(
                id integer primary key autoincrement not null,
                name text,
                surname text,
                birth_date date);""")

    demo_data = [{'name': 'Руслан', 'surname': 'Кротов', 'birth_date': '1993-09-04'},
                 {'name': 'Олег', 'surname': 'Петров', 'birth_date': '1994-11-09'},
                 {'name': 'Иван', 'surname': 'Иванов', 'birth_date': '2001-01-26'},
                 {'name': 'Петр', 'surname': 'Синицын', 'birth_date': '1986-07-14'}]

    demo_data_arr = []
    for i in demo_data:
        demo_data_arr.append((i['name'], i['surname'], i['birth_date']))

    cur.executemany("""INSERT INTO person(name, surname, birth_date)
                    VALUES(?,?,?);""", demo_data_arr)
    conn.commit()
    conn.close()


def read_db():
    data = []
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("""SELECT name, surname, FLOOR((julianday(DATE('now')) - julianday(birth_date))/365) 
                    as age FROM person;""")
    for row in cur.fetchall():
        data.append(row)
    return(data)



if __name__ == '__main__':
    root = Tk()
    root.title("Tkinter & SQLite")
    root.geometry("600x400")

    database = 'people.db'
    #проверка существования БД
    #при необходимости создание
    if os.path.exists(database):
        print('БД существует!')
        label = ttk.Label(text="База данных существует!")
        label.pack()
    else:
        label = ttk.Label(text="База данных отсутствовала! Она была создана и заполнена тестовыми данными")
        label.pack()
        create_db(database)

    # определяем столбцы
    columns = ("name", "surname", "ege")

    tree = ttk.Treeview(columns=columns, show="headings")
    tree.pack(fill=BOTH, expand=1)

    # определяем заголовки
    tree.heading("name", text="Имя")
    tree.heading("surname", text="Фамилия")
    tree.heading("ege", text="Возраст")

    data = read_db()
    # добавляем данные
    for person in data:
        tree.insert("", END, values=person)

    root.mainloop()
