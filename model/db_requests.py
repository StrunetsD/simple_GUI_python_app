from sqlalchemy.orm import joinedload
from db_conn import get_session
from .models import Student, Parent
from sqlalchemy.exc import SQLAlchemyError


class DBRequests:

    @staticmethod
    def add_student(first_name, middle_name, last_name, father: Parent, mother: Parent,
                    brothers_count: int = 0, sisters_count: int = 0):
        with get_session() as session:
            try:
                session.add(father)
                session.add(mother)
                session.flush()   # id родителя

                student = Student(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    father_id=father.id,
                    mother_id=mother.id,
                    brothers_count=brothers_count,
                    sisters_count=sisters_count
                )

                session.add(student)
                session.commit()
                return student

            except Exception as e:
                session.rollback()
                raise ValueError(f"Ошибка при добавлении: {str(e)}")

    @staticmethod
    def get_query_of_students():
        try:
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
                        student.father.full_name if student.father else "Нет данных",
                        f"{student.father.income:.2f}" if student.father else "0.00",
                        student.mother.full_name if student.mother else "Нет данных",
                        f"{student.mother.income:.2f}" if student.mother else "0.00",
                        student.brothers_count,
                        student.sisters_count
                    ))
                return data
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при получении списка студентов: {e}")

    @staticmethod
    def search_students_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        try:
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
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при поиске студентов: {e}")

    @staticmethod
    def delete_student_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        try:
            with get_session() as session:
                student = session.query(Student).options(
                    joinedload(Student.father),
                    joinedload(Student.mother)
                ).filter(
                    (Student.first_name.ilike(f'%{search_term}%')) |
                    (Student.middle_name.ilike(f'%{search_term}%')) |
                    (Student.last_name.ilike(f'%{search_term}%'))
                ).first()

                if not student:
                    raise ValueError("Студент не найден.")

                session.delete(student)
                session.commit()
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при удалении студента: {e}")

    @staticmethod
    def delete_parent_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        try:
            with get_session() as session:
                parent_to_delete = session.query(Parent).filter(
                    (Parent.first_name.ilike(f'%{search_term}%')) |
                    (Parent.middle_name.ilike(f'%{search_term}%')) |
                    (Parent.last_name.ilike(f'%{search_term}%'))
                ).first()

                if not parent_to_delete:
                    raise ValueError("Родитель не найден.")

                session.delete(parent_to_delete)
                session.commit()
                return parent_to_delete
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при удалении родителя: {e}")

    @staticmethod
    def search_parents_by_name(search_term):
        if not search_term:
            raise ValueError("Поисковой запрос не может быть пустым.")
        try:
            with get_session() as session:
                parents = session.query(Parent).filter(
                    (Parent.first_name.ilike(f'%{search_term}%')) |
                    (Parent.middle_name.ilike(f'%{search_term}%')) |
                    (Parent.last_name.ilike(f'%{search_term}%'))
                ).all()
            return parents
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при поиске родителей: {e}")

    @staticmethod
    def search_by_count_of_brothers_or_sisters(count):
        if count is None:
            raise ValueError("Количество не может быть None.")
        try:
            with get_session() as session:
                students = session.query(Student).options(
                    joinedload(Student.father),
                    joinedload(Student.mother)
                ).filter(
                    (Student.brothers_count == count) |
                    (Student.sisters_count == count)
                ).all()
            return students
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при поиске студентов по количеству братьев или сестер: {e}")

    @staticmethod
    def delete_by_count_of_brothers_or_sisters(count):
        if count is None:
            raise ValueError("Количество не может быть None.")
        try:
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

                session.commit()
                return len(students)
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при удалении студентов по количеству братьев или сестер: {e}")

    @staticmethod
    def search_by_income_of_parents(minimum_income, maximum_income):
        if minimum_income is not None and maximum_income is not None and minimum_income > maximum_income:
            raise ValueError("Минимальный доход не может быть больше максимального.")
        try:
            with get_session() as session:
                query = session.query(Parent)

                if minimum_income is not None:
                    query = query.filter(Parent.income >= minimum_income)
                if maximum_income is not None:
                    query = query.filter(Parent.income <= maximum_income)

                parents = query.all()
                return parents
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при поиске родителей по доходу: {e}")

    @staticmethod
    def delete_by_income_of_parents(minimum_income=None, maximum_income=None):
        if minimum_income is not None and maximum_income is not None and minimum_income > maximum_income:
            raise ValueError("Минимальный доход не может быть больше максимального.")
        try:
            with get_session() as session:
                query = session.query(Parent)

                if minimum_income is not None:
                    query = query.filter(Parent.income >= minimum_income)
                if maximum_income is not None:
                    query = query.filter(Parent.income <= maximum_income)

                parents_to_delete = query.all()

                if not parents_to_delete:
                    raise ValueError("Нет записей для удаления.")

                for parent in parents_to_delete:
                    session.delete(parent)

                session.commit()
                return len(parents_to_delete)
        except SQLAlchemyError as e:
            raise ValueError(f"Ошибка при удалении по доходу: {e}")
