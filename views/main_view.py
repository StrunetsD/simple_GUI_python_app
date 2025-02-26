from views.table_view import TableView
from dialog import *
from views.pagination import Pagination
from controllers.controllers import Controller


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Студенты")
        self.geometry("600x400")
        self.controller = Controller()
        self.table_view = TableView(self)
        self.table_view.pack(fill=tk.BOTH, expand=True)

        try:
            self.data = self.controller.get_students()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить данные студентов: {e}")
            self.data = []

        self.pagination = Pagination(len(self.data))

        controls = self.create_controls(self, self.pagination, self.update_table)
        self.status_label = controls["status_label"]

        self.update_table()
        self.update_status_label(self.pagination, self.status_label)

        self.create_menu()

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
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить данные: {e}")

    def update_table(self):
        try:
            current_data = self.pagination.get_current_page_data(self.data)
            self.table_view.clear_data()
            self.table_view.insert_data(current_data)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обновить таблицу: {e}")

    def previous_page(self):
        try:
            self.pagination.previous_page()
            self.update_table()
            self.update_status_label(self.pagination, self.status_label)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось перейти на предыдущую страницу: {e}")

    def next_page(self):
        try:
            self.pagination.next_page()
            self.update_table()
            self.update_status_label(self.pagination, self.status_label)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось перейти на следующую страницу: {e}")

    def count(self):
        try:
            deleted_count, found_count = self.controller.get_counts()
            messagebox.showinfo("Статистика", f"Удалено записей: {deleted_count}\nНайдено записей: {found_count}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить статистику: {e}")

    def create_menu(self):
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
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
        try:
            dialog = AddStudentDialog(self, self.controller)
            self.wait_window(dialog.top)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении студента: {str(e)}")

    def open_search_student_dialog(self):
        try:
            dialog = SearchStudentByNameDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога поиска студента: {e}")

    def open_search_parent_dialog(self):
        try:
            dialog = SearchParentByNameDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога поиска родителя: {e}")

    def open_siblings_search_dialog(self):
        try:
            dialog = SearchBySiblingsDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога поиска брата/сестры: {e}")

    def open_income_search_dialog(self):
        try:
            dialog = IncomeSearchDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога поиска по заработку: {e}")

    def open_delete_student_dialog(self):
        try:
            dialog = DeleteStudentByNameDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
            deleted, found = self.controller.get_counts()
            messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога удаления студента: {e}")

    def open_delete_siblings_dialog(self):
        try:
            dialog = DeleteBySiblingsDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
            deleted, found = self.controller.get_counts()
            messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога удаления по брату/сестре: {e}")

    def open_delete_income_dialog(self):
        try:
            dialog = DeleteByIncomeDialog(self, self.controller)
            self.wait_window(dialog)
            self.load_data()
            deleted, found = self.controller.get_counts()
            messagebox.showinfo("Статистика", f"Всего удалено: {deleted}\nВсего найдено: {found}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии диалога удаления по доходу: {e}")

    @staticmethod
    def update_status_label(pagination, status_label):
        status_label.config(
            text=f"Страница {pagination.current_page} из {pagination.total_pages} (Размер страницы: {pagination.page_size})")

    def create_controls(self, parent, pagination, update_table_callback):
        control_frame = tk.Frame(parent)
        control_frame.pack(fill=tk.X, pady=10, padx=10)

        nav_frame = tk.Frame(control_frame)
        nav_frame.pack(side=tk.LEFT)

        first_button = tk.Button(nav_frame, text="<<",
                                 command=lambda: [
                                     pagination.first_page() if pagination else None,
                                     update_table_callback(),
                                     self.update_status_label(pagination, status_label) if pagination else None])

        first_button.pack(side=tk.LEFT)

        prev_button = tk.Button(nav_frame, text="<",
                                command=lambda: [
                                    pagination.previous_page() if pagination else None,
                                    update_table_callback(),
                                    self.update_status_label(pagination, status_label) if pagination else None])

        prev_button.pack(side=tk.LEFT, padx=5)

        next_button = tk.Button(nav_frame, text=">", command=lambda: [
            pagination.next_page() if pagination else None,
            update_table_callback(),
            self.update_status_label(pagination, status_label) if pagination else None])

        next_button.pack(side=tk.LEFT)

        last_button = tk.Button(nav_frame, text=">>", command=lambda: [
            pagination.last_page() if pagination else None,
            update_table_callback(),
            self.update_status_label(pagination, status_label) if pagination else None])

        last_button.pack(side=tk.LEFT, padx=5)

        page_size_var = tk.StringVar(value="10")
        sizes = ("10", "20", "50", "100")
        page_size_menu = tk.OptionMenu(
            control_frame,
            page_size_var,
            *sizes,
            command=lambda value: [
                pagination.set_page_size(int(value)) if pagination else None,
                update_table_callback(),
                self.update_status_label(pagination, status_label) if pagination else None])

        page_size_menu.pack(side=tk.RIGHT)

        info_frame = tk.Frame(control_frame)
        info_frame.pack(side=tk.RIGHT, padx=20)

        status_label = tk.Label(info_frame, text="")
        status_label.pack()

        if pagination:
            self.update_status_label(pagination, status_label)

        return {
            "status_label": status_label,
            "page_size_var": page_size_var,
        }


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
