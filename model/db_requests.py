from sqlalchemy.orm import joinedload
from db_conn import get_session
from models import Student, Parent


class DBRequests:

    @staticmethod
    def get_query_of_students():
        with get_session() as session:
            students = (
                session.query(Student)
                .options(joinedload(Student.father), joinedload(Student.mother))
                .all()
            )

            data = []
            for student in students:
                data.append((
                    student.full_name,
                    student.get_father_full_name,
                    student.get_father_income,
                    student.get_mother_full_name,
                    student.get_mother_income,
                    student.brothers_count,
                    student.sisters_count
                ))
            return data

    @staticmethod
    def search_students_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        with get_session() as session:
            students = session.query(Student).options(
                joinedload(Student.father),
                joinedload(Student.mother)
            ).filter(
                (Student.first_name.ilike(f'%{search_term}%')) |
                (Student.middle_name.ilike(f'%{search_term}%')) |
                (Student.last_name.ilike(f'%{search_term}%'))
            ).all()
        return students

    @staticmethod
    def delete_student_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        with get_session() as session:
            students = session.query(Student).options(
                joinedload(Student.father),
                joinedload(Student.mother)
            ).filter(
                (Student.first_name.ilike(f'%{search_term}%')) |
                (Student.middle_name.ilike(f'%{search_term}%')) |
                (Student.last_name.ilike(f'%{search_term}%'))
            ).first()

            if not students:
                raise ValueError("Студент не найден.")

            try:
                session.delete(students)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ValueError(f'Ошибка при удалении студента: {e}')


    @staticmethod
    def delete_parent_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        with get_session() as session:
            parent_to_delete = session.query(Parent).filter(
                (Parent.first_name.ilike(f'%{search_term}%')) |
                (Parent.middle_name.ilike(f'%{search_term}%')) |
                (Parent.last_name.ilike(f'%{search_term}%'))
            ).first()

            if not parent_to_delete:
                raise ValueError("Родитель не найден.")

            try:
                session.delete(parent_to_delete)
                session.commit()
            except Exception as e:
                session.rollback()
                raise ValueError(f'Ошибка при удалении родителя: {e}')

            return parent_to_delete

    @staticmethod
    def search_parents_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        with get_session() as session:
            parents = session.query(Parent).filter(
                (Parent.first_name.ilike(f'%{search_term}%')) |
                (Parent.middle_name.ilike(f'%{search_term}%')) |
                (Parent.last_name.ilike(f'%{search_term}%'))
            ).all()
        return parents

    @staticmethod
    def search_by_count_of_brothers_or_sisters(count):
        if count is None:
            raise ValueError("Количество не может быть None.")
        with get_session() as session:
            students = session.query(Student).options(
                joinedload(Student.father),
                joinedload(Student.mother)
            ).filter(
                (Student.brothers_count == count) |
                (Student.sisters_count == count)
            ).all()
            return students

    @staticmethod
    def delete_by_count_of_brothers_or_sisters(count):
        if count is None:
            raise ValueError("Количество не может быть None.")
        with get_session() as session:
            students = session.query(Student).options(
                joinedload(Student.father),
                joinedload(Student.mother)
            ).filter(
                (Student.brothers_count == count) |
                (Student.sisters_count == count)
            ).all()

            if not students:
                raise ValueError("Нет студентов для удаления.")

            for student in students:
                session.delete(student)

            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise ValueError(f'Ошибка при удалении студентов: {e}')

            return len(students)

    @staticmethod
    def search_by_income_of_parents(minimum_income, maximum_income):
        if minimum_income is not None and maximum_income is not None and minimum_income > maximum_income:
            raise ValueError("Минимальный доход не может быть больше максимального.")
        with get_session() as session:
            query = session.query(Parent)

            if minimum_income is not None:
                query = query.filter(Parent.income >= minimum_income)
            if maximum_income is not None:
                query = query.filter(Parent.income <= maximum_income)

            parents = query.all()
            return parents

    @staticmethod
    def , (minimum_income=None, maximum_income=None):
        if minimum_income is not None and maximum_income is not None and minimum_income > maximum_income:
            raise ValueError("Минимальный доход не может быть больше максимального.")
        with get_session() as session:
            query = session.query(Parent)

            if minimum_income is not None:
                query = query.filter(Parent.income >= minimum_income)
            if maximum_income is not None:
                query = query.filter(Parent.income <= maximum_income)

            parents_to_delete = query.all()

            if not parents_to_delete:
                raise ValueError("Нет родителей для удаления.")

            for parent in parents_to_delete:
                session.delete(parent)

            try:
                session.commit()
            except Exception as e:
                session.rollback()
                raise ValueError(f'Ошибка при удалении родителей: {e}')

            return len(parents_to_delete)
