import sqlite3

from excel import first_grades, second_grades
def init_db():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
user_id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
grade TEXT NOT NULL
)
''')
    connection.commit()
    connection.close()

def add_or_change(user_id: int, username: str, grade: str):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('INSERT OR REPLACE INTO Users (user_id, username, grade) VALUES (?, ?, ?)', (user_id, username, grade))
    connection.commit()
    connection.close()

def get_user_grade_by_id(user_id):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT grade FROM Users WHERE user_id == ?', (user_id,))
    results = cursor.fetchall()
    print(results)

    connection.close()

def get_list_ids_by_grade(grade):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_id FROM Users WHERE grade == ?', (grade,))
    results = cursor.fetchall()
    connection.close()
    return results


def get_user_grade_from_db(user_id):
    conn = sqlite3.connect('my_database.db') 
    cursor = conn.cursor()
    cursor.execute("SELECT grade FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return result[0]  # Возвращает строку, например "9А"
    return None


def print_db():
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT user_id, username, grade FROM Users WHERE user_id != ?', ('',))
    results = cursor.fetchall()
    print(results)
    connection.close()

def delete_all_users():
    with sqlite3.connect('my_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Users')
        conn.commit()
        print("База данных очищена!")