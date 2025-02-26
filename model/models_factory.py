import factory
from factory.alchemy import SQLAlchemyModelFactory

from db_conn import get_session
from models import Parent, Student


class ParentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parent
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    middle_name = factory.Faker('first_name', locale='ru_RU')
    income = factory.Faker('pydecimal', left_digits=5, right_digits=2, positive=True)
    gender = factory.Iterator(['male', 'female'])


class StudentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Student
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "commit"

    first_name = factory.Faker('first_name', locale='ru_RU')
    last_name = factory.Faker('last_name', locale='ru_RU')
    middle_name = factory.Faker('first_name', locale='ru_RU')
    father = factory.SubFactory(ParentFactory)
    mother = factory.SubFactory(ParentFactory)
    brothers_count = factory.Faker('random_int', min=0, max=5)
    sisters_count = factory.Faker('random_int', min=0, max=5)


if __name__ == "__main__":
    with get_session() as session:
        ParentFactory._meta.sqlalchemy_session = session
        StudentFactory._meta.sqlalchemy_session = session
        fathers = [ParentFactory() for _ in range(20)]
        mothers = [ParentFactory() for _ in range(20)]
        students = [StudentFactory(father=fathers[i], mother=mothers[i]) for i in range(20)]
