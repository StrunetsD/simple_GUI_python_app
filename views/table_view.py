import tkinter as tk
from tkinter import ttk


class TableView(ttk.Frame):
    def __init__(self, parent, columns=None):
        super().__init__(parent)
        self.columns = columns or (
            "ФИО студента",
            "ФИО Отца",
            "Заработок отца",
            "ФИО Матери",
            "Заработок матери",
            "Число братьев",
            "Число сестер"
        )

        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, stretch=tk.YES)

        self.tree.pack(fill=tk.BOTH, expand=True)

    def insert_data(self, data):
        for row in data:
            self.tree.insert("", "end", values=row)

    def clear_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
