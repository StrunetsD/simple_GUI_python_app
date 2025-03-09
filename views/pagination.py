import tkinter as tk
from tkinter import messagebox

from table_tree_view import TableView


class SearchResultsWindow(tk.Toplevel):
    def __init__(self, parent, results, title="Результаты поиска"):
        super().__init__(parent)
        self.title(title)
        self.geometry("800x600")

        self.results = results
        self.table_view = TableView(self)
        self.table_view.pack(fill=tk.BOTH, expand=True)

        self.pagination = Pagination(len(results))
        self.create_controls()

        self.update_table()

    def create_controls(self):
        control_frame = tk.Frame(self)
        control_frame.pack(fill=tk.X, pady=10, padx=10)

        nav_frame = tk.Frame(control_frame)
        nav_frame.pack(side=tk.LEFT)

        tk.Button(nav_frame, text="<<",
                  command=lambda: self._handle_pagination_action(self.pagination.first_page)).pack(side=tk.LEFT)
        tk.Button(nav_frame, text="<",
                  command=lambda: self._handle_pagination_action(self.pagination.previous_page)).pack(side=tk.LEFT)
        tk.Button(nav_frame, text=">", command=lambda: self._handle_pagination_action(self.pagination.next_page)).pack(
            side=tk.LEFT)
        tk.Button(nav_frame, text=">>", command=lambda: self._handle_pagination_action(self.pagination.last_page)).pack(
            side=tk.LEFT)

        self.status_label = tk.Label(control_frame, text="")
        self.status_label.pack(side=tk.RIGHT)

    def update_table(self):
        try:
            current_data = self.pagination.get_current_page_data(self.results)
            self.table_view.clear_data()
            if current_data:
                self.table_view.insert_data(current_data)
            self.update_status_label()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления: {str(e)}")

    def update_status_label(self):
        self.status_label.config(
            text=f"Страница {self.pagination.current_page} из {self.pagination.total_pages}"
        )

    def _handle_pagination_action(self, action):
        action()
        self.update_table()


class Pagination:
    def __init__(self, total_items, page_size=10):
        if total_items < 0:
            raise ValueError("Общее количество элементов не может быть отрицательным.")
        if page_size <= 0:
            raise ValueError("Размер страницы должен быть положительным числом.")

        self.page_size = page_size
        self.current_page = 1
        self.total_items = total_items
        self.total_pages = (total_items + page_size - 1) // page_size

    def get_current_page_data(self, data):
        if not isinstance(data, list):
            raise ValueError("Данные должны быть списком.")

        start_index = (self.current_page - 1) * self.page_size
        end_index = start_index + self.page_size
        return data[start_index:end_index]

    def next_page(self):
        if self.current_page < self.total_pages:
            self.current_page += 1

    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1

    def first_page(self):
        self.current_page = 1

    def last_page(self):
        self.current_page = self.total_pages

    def set_page_size(self, size):
        if size <= 0:
            raise ValueError("Размер страницы должен быть положительным числом.")

        self.page_size = size
        self.total_pages = (self.total_items + size - 1) // size
        self.current_page = 1

    def update_total(self, total_items):
        if total_items < 0:
            raise ValueError("Общее количество элементов не может быть отрицательным.")

        self.total_items = total_items
        self.total_pages = (total_items + self.page_size - 1) // self.page_size
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        elif self.current_page < 1:
            self.current_page = 1
