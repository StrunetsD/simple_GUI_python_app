import tkinter as tk
from tkinter import simpledialog, messagebox

from model.models import Parent


class BaseDialog(simpledialog.Dialog):
    def __init__(self, parent, controller, title=None):
        self.controller = controller
        super().__init__(parent, title=title)

    @staticmethod
    def validate_name(value):
        return all(c.isalpha() or c in (" ", "-", "'") for c in value)

    @staticmethod
    def validate_number_of_siblings(value):
        return value == "" or (value.isdigit() and 0 <= int(value) <= 100)

    @staticmethod
    def validate_income(value):
        if value in ("", ".", "-"):
            return True
        try:
            num = float(value)
            return num >= 0
        except Exception:
            return False

    @staticmethod
    def validate_not_empty(value):
        return len(value.strip()) > 0

    @staticmethod
    def validate_int(value):
        return value == "" or value.isdigit()

    @staticmethod
    def validate_float(value):
        try:
            if value in ("", ".", "-"):
                return True
            float(value)
            return True
        except ValueError:
            return False

    @staticmethod
    def show_results(results, title="Результаты", success_message="Найдено записей: {}",
                     empty_message="Записи не найдены"):
        if not results:
            messagebox.showinfo(title, empty_message)
            return

        if isinstance(results, int):
            if results > 0:
                messagebox.showinfo(title, success_message.format(results))
            else:
                messagebox.showinfo(title, empty_message)
        else:
            result_text = "\n".join([str(result) for result in results])
            messagebox.showinfo(title, result_text)

    @staticmethod
    def create_input_field(master, label_text, validation=None):
        frame = tk.Frame(master)
        frame.pack(pady=5, fill=tk.X)

        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(frame)
        if validation:
            entry.config(validate="key", validatecommand=(validation, "%P"))
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

        return entry


