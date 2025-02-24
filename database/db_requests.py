from sqlalchemy.orm import joinedload
from db_conn import get_session
from models import Student

class DBRequests:


    @staticmethod
    def get_query():
        with get_session() as session:
            students = (
                session.query(Student)
                .options(joinedload(Student.father), joinedload(Student.mother))
                .all()
            )
            return students

if __name__ == "__main__":
    db = DBRequests()
    with get_session() as session:
        students = db.get_query()
        for student in students:
            print(student)