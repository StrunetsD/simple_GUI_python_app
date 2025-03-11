import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from views.table_tree_view import TableView, TreeView
from dialog_view import *
from views.pagination import Pagination
from controllers.controllers import Controller

class StartWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Выбор режима работы")
        self.geometry("600x400")

        ttk.Label(self, text="Выберите источник данных:").pack(pady=10)

        ttk.Button(self, text="База данных",
                   command=lambda: self.start_app("db")).pack(pady=5)

        ttk.Button(self, text="XML файлы",
                   command=lambda: self.start_app("xml")).pack(pady=5)

    def start_app(self, mode):
        self.destroy()
        app = MainWindow(mode)
        app.mainloop()

class MainWindow(tk.Tk):
    def __init__(self, mode):
        super().__init__()
        self.title("Студенты")
        self.geometry("600x400")
        self.mode = mode
        self.controller = Controller(mode)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.table_view = TableView(self)
        self.tree_view = TreeView(self)

        self.table_tab = ttk.Frame(self.notebook)
        self.tree_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.table_tab, text="Таблица")
        self.notebook.add(self.tree_tab, text="Дерево")

        self.table_view.pack(fill=tk.BOTH, expand=True, in_=self.table_tab)
        self.tree_view.pack(fill=tk.BOTH, expand=True, in_=self.tree_tab)

        ttk.Label(self, text=f"Режим работы: {mode.upper()}").pack(side=tk.TOP, pady=5)

        self.data = []
        self.pagination = Pagination(len(self.data))

        controls = self.create_controls(self, self.pagination, self.update_table)
        self.status_label = controls["status_label"]

        self.update_table()
        self.update_status_label(self.pagination, self.status_label)

        self.create_menu()

    def _format_data_xml(self, raw_data):
        formatted_data = []
        for student in raw_data:
            row = [
                student.fio,
                student.father_fio,
                student.father_income,
                student.mother_fio,
                student.mother_income,
                student.brother_count,
                student.sister_count
            ]
            formatted_data.append(row)
        return formatted_data

    def load_data(self):
        try:
            self.data = self.controller.get_students()
            self.pagination.update_total(len(self.data))

            if self.pagination.current_page > self.pagination.total_pages:
                self.pagination.current_page = self.pagination.total_pages
            elif self.pagination.current_page < 1:
                self.pagination.current_page = 1

            self.update_table()
            self.update_status_label(self.pagination, self.status_label)
        except Exception:
            messagebox.showerror("Ошибка", "Не удалось обновить данные")

    def update_table(self):
        try:
            current_data = self.pagination.get_current_page_data(self.data)
            self.table_view.clear_data()
            if self.mode == "xml":
                formatted_data = self._format_data_xml(current_data)
                self.table_view.insert_data(formatted_data)
                self.tree_view.clear_data()
                self.tree_view.insert_data(formatted_data)
            else:
                self.table_view.insert_data(current_data)
                self.tree_view.clear_data()
                self.tree_view.insert_data(current_data)
        except Exception:
            messagebox.showerror("Ошибка", "Не удалось обновить таблицу")

    def previous_page(self):
        try:
            self.pagination.previous_page()
            self.update_table()
            self.update_status_label(self.pagination, self.status_label)
        except Exception:
            messagebox.showerror("Ошибка", "Не удалось перейти на предыдущую страницу")

    def next_page(self):
        try:
            self.pagination.next_page()
            self.update_table()
            self.update_status_label(self.pagination, self.status_label)
        except Exception:
            messagebox.showerror("Ошибка", "Не удалось перейти на следующую страницу")

    def count(self):
        try:
            deleted_count, found_count = self.controller.get_counts()
            messagebox.showinfo("Статистика", f"Удалено записей: {deleted_count}\nНайдено записей: {found_count}")
        except Exception:
            messagebox.showerror("Ошибка", "Не удалось получить статистику")

    def load_students_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if file_path:
            try:
                self.data = self.controller.get_students(file_path)
                self.pagination.update_total(len(self.data))
                self.update_table()
                messagebox.showinfo("Успех", "Данные загружены!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        if self.mode == "xml":
            file_menu.add_command(label="Выгрузка из файла", command=self.load_students_from_file)
            file_menu.add_command(label="Поиск студента по имени", command=self.open_search_student_dialog)
            file_menu.add_command(label="Поиск родителя по имени", command=self.open_search_parent_dialog)
            file_menu.add_command(label="Поиск по братьям/сестрам", command=self.open_siblings_search_dialog)
            file_menu.add_command(label="Поиск по доходу", command=self.open_income_search_dialog)
            file_menu.add_separator()
            file_menu.add_command(label="Удалить студента по имени", command=self.open_delete_student_dialog)
            file_menu.add_command(label="Удалить по братьям/сестрам", command=self.open_delete_siblings_dialog)
            file_menu.add_command(label="Удалить по доходу", command=self.open_delete_income_dialog)
            file_menu.add_command(label="Добавить студента", command=self.open_add_student_dialog)
            file_menu.add_command(label="Обновить данные", command=self.load_data)
            file_menu.add_command(label="Статистика", command=self.count)
            menubar.add_cascade(label="Операции", menu=file_menu)
        else:
            file_menu.add_command(label="Поиск студента по имени", command=self.open_search_student_dialog)
            file_menu.add_command(label="Поиск родителя по имени", command=self.open_search_parent_dialog)
            file_menu.add_command(label="Поиск по братьям/сестрам", command=self.open_siblings_search_dialog)
            file_menu.add_command(label="Поиск по доходу", command=self.open_income_search_dialog)
            file_menu.add_separator()
            file_menu.add_command(label="Удалить студента по имени", command=self.open_delete_student_dialog)
            file_menu.add_command(label="Удалить по братьям/сестрам", command=self.open_delete_siblings_dialog)
            file_menu.add_command(label="Удалить по доходу", command=self.open_delete_income_dialog)
            file_menu.add_command(label="Добавить студента", command=self.open_add_student_dialog)
            file_menu.add_command(label="Обновить данные", command=self.load_data)
            file_menu.add_command(label="Статистика", command=self.count)
            menubar.add_cascade(label="Операции", menu=file_menu)

    def open_add_student_dialog(self):
        dialog = AddStudentDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()

    def open_search_student_dialog(self):
        dialog = SearchStudentByNameDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()

    def open_search_parent_dialog(self):
        dialog = SearchParentByNameDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()

    def open_siblings_search_dialog(self):
        dialog = SearchBySiblingsDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()

    def open_income_search_dialog(self):
        dialog = IncomeSearchDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()

    def open_delete_student_dialog(self):
        dialog = DeleteStudentByNameDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()
        deleted, found = self.controller.get_counts()
        messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")

    def open_delete_siblings_dialog(self):
        dialog = DeleteBySiblingsDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()
        deleted, found = self.controller.get_counts()
        messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")

    def open_delete_income_dialog(self):
        dialog = DeleteByIncomeDialog(self, self.controller)
        self.wait_window(dialog)
        self.load_data()
        deleted, found = self.controller.get_counts()
        messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")

    @staticmethod
    def update_status_label(pagination, status_label):
        status_label.config(
            text=f"Страница {pagination.current_page} из {pagination.total_pages} (Размер страницы: {pagination.page_size})")

    def create_controls(self, parent, pagination, update_table_callback):
        control_frame = tk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10, padx=10)

        nav_frame = tk.Frame(control_frame)
        nav_frame.pack(side=tk.LEFT)

        first_button = tk.Button(nav_frame, text="<<", command=lambda: self._handle_pagination_action(
            lambda: pagination.first_page(), pagination, update_table_callback, self.status_label
        ))
        first_button.pack(side=tk.LEFT)

        prev_button = tk.Button(nav_frame, text="<", command=lambda: self._handle_pagination_action(
            lambda: pagination.previous_page(), pagination, update_table_callback, self.status_label
        ))
        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(nav_frame, text=">", command=lambda: self._handle_pagination_action(
            lambda: pagination.next_page(), pagination, update_table_callback, self.status_label
        ))
        next_button.pack(side=tk.LEFT)

        last_button = tk.Button(nav_frame, text=">>", command=lambda: self._handle_pagination_action(
            lambda: pagination.last_page(), pagination, update_table_callback, self.status_label
        ))
        last_button.pack(side=tk.LEFT, padx=5)

        page_size_frame = tk.Frame(control_frame)
        page_size_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(page_size_frame, text="Строк на странице:").pack(side=tk.LEFT)

        page_size_var = tk.StringVar(value="10")
        validation = (parent.register(self._validate_page_size), '%P')
        page_size_entry = tk.Entry(
            page_size_frame,
            textvariable=page_size_var,
            validate="key",
            validatecommand=validation,
            width=5
        )
        page_size_entry.pack(side=tk.LEFT, padx=5)

        page_size_entry.bind("<Return>", lambda e: self._apply_page_size(
            page_size_var, pagination, update_table_callback, self.status_label
        ))

        info_frame = tk.Frame(control_frame)
        info_frame.pack(side=tk.RIGHT, padx=20)
        self.status_label = tk.Label(info_frame, text="")
        self.status_label.pack()

        if pagination:
            self.update_status_label(pagination, self.status_label)

        return {
            "status_label": self.status_label,
            "page_size_var": page_size_var,
            "control_frame": control_frame
        }

    @staticmethod
    def _validate_page_size(new_value):
        return new_value.isdigit() or new_value == ""

    def _apply_page_size(self, page_size_var, pagination, update_callback, status_label):
        try:
            new_size = int(page_size_var.get())
            if new_size <= 0:
                raise ValueError
            if pagination:
                pagination.set_page_size(new_size)
                update_callback()
                self.update_status_label(pagination, status_label)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите положительное число")
            page_size_var.set(str(pagination.page_size if pagination else 10))

    def _handle_pagination_action(self, action, pagination, update_callback, status_label):
        if pagination:
            action()
            update_callback()
            self.update_status_label(pagination, status_label)
