import os
import xml.dom.minidom
import xml.sax

from xml_models import XMLStudent


class XMLManager:
    def __init__(self, students_file=None):
        self.students_file = students_file

    def set_file(self, file_path):
        self.students_file = file_path
        self._init_files()

    def _init_files(self):
        if self.students_file:
            os.makedirs(os.path.dirname(self.students_file), exist_ok=True)
            if not os.path.exists(self.students_file):
                self.save_students([])

    def save_students(self, students):
        doc = xml.dom.minidom.Document()
        root = doc.createElement("students")
        doc.appendChild(root)

        for student in students:
            student_elem = doc.createElement("student")

            def add_text_elem(parent, tag, value):
                elem = doc.createElement(tag)
                elem.appendChild(doc.createTextNode(str(value)))
                parent.appendChild(elem)

            add_text_elem(student_elem, "fio", student.fio)
            add_text_elem(student_elem, "father_fio", student.father_fio)
            add_text_elem(student_elem, "mother_fio", student.mother_fio)
            add_text_elem(student_elem, "father_income", student.father_income)
            add_text_elem(student_elem, "mother_income", student.mother_income)
            add_text_elem(student_elem, "brother_count", student.brother_count)
            add_text_elem(student_elem, "sister_count", student.sister_count)

            root.appendChild(student_elem)

        with open(self.students_file, 'w', encoding='utf-8') as f:
            doc.writexml(f, indent="", addindent="  ", newl="\n", encoding="utf-8")


class StudentsSAXHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.students = []
        self.current_data = ""
        self.current_student = None
        self.content = ""

    def startElement(self, tag, _):
        self.current_data = tag
        if tag == "student":
            self.current_student = XMLStudent(
                fio="", father_fio="", mother_fio="",
                father_income=0, mother_income=0,
                brother_count=0, sister_count=0
            )

    def endElement(self, tag):
        if self.current_student is None:
            return

        if tag == "fio":
            self.current_student.fio = self.content
        elif tag == "father_fio":
            self.current_student.father_fio = self.content
        elif tag == "mother_fio":
            self.current_student.mother_fio = self.content
        elif tag == "father_income":
            self.current_student.father_income = float(self.content)
        elif tag == "mother_income":
            self.current_student.mother_income = float(self.content)
        elif tag == "brother_count":
            self.current_student.brother_count = int(self.content)
        elif tag == "sister_count":
            self.current_student.sister_count = int(self.content)
        elif tag == "student":
            self.students.append(self.current_student)

        self.content = ""

    def characters(self, content):
        self.content += content.strip()


class StudentsModel:
    def __init__(self, xml_manager):
        self.students = []
        self.xml_manager = xml_manager

    def load_students(self, file_path):
        handler = StudentsSAXHandler()
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)
        parser.setContentHandler(handler)
        parser.parse(file_path)
        self.students = handler.students
        self.xml_manager.set_file(file_path)
        return self.students

    def save_students(self):
        self.xml_manager.save_students(self.students)

    def add_student(self, student_data):
        student = XMLStudent(**student_data)
        self.students.append(student)
        self.save_students()

    def search_by_fio(self, fio_part: str):
        return [s for s in self.students if fio_part.lower() in s.fio.lower()]

    def search_by_parent_name(self, last_name: str):
        return [
            s for s in self.students
            if last_name.lower() in s.father_fio.lower().split()[0] or
               last_name.lower() in s.mother_fio.lower().split()[0]
        ]

    def search_by_count_of_brothers_or_sisters(self, count):
        count = int(count)
        return [s for s in self.students if s.brother_count == count or s.sister_count == count]

    def search_by_income_parents(self, income_part):
        income_part = float(income_part)
        return [
            s for s in self.students
            if s.father_income == income_part or s.mother_income == income_part
        ]

    def delete_by_count_of_brothers_or_sisters(self, count):
        count = int(count)
        before = len(self.students)
        self.students = [
            s for s in self.students
            if s.brother_count != count and s.sister_count != count
        ]
        deleted = before - len(self.students)
        if deleted > 0:
            self.save_students()
        return deleted

    def delete_student_by_fio(self, index):
        index = int(index)
        if 0 <= index < len(self.students):
            del self.students[index]
            self.save_students()
            return f"Студент с индексом {index} удален."
        else:
            return "Ошибка: неверный индекс."

    def delete_by_income_parents(self, min_income: float, max_income: float):
        min_income = float(min_income)
        max_income = float(max_income)
        before = len(self.students)
        self.students = [
            s for s in self.students
            if not (min_income <= s.father_income <= max_income) and
               not (min_income <= s.mother_income <= max_income)
        ]
        deleted = before - len(self.students)
        if deleted > 0:
            self.save_students()
        return deleted
