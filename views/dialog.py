import tkinter as tk
from tkinter import simpledialog, messagebox
from model.models import Parent


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


class AddStudentDialog(BaseDialog):
    def __init__(self, parent, controller):
        self.controller = controller
        super().__init__(parent, title="Добавить студента")
        self.top = None

    def destroy(self):
        if self.top:
            self.top.destroy()
        super().destroy()

    def body(self, master):
        self.entries = {}

        self.top = tk.Toplevel(master)
        self.top.transient(master)
        self.top.grab_set()

        val_num = self.top.register(self.validate_number)
        val_income = self.top.register(self.validate_income)
        val_name = self.top.register(self.validate_name)

        fields = [
            ("Фамилия студента:", "last_name", val_name),
            ("Имя студента:", "first_name", val_name),
            ("Отчество студента:", "middle_name", val_name),
            ("Количество братьев:", "brothers_count", val_num),
            ("Количество сестер:", "sisters_count", val_num),
        ]

        father_fields = [
            ("Фамилия отца:", "father_last", val_name),
            ("Имя отца:", "father_first", val_name),
            ("Отчество отца:", "father_middle", val_name),
            ("Доход отца:", "father_income", val_income),
        ]

        mother_fields = [
            ("Фамилия матери:", "mother_last", val_name),
            ("Имя матери:", "mother_first", val_name),
            ("Отчество матери:", "mother_middle", val_name),
            ("Доход матери:", "mother_income", val_income),
        ]

        row = 0
        tk.Label(self.top, text="Данные студента:").grid(row=row, columnspan=2, sticky="w")
        row += 1

        for label, key, validator in fields:
            tk.Label(self.top, text=label).grid(row=row, sticky="w")
            self.entries[key] = tk.Entry(
                self.top,
                validate="key",
                validatecommand=(validator, "%P")
            )
            self.entries[key].grid(row=row, column=1)
            row += 1

        tk.Label(self.top, text="\nДанные отца:").grid(row=row, columnspan=2, sticky="w")
        row += 1
        for label, key, validator in father_fields:
            tk.Label(self.top, text=label).grid(row=row, sticky="w")
            self.entries[key] = tk.Entry(
                self.top,
                validate="key",
                validatecommand=(validator, "%P")
            )
            self.entries[key].grid(row=row, column=1)
            row += 1

        tk.Label(self.top, text="\nДанные матери:").grid(row=row, columnspan=2, sticky="w")
        row += 1
        for label, key, validator in mother_fields:
            tk.Label(self.top, text=label).grid(row=row, sticky="w")
            self.entries[key] = tk.Entry(
                self.top,
                validate="key",
                validatecommand=(validator, "%P")
            )
            self.entries[key].grid(row=row, column=1)
            row += 1

        button_frame = tk.Frame(self.top)
        button_frame.grid(row=row, columnspan=2, pady=10)

        ok_button = tk.Button(button_frame, text="ОК", command=self.on_ok)
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Отмена", command=self.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)

        return self.entries["last_name"]

    def on_ok(self):
        if self.validate():
            self.apply()
            self.destroy()

    def validate_number(self, value):
        if value == "": return True
        try:
            int(value)
            return True
        except:
            return False

    def validate_income(self, value):
        if value in ("", "."): return True
        try:
            num = float(value)
            return num >= 0
        except:
            return False

    def validate_name(self, value):
        return all(c.isalpha() or c in (" ", "-") for c in value)

    def validate(self):
        required = [
            ("last_name", "Фамилия студента"),
            ("first_name", "Имя студента"),
            ("middle_name", "Отчество студента"),
            ("father_last", "Фамилия отца"),
            ("father_first", "Имя отца"),
            ("father_middle", "Отчество отца"),
            ("father_income", "Доход отца"),
            ("mother_last", "Фамилия матери"),
            ("mother_first", "Имя матери"),
            ("mother_middle", "Отчество матери"),
            ("mother_income", "Доход матери")
        ]

        for field, name in required:
            if field not in self.entries:
                messagebox.showerror("Ошибка конфигурации", f"Отсутствует поле: {field}")
                return False

            value = self.entries[field].get().strip()
            if not value:
                messagebox.showwarning("Ошибка", f"Поле '{name}' обязательно для заполнения")
                return False

        numeric_checks = [
            ("brothers_count", "Количество братьев", 0, 100),
            ("sisters_count", "Количество сестер", 0, 100),
            ("father_income", "Доход отца", 0.01, 1000000),
            ("mother_income", "Доход матери", 0.01, 1000000)
        ]

        for field, name, min_val, max_val in numeric_checks:
            try:
                value = float(self.entries[field].get())
                if not (min_val <= value <= max_val):
                    messagebox.showwarning("Ошибка",
                                           f"{name} должно быть между {min_val} и {max_val}")
                    return False
            except ValueError:
                messagebox.showwarning("Ошибка", f"Некорректное значение для {name}")
                return False

        return True

    def apply(self):
        try:
            data = {key: entry.get().strip() for key, entry in self.entries.items()}

            father = Parent(
                first_name=data["father_first"],
                middle_name=data["father_middle"],
                last_name=data["father_last"],
                income=round(float(data["father_income"]), 2),
                gender="male"
            )

            mother = Parent(
                first_name=data["mother_first"],
                middle_name=data["mother_middle"],
                last_name=data["mother_last"],
                income=round(float(data["mother_income"]), 2),
                gender="female"
            )

            self.controller.db.add_student(
                first_name=data["first_name"],
                middle_name=data["middle_name"],
                last_name=data["last_name"],
                father=father,
                mother=mother,
                brothers_count=int(data["brothers_count"]),
                sisters_count=int(data["sisters_count"])
            )

            messagebox.showinfo("Успех", "Студент успешно добавлен")

        except Exception as e:
            messagebox.showerror("Ошибка",
                                 f"Ошибка при сохранении:\n{str(e)}\n"
                                 "Проверьте корректность всех данных")