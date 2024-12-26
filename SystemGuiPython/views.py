import tkinter as tk
from tkinter import messagebox, ttk
from controllers import SecretaryController, StudentController, ProfessorController


class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Добро пожаловать!")
        self.root.geometry("300x200")

        self.username_label = tk.Label(root, text="Имя пользователя:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(root, text="Пароль:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(root, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if SecretaryController.authenticate(username, password):
            messagebox.showinfo("Вход выполнен", "Добро пожаловать!")
            self.root.destroy()
            show_main_view()
        else:
            messagebox.showerror("Ошибка входа", "Неверные учетные данные!")


class MainView:
    def __init__(self, root):
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x300")

        self.student_button = tk.Button(root, text="Студенты", command=self.show_students)
        self.student_button.pack(pady=10)

        self.professor_button = tk.Button(root, text="Преподаватели", command=self.show_professors)
        self.professor_button.pack(pady=10)

    def show_students(self):
        StudentListView(self.root)

    def show_professors(self):
        ProfessorListView(self.root)


class StudentListView:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Список студентов")
        self.window.geometry("500x400")

        # Отображаем только ID и Имя
        self.tree = ttk.Treeview(self.window, columns=("ID", "Имя"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Имя", text="Полное имя")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Обработка двойного клика
        self.tree.bind("<Double-1>", self.show_student_details)

        self.load_students()

    def load_students(self):
        # Загружаем только ID и имя
        students = StudentController.get_students()  # students: [(id, full_name, student_id, grades)]
        for student in students:
            self.tree.insert("", tk.END, values=(student[0], student[1]))  # Только ID и имя

    def show_student_details(self, event):
        selected_item = self.tree.selection()[0]
        student_id = self.tree.item(selected_item, "values")[0]
        student_details = StudentController.get_student_details(student_id)
        StudentDetailView(self.window, student_details)


class ProfessorListView:
    def __init__(self, root):
        self.window = tk.Toplevel(root)
        self.window.title("Список преподавателей")
        self.window.geometry("500x400")

        # Отображаем только ID и Имя
        self.tree = ttk.Treeview(self.window, columns=("ID", "Имя"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Имя", text="Полное имя")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Обработка двойного клика
        self.tree.bind("<Double-1>", self.show_professor_details)

        self.load_professors()

    def load_professors(self):
        # Загружаем только ID и имя
        professors = ProfessorController.get_professors()  # professors: [(id, full_name, experience, subjects)]
        for professor in professors:
            self.tree.insert("", tk.END, values=(professor[0], professor[1]))  # Только ID и имя

    def show_professor_details(self, event):
        selected_item = self.tree.selection()[0]
        professor_id = self.tree.item(selected_item, "values")[0]
        professor_details = ProfessorController.get_professor_details(professor_id)
        ProfessorDetailView(self.window, professor_details)


class StudentDetailView:
    def __init__(self, root, student_details):
        self.window = tk.Toplevel(root)
        self.window.title("Детали студента")
        self.window.geometry("400x300")

        # Извлекаем данные из student_details, которое теперь является словарем
        student_name = student_details["full_name"]
        student_id = student_details["student_id"]
        grades = student_details["grades"]

        # Формируем информацию об оценках
        grades_text = "Оценки:\n" + "\n".join([f"{subject}: {grade}" for subject, grade in grades.items()])

        # Отображаем данные на экране
        self.name_label = tk.Label(self.window, text=f"Имя: {student_name}")
        self.name_label.pack(pady=5)
        self.student_id_label = tk.Label(self.window, text=f"ID студента: {student_id}")
        self.student_id_label.pack(pady=5)
        self.grades_label = tk.Label(self.window, text=grades_text)
        self.grades_label.pack(pady=5)


class ProfessorDetailView:
    def __init__(self, root, professor_details):
        self.window = tk.Toplevel(root)
        self.window.title("Детали преподавателя")
        self.window.geometry("400x300")

        professor_name, experience, subjects = professor_details
        subject_info = f"Предметы: {subjects}"

        self.name_label = tk.Label(self.window, text=f"Имя: {professor_name}")
        self.name_label.pack(pady=5)
        self.experience_label = tk.Label(self.window, text=f"Опыт работы: {experience} лет")
        self.experience_label.pack(pady=5)
        self.subjects_label = tk.Label(self.window, text=subject_info)
        self.subjects_label.pack(pady=5)


def show_main_view():
    main_window = tk.Tk()
    MainView(main_window)
    main_window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    LoginView(root)
    root.mainloop()
