import tkinter as tk
from tree_view import TableView
from model.db_requests import DBRequests


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Table View Example")
        self.geometry("600x400")
        db = DBRequests()

        columns = (
                    "ФИО студента",
                    "ФИО Отца",
                    "заработок отца",
                    "ФИО Матери",
                    "заработок матери",
                    "число братьев",
                    "число сестер"
                    )

        self.table_view = TableView(self, columns)
        self.table_view.pack(fill=tk.BOTH, expand=True)

        data = db.get_query()

        self.table_view.insert_data(data)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