class AddBaseDialog(BaseDialog):
    def __init__(self, parent, controller, title=None, fields=None, validation_methods=None):
        self.controller = controller
        self.fields = fields or []
        self.entries = {}
        self.validation_methods = validation_methods or {}
        super().__init__(parent, title=title, controller=controller)

    def body(self, master):
        for section, rows in self.fields:
            frame = tk.LabelFrame(master, text=section)
            frame.pack(fill=tk.X, padx=5, pady=5)

            for label, key, val_type in rows:
                self.create_field(frame, label, key, val_type)

    def create_field(self, master, label, key, val_type):
        frame = tk.Frame(master)
        frame.pack(fill=tk.X, pady=2)

        tk.Label(frame, text=label).pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, validate="key",
                         validatecommand=(self.register(self.validation_methods[val_type]), "%P"))
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        self.entries[key] = entry

    def validate(self):
        for key in self.entries.keys():
            if not self.entries[key].get().strip():
                messagebox.showwarning("Ошибка", f"Заполните поля")
                self.entries[key].focus_set()
                return False
        return True

    def apply(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        self.process_data(data)

    def process_data(self, data):
        pass


class SearchBaseDialog(BaseDialog):
    def __init__(self, parent, controller, title, field_label, search_method):
        self.field_label = field_label
        self.search_method = search_method
        super().__init__(parent, controller, title=title)

    def body(self, master):
        self.entry = self.create_input_field(master, self.field_label)
        return self.entry

    def validate(self):
        value = self.entry.get()
        if not value.strip():
            messagebox.showwarning("Ошибка", "Поле не может быть пустым")
            return False
        return True

    def apply(self):
        search_term = self.entry.get().strip()
        results = self.search_method(search_term)
        self.show_results(results, title="Результаты поиска")


class DeleteBaseDialog(BaseDialog):
    def __init__(self, parent, controller, title, field_label, delete_method):
        self.field_label = field_label
        self.delete_method = delete_method
        super().__init__(parent, controller, title=title)

    def body(self, master):
        self.entry = self.create_input_field(master, self.field_label)
        return self.entry

    def validate(self):
        value = self.entry.get()
        if not value.strip():
            messagebox.showwarning("Ошибка", "Поле не может быть пустым")
            return False
        return True

    def apply(self):
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выполнить удаление?"):
            return

        try:
            deleted_count = self.delete_method(self.entry.get().strip())
            self.show_results(
                deleted_count,
                title="Результаты удаления",
                success_message="Удалено записей: {}",
                empty_message="Записи для удаления не найдены"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class RangeInputDialog(BaseDialog):
    def __init__(self, parent, controller, title, min_label, max_label, apply_method):
        self.min_label = min_label
        self.max_label = max_label
        self.apply_method = apply_method
        super().__init__(parent, controller, title=title)

    def body(self, master):
        self.min_entry = self.create_input_field(master, self.min_label, self.register(self.validate_float))
        self.max_entry = self.create_input_field(master, self.max_label, self.register(self.validate_float))
        return self.min_entry

    def validate(self):
        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())

            if min_val > max_val:
                messagebox.showwarning("Ошибка", "Минимальное значение не может быть больше максимального")
                return False

            return True
        except ValueError:
            messagebox.showwarning("Ошибка", "Введите корректные числовые значения")
            return False

    def apply(self):
        pass


class SearchStudentByNameDialog(SearchBaseDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Поиск по имени студента",
            field_label="Введите часть ФИО студента:",
            search_method=controller.search_students_by_name
        )


class SearchParentByNameDialog(SearchBaseDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Поиск по имени родителя",
            field_label="Введите часть ФИО родителя:",
            search_method=controller.search_parents_by_name
        )


class SearchBySiblingsDialog(SearchBaseDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Поиск по количеству братьев/сестёр",
            field_label="Введите количество братьев или сестер:",
            search_method=controller.search_by_count_of_brothers_or_sisters
        )


class IncomeSearchDialog(RangeInputDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Поиск по доходу родителей",
            min_label="Минимальный доход:",
            max_label="Максимальный доход:",
            apply_method=controller.search_by_income_of_parents
        )

    def apply(self):
        if not self.validate():
            return
        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())
            results = self.apply_method(min_val, max_val)
            self.show_results(
                results,
                title="Результаты поиска",
                success_message="Найдено записей: {}",
                empty_message="Записи не найдены"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class DeleteStudentByNameDialog(DeleteBaseDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Удаление по имени студента",
            field_label="Введите часть ФИО студента:",
            delete_method=controller.delete_student_by_name
        )


class DeleteBySiblingsDialog(DeleteBaseDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            field_label="Введите количество братьев или сестер:",
            title="Удаление по количеству братьев/сестёр",
            delete_method=controller.delete_by_count_of_brothers_or_sisters
        )


class DeleteByIncomeDialog(RangeInputDialog):
    def __init__(self, parent, controller):
        super().__init__(
            parent=parent,
            controller=controller,
            title="Удаление по доходу",
            min_label="Минимальный доход:",
            max_label="Максимальный доход:",
            apply_method=controller.delete_by_income_of_parents
        )

    def apply(self):
        if not messagebox.askyesno("Подтверждение", "Вы уверены, что хотите выполнить удаление?"):
            return

        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())
            deleted_count = self.apply_method(min_val, max_val)

            self.show_results(
                deleted_count,
                title="Результаты удаления",
                success_message="Удалено записей: {}",
                empty_message=f"Записи с доходом от {min_val} до {max_val} не найдены"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


class AddStudentDialog(AddBaseDialog):
    def __init__(self, parent, controller):
        validation_methods = {
            "name": self.validate_name,
            "number": self.validate_number_of_siblings,
            "income": self.validate_income
        }

        fields = [
            ("Студент", [
                ("Фамилия:", "last_name", 'name'),
                ("Имя:", "first_name", 'name'),
                ("Отчество:", "middle_name", 'name'),
                ("Братья:", "brothers_count", 'number'),
                ("Сестры:", "sisters_count", 'number')
            ]),
            ("Отец", [
                ("Фамилия:", "father_last", 'name'),
                ("Имя:", "father_first", 'name'),
                ("Отчество:", "father_middle", 'name'),
                ("Доход:", "father_income", 'income')
            ]),
            ("Мать", [
                ("Фамилия:", "mother_last", 'name'),
                ("Имя:", "mother_first", 'name'),
                ("Отчество:", "mother_middle", 'name'),
                ("Доход:", "mother_income", 'income')
            ])
        ]

        super().__init__(parent, controller,
                         title="Добавить студента",
                         fields=fields,
                         validation_methods=validation_methods
                         )

    def process_data(self, data):
        try:
            father = Parent(
                first_name=data['father_first'],
                middle_name=data['father_middle'],
                last_name=data['father_last'],
                income=round(float(data['father_income']), 2),
                gender="male"
            )

            mother = Parent(
                first_name=data['mother_first'],
                middle_name=data['mother_middle'],
                last_name=data['mother_last'],
                income=round(float(data['mother_income']), 2),
                gender="female"
            )

            self.controller.add_student(
                first_name=data['first_name'],
                middle_name=data['middle_name'],
                last_name=data['last_name'],
                father=father,
                mother=mother,
                brothers_count=int(data['brothers_count']),
                sisters_count=int(data['sisters_count'])
            )

            messagebox.showinfo("Успех", "Студент успешно добавлен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при добавлении: {str(e)}")
