import sqlite3


def vowels(s):
    a = []
    for i in range(len(s)):
        if s[i] in 'ёуеыаоэяию':
            a.append(str(i))
    return ';'.join(a)


def stress(s):
    for i in range(len(s)):
        if s[i].isupper():
            return i


try:
    sqlite_connection = sqlite3.connect('C:\\Documents\\app\\data.db')
    cursor = sqlite_connection.cursor()
    print("База данных создана и успешно подключена к SQLite")
    word = input()
    c = 1
    while word != '0':
        sqlite_insert_query = f"INSERT INTO four (id, word, vowels, stress) VALUES ({c}, '{word.lower()}', '{vowels(word.lower())}', {stress(word)});"
        count = cursor.execute(sqlite_insert_query)
        c += 1
        word = input()
    record = cursor.fetchall()
    print("Версия базы данных SQLite: ", record)
    cursor.execute("SELECT * FROM four")
    print(cursor.fetchall())
    sqlite_connection.commit()
    cursor.close()

except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
finally:
    if sqlite_connection:
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")
