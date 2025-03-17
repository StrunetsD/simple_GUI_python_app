from model.db_requests import DBRequests
from xml_manager import StudentsModel as xmlStudents
from xml_manager import XMLManager


class Controller:
    def __init__(self, mode):
        self.db = DBRequests()
        self.xml_manager = XMLManager()
        self.deleted_count = 0
        self.found_count = 0
        self.mode = mode
        self.handler = self._get_handler()
        self.xml_model = xmlStudents(self.xml_manager)

    def _get_handler(self):
        if self.mode == "db":
            from model.db_requests import DBRequests
            return DBRequests()
        elif self.mode == "xml":
            from model.xml_manager import XMLManager
            return XMLManager()
        else:
            raise ValueError("Неподдерживаемый режим работы")

    def get_students(self, file_path=None):
        if self.mode == "xml":
            students = self.xml_model.load_students(file_path)  # Загрузка данных
            return students
        return self.db.get_query_of_students()

    def add_student(self, first_name, middle_name, last_name, father, mother,brothers_count, sisters_count,
                    father_income=None, mother_income=None):
        if self.mode == "xml":
            student_data = {
                "fio": f"{last_name} {first_name} {middle_name}",
                "father_fio": father,
                "mother_fio": mother,
                "father_income": father_income,
                "mother_income": mother_income,
                "brother_count": brothers_count,
                "sister_count": sisters_count
            }
            self.xml_model.add_student(student_data)
        elif self.mode == "db":
            self.db.add_student(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                father=father,
                mother=mother,
                brothers_count=brothers_count,
                sisters_count=sisters_count
            )

    def delete_by_income_of_parents(self, min_income=None, max_income=None):
        if self.mode == "db":
            count = self.db.delete_by_income_of_parents(min_income, max_income)
            self.deleted_count += count
            return f"Удалено {count} записей"
        else:
            count = self.xml_model.delete_by_income_parents(min_income, max_income)
            self.deleted_count += count
            return f"Удалено {count} записей"

    def search_by_income_of_parents(self, min_income, max_income):
        if self.mode == "db":
            results = self.db.search_by_income_of_parents(min_income, max_income)
            formatted = []
            for parent in results:
                if parent.gender == "male":
                    formatted.append((
                        "-",
                        f"{parent.last_name} {parent.first_name} {parent.middle_name}",
                        parent.income,
                        "-", "-", "-", "-"
                    ))
                else:
                    formatted.append((
                        "-",
                        "-", "-",
                        f"{parent.last_name} {parent.first_name} {parent.middle_name}",
                        parent.income,
                        "-", "-"
                    ))
            self.found_count += len(results)
            return formatted
        else:
            results = []
            for student in self.xml_model.students:
                if min_income <= student.father_income <= max_income:
                    results.append((
                        "-",
                        student.father_fio,
                        student.father_income,
                        "-", "-", "-", "-"
                    ))
                if min_income <= student.mother_income <= max_income:
                    results.append((
                        "-",
                        "-", "-",
                        student.mother_fio,
                        student.mother_income,
                        "-", "-"
                    ))
            self.found_count += len(results)
            return results

    def search_by_count_of_brothers_or_sisters(self, count):
        if self.mode == "db":
            results = self.db.search_by_count_of_brothers_or_sisters(count)
            formatted_result = []
            for student in results:
                formatted = (
                    f"{student.last_name} {student.first_name} {student.middle_name}",
                    f"{student.father.last_name} {student.father.first_name} {student.father.middle_name}",
                    student.father.income,
                    f"{student.mother.last_name} {student.mother.first_name} {student.mother.middle_name}",
                    student.mother.income,
                    student.brothers_count,
                    student.sisters_count
                )
                formatted_result.append(formatted)
            self.found_count += len(results)
            return formatted_result
        else:
            results = self.xml_model.search_by_count_of_brothers_or_sisters(count)
            formatted_result = []
            for student in results:
                formatted = (
                    student.fio,
                    student.father_fio,
                    student.father_income,
                    student.mother_fio,
                    student.mother_income,
                    student.brother_count,
                    student.sister_count
                )
                formatted_result.append(formatted)
            self.found_count += len(results)
            return formatted_result

    def search_students_by_name(self, search_term):
        if self.mode == "db":
            results = self.db.search_students_by_name(search_term)
            formatted = []
            for student in results:
                formatted_results = (
                    f"{student.last_name} {student.first_name} {student.middle_name}",
                    f"{student.father.last_name} {student.father.first_name} {student.father.middle_name}",
                    student.father.income,
                    f"{student.mother.last_name} {student.mother.first_name} {student.mother.middle_name}",
                    student.mother.income,
                    student.brothers_count,
                    student.sisters_count
                )
                formatted.append(formatted_results)
            self.found_count += len(results)
            return formatted
        else:
            results = self.xml_model.search_by_fio(search_term)
            formatted = []
            for student in results:
                formatted_results = (
                    student.fio,
                    student.father_fio,
                    student.father_income,
                    student.mother_fio,
                    student.mother_income,
                    student.brother_count,
                    student.sister_count
                )
                formatted.append(formatted_results)
            self.found_count += len(results)
            return formatted

    def search_parents_by_name(self, search_item):
        if self.mode == "db":
            results = self.db.search_parents_by_name(search_item)
            formatted_result = []
            for parent in results:
                if parent.gender == "male":
                    formatted = (
                        "-",
                        f"{parent.last_name} {parent.first_name} {parent.middle_name}",
                        parent.income,
                        "-", "-", "-", "-"
                    )
                    formatted_result.append(formatted)
                else:
                    formatted = (
                        "-",
                        "-", "-",
                        f"{parent.last_name} {parent.first_name} {parent.middle_name}",
                        parent.income,
                        "-", "-"
                    )
                    formatted_result.append(formatted)
            self.found_count += len(results)
            return formatted_result
        else:
            results = self.xml_model.search_by_parent_name(search_item)
            formatted_result = []
            for student in results:
                formatted_father = (
                    "-",
                    student.father_fio,
                    student.father_income,
                    "-", "-", "-", "-"
                )
                formatted_result.append(formatted_father)

                formatted_mother = (
                    "-",
                    "-", "-",
                    student.mother_fio,
                    student.mother_income,
                    "-", "-"
                )
                formatted_result.append(formatted_mother)

            self.found_count += len(results) * 2
            return formatted_result

    def delete_by_count_of_brothers_or_sisters(self, count: int):
        count = int(count)
        if self.mode == "db":
            count = self.db.delete_by_count_of_brothers_or_sisters(count)
            self.deleted_count += count
            return f"Удалено {count} записей"
        else:
            before = len(self.xml_model.students)
            self.xml_model.students = [
                s for s in self.xml_model.students
                if s.brother_count != count and s.sister_count != count
            ]
            deleted_count = before - len(self.xml_model.students)
            if deleted_count > 0:
                self.xml_model.save_students()
            self.deleted_count += deleted_count
            return f"Удалено {deleted_count} записей"

    def delete_parent_by_name(self, search_term: str):
        if self.mode == "db":
            self.db.delete_parent_by_name(search_term)
            self.deleted_count += 1
            return f"Удалена 1 запись {search_term}"
        else:
            before = len(self.xml_model.students)
            self.xml_model.students = [
                s for s in self.xml_model.students
                if search_term.lower() not in s.father_fio.lower() and
                   search_term.lower() not in s.mother_fio.lower()
            ]
            deleted_count = before - len(self.xml_model.students)
            if deleted_count > 0:
                self.xml_model.save_students()
            self.deleted_count += deleted_count
            return f"Удалено {deleted_count} записей"

    def delete_student_by_name(self, search_term: str):
        if self.mode == "db":
            self.db.delete_student_by_name(search_term)
            self.deleted_count += 1
            return f"Удалена 1 запись {search_term}"
        else:
            before = len(self.xml_model.students)
            self.xml_model.students = [
                s for s in self.xml_model.students
                if search_term.lower() not in s.fio.lower()
            ]
            deleted_count = before - len(self.xml_model.students)
            if deleted_count > 0:
                self.xml_model.save_students()
            self.deleted_count += deleted_count
            return f"Удалено {deleted_count} записей"

    def get_counts(self):
        return self.deleted_count, self.found_count
