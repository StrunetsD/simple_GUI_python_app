import tkinter as tk
from tkinter import simpledialog, messagebox


class BaseDialog(simpledialog.Dialog):

    @staticmethod
    def show_results(results, title="Результаты поиска"):
        if results:
            result_text = "\n".join([str(result) for result in results])
            messagebox.showinfo(title, result_text)
        else:
            messagebox.showinfo(title, "Записи не найдены.")


class SearchStudentByNameDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Поиск по имени студента")

    def body(self, master):
        tk.Label(master, text="Введите часть ФИО студента:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, padx=5, pady=5)
        return self.entry

    def validate(self):
        if not self.entry.get():
            messagebox.showwarning("Ошибка", "Введите данные для поиска.")
            return False
        return True

    def apply(self):
        results = self.controller.search_students_by_name(self.entry.get())
        self.show_results(results)


class SearchParentByNameDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Поиск по имени родителя")

    def body(self, master):
        tk.Label(master, text="Введите часть ФИО родителя:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, padx=5, pady=5)
        return self.entry

    def validate(self):
        if not self.entry.get():
            messagebox.showwarning("Ошибка", "Введите данные для поиска.")
            return False
        return True

    def apply(self):
        results = self.controller.search_parents_by_name(self.entry.get())
        self.show_results(results)


class SearchBySiblingsDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Поиск по количеству братьев/сестёр")

    def body(self, master):
        tk.Label(master, text="Введите точное количество:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, padx=5, pady=5)
        return self.entry

    def validate(self):
        try:
            int(self.entry.get())
            return True
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите целое число.")
            return False

    def apply(self):
        try:
            results = self.controller.search_by_count_of_brothers_or_sisters(int(self.entry.get()))
            self.show_results(results)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class IncomeSearchDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Поиск по доходу родителей")

    def body(self, master):
        tk.Label(master, text="Минимальный доход:").grid(row=0)
        self.min_income_entry = tk.Entry(master)
        self.min_income_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Максимальный доход:").grid(row=1)
        self.max_income_entry = tk.Entry(master)
        self.max_income_entry.grid(row=1, column=1, padx=5, pady=5)
        return self.min_income_entry

    def validate(self):
        try:
            min_income = float(self.min_income_entry.get())
            max_income = float(self.max_income_entry.get())

            if min_income > max_income:
                messagebox.showwarning("Ошибка", "Минимальный доход не может быть больше максимального.")
                return False

            if min_income < 0 or max_income < 0:
                messagebox.showwarning("Ошибка", "Доходы должны быть положительными числами.")
                return False

        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректные числа.")
            return False

        return True

    def apply(self):
        min_income = float(self.min_income_entry.get())
        max_income = float(self.max_income_entry.get())
        results = self.controller.search_by_income_of_parents(min_income, max_income)
        if results:
            result_text = "\n".join([str(result) for result in results])
            messagebox.showinfo("Результаты поиска", result_text)
        else:
            messagebox.showinfo("Результаты поиска", "Записи не найдены.")


class DeleteStudentByNameDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Удаление по имени студента")

    def body(self, master):
        tk.Label(master, text="Введите часть ФИО студента:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, padx=5, pady=5)
        return self.entry

    def validate(self):
        if not self.entry.get():
            messagebox.showwarning("Ошибка", "Введите данные для удаления.")
            return False
        return True

    def apply(self):
        deleted = self.controller.delete_student_by_name(self.entry.get())
        messagebox.showinfo("Удалено", f"Удалено записей: {deleted}")


class DeleteBySiblingsDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Удаление по количеству братьев/сестёр")

    def body(self, master):
        tk.Label(master, text="Введите точное количество:").grid(row=0)
        self.entry = tk.Entry(master)
        self.entry.grid(row=1, padx=5, pady=5)
        return self.entry

    def validate(self):
        try:
            int(self.entry.get())
            return True
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите целое число.")
            return False

    def apply(self):
        deleted = self.controller.delete_by_count_of_brothers_or_sisters(int(self.entry.get()))
        deleted_total, found_total = self.controller.get_counts()
        messagebox.showinfo("Удалено",
                            f"Текущее удаление: {deleted}\nОбщий счётчик удалений: {deleted_total}")



class DeleteByIncomeDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Удаление по доходу")

    def body(self, master):
        tk.Label(master, text="Минимальный доход:").grid(row=0)
        self.min_income_entry = tk.Entry(master)
        self.min_income_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(master, text="Максимальный доход:").grid(row=1)
        self.max_income_entry = tk.Entry(master)
        self.max_income_entry.grid(row=1, column=1, padx=5, pady=5)
        return self.min_income_entry

    def validate(self):
        try:
            min_income = float(self.min_income_entry.get())
            max_income = float(self.max_income_entry.get())

            if min_income > max_income:
                messagebox.showwarning("Ошибка", "Минимальный доход не может быть больше максимального.")
                return False

            if min_income < 0 or max_income < 0:
                messagebox.showwarning("Ошибка", "Доходы должны быть положительными числами.")
                return False

        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректные числа.")
            return False

        return True

    def apply(self):
        min_income = float(self.min_income_entry.get())
        max_income = float(self.max_income_entry.get())
        deleted = self.controller.delete_by_income_of_parents(min_income, max_income)
        messagebox.showinfo("Удалено", f"Удалено записей: {deleted}\nВсего удалено записей: {self.controller.deleted_count}")


