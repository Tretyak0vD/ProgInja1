import sqlite3


class SecretaryController:
    @staticmethod
    def authenticate(username, password):
        """Authenticates the secretary with provided username and password."""
        connection = sqlite3.connect("university.db")
        cursor = connection.cursor()

        cursor.execute('''
        SELECT * FROM secretary WHERE username = ? AND password = ?
        ''', (username, password))
        result = cursor.fetchone()

        connection.close()
        return result is not None


class StudentController:
    @staticmethod
    def get_students():
        """Fetches all students from the database."""
        connection = sqlite3.connect("university.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id, full_name grades FROM students')
        students = cursor.fetchall()

        connection.close()
        return students

    @staticmethod
    def get_student_details(student_id):
        connection = sqlite3.connect("university.db")
        cursor = connection.cursor()

        # Извлекаем основные данные о студенте
        cursor.execute('''
        SELECT id, full_name, student_id FROM students WHERE id = ?
        ''', (student_id,))
        student = cursor.fetchone()

        if not student:
            connection.close()
            return None  # Если студент не найден, возвращаем None

        # Извлекаем оценки из таблицы grades
        cursor.execute('''
        SELECT subject, grade FROM grades WHERE student_id = ?
        ''', (student_id,))
        grades = cursor.fetchall()

        # Формируем данные: student + оценки
        student_details = {
            "id": student[0],
            "full_name": student[1],
            "student_id": student[2],
            "grades": {subject: grade for subject, grade in grades}  # Преобразуем в словарь
        }

        connection.close()
        return student_details


class ProfessorController:
    @staticmethod
    def get_professors():
        """Fetches all professors from the database."""
        connection = sqlite3.connect("university.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id, full_name, experience, subjects FROM professors')
        professors = cursor.fetchall()

        connection.close()
        return professors

    @staticmethod
    def get_professor_details(professor_id):
        """Fetches detailed information for a specific professor."""
        connection = sqlite3.connect("university.db")
        cursor = connection.cursor()

        cursor.execute('SELECT full_name, experience, subjects FROM professors WHERE id = ?', (professor_id,))
        professor = cursor.fetchone()

        connection.close()
        return professor
