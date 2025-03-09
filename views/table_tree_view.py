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

class TreeView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("Details"), show="tree")
        self.tree.heading("#0", text="Студенты")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def insert_data(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for student in data:
            student_id = self.tree.insert("", "end", text=student[0], values=("Студент"))
            father_info = f"Отец: {student[1]} (Доход: {student[2]})"
            self.tree.insert(student_id, "end", text=father_info)
            mother_info = f"Мать: {student[3]} (Доход: {student[4]})"
            self.tree.insert(student_id, "end", text=mother_info)
            siblings_info = f"Братья: {student[5]}, Сестры: {student[6]}"
            self.tree.insert(student_id, "end", text=siblings_info)

    def clear_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)