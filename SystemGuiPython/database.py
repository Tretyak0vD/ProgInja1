import sqlite3

def initialize_database():
    """Creates and initializes the SQLite database."""
    connection = sqlite3.connect("university.db")
    cursor = connection.cursor()

    # Create the tables if they do not exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS secretary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        student_id TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        experience INTEGER,
        subjects TEXT
    )
    ''')

    # Новая таблица для хранения оценок
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        grade INTEGER NOT NULL,
        FOREIGN KEY(student_id) REFERENCES students(id)
    )
    ''')

    # Insert default secretary if not exists
    cursor.execute('''
    INSERT OR IGNORE INTO secretary (id, username, password)
    VALUES (1, 'abc', 'cba')
    ''')

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
