import sqlite3

def table_exists(cursor, table_name):
    """Checks if a table exists in the database."""
    cursor.execute('''
    SELECT name FROM sqlite_master WHERE type='table' AND name=?
    ''', (table_name,))
    return cursor.fetchone() is not None

def seed_database():
    """Populates the database with test data for students, professors, and secretaries."""
    connection = sqlite3.connect("university.db")
    cursor = connection.cursor()

    # Check if tables exist
    if not table_exists(cursor, "students") or not table_exists(cursor, "grades"):
        print("Tables 'students' or 'grades' do not exist. Please initialize the database first.")
        connection.close()
        return

    if not table_exists(cursor, "professors"):
        print("Table 'professors' does not exist. Please initialize the database first.")
        connection.close()
        return

    # Clear old data
    cursor.execute('DELETE FROM students')
    cursor.execute('DELETE FROM professors')
    cursor.execute('DELETE FROM grades')

    # Insert test data for students
    students = [
        ("Иван Иванов", "S12345"),
        ("Мария Смирнова", "S23456"),
        ("Алексей Кузнецов", "S34567"),
    ]
    cursor.executemany('''
    INSERT INTO students (full_name, student_id)
    VALUES (?, ?)
    ''', students)

    # Get inserted students' IDs
    cursor.execute('SELECT id FROM students WHERE student_id = "S12345"')
    student1_id = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM students WHERE student_id = "S23456"')
    student2_id = cursor.fetchone()[0]
    cursor.execute('SELECT id FROM students WHERE student_id = "S34567"')
    student3_id = cursor.fetchone()[0]

    # Insert test grades for students
    grades = [
        (student1_id, "Математика", 5),
        (student1_id, "Физика", 4),
        (student1_id, "Химия", 5),
        (student2_id, "Математика", 4),
        (student2_id, "Физика", 3),
        (student2_id, "Химия", 4),
        (student3_id, "Математика", 5),
        (student3_id, "Физика", 5),
        (student3_id, "Химия", 5),
    ]
    cursor.executemany('''
    INSERT INTO grades (student_id, subject, grade)
    VALUES (?, ?, ?)
    ''', grades)

    # Insert test data for professors
    professors = [
        ("Дмитрий Петров", 10, "Математика, Физика"),
        ("Екатерина Соколова", 15, "Химия, Биология"),
        ("Анна Тихонова", 8, "Информатика"),
    ]
    cursor.executemany('''
    INSERT INTO professors (full_name, experience, subjects)
    VALUES (?, ?, ?)
    ''', professors)

    connection.commit()
    connection.close()
    print("База данных заполнена тестовыми данными.")


def verify_data():
    """Verifies if data has been inserted successfully."""
    connection = sqlite3.connect("university.db")
    cursor = connection.cursor()

    print("\nСтуденты:")
    if table_exists(cursor, "students"):
        cursor.execute('SELECT * FROM students')
        for row in cursor.fetchall():
            print(row)
    else:
        print("Table 'students' does not exist.")

    print("\nОценки:")
    if table_exists(cursor, "grades"):
        cursor.execute('SELECT * FROM grades')
        for row in cursor.fetchall():
            print(row)
    else:
        print("Table 'secretaries' does not exist.")

    print("\nПреподаватели:")
    if table_exists(cursor, "professors"):
        cursor.execute('SELECT * FROM professors')
        for row in cursor.fetchall():
            print(row)
    else:
        print("Table 'professors' does not exist.")

    print("\nСекретари:")
    if table_exists(cursor, "secretary"):
        cursor.execute('SELECT * FROM secretary')
        for row in cursor.fetchall():
            print(row)
    else:
        print("Table 'secretaries' does not exist.")



    connection.close()

if __name__ == "__main__":
    seed_database()
    verify_data()
