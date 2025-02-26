from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class Parent(Base):
    __tablename__ = 'parents'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    income = Column(Numeric(12, 2), nullable=False)
    gender = Column(String, nullable=False)

    children_as_father = relationship(
        'Student',
        back_populates='father',
        foreign_keys='Student.father_id',
        cascade="all, delete-orphan"
    )

    children_as_mother = relationship(
        'Student',
        back_populates='mother',
        foreign_keys='Student.mother_id',
        cascade="all, delete-orphan"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def __repr__(self):
        return f"<({self.first_name} {self.middle_name} {self.last_name}, {self.income}, gender={self.gender})>"


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    father_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    mother_id = Column(Integer, ForeignKey('parents.id'), nullable=False)
    brothers_count = Column(Integer, default=0)
    sisters_count = Column(Integer, default=0)

    father = relationship(
        'Parent',
        foreign_keys=[father_id],
        back_populates='children_as_father',
        single_parent=True
    )

    mother = relationship(
        'Parent',
        foreign_keys=[mother_id],
        back_populates='children_as_mother',
        single_parent=True
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    @property
    def get_father_full_name(self):
        return f"{self.father.first_name} {self.father.middle_name} {self.father.last_name}"

    @property
    def get_father_income(self):
        return f"{self.father.income}"

    @property
    def get_mother_full_name(self):
        return f"{self.mother.first_name} {self.mother.middle_name} {self.mother.last_name}"

    @property
    def get_mother_income(self):
        return f"{self.mother.income}"

    @property
    def get_brothers_count(self):
        return f"{self.brothers_count}"

    @property
    def get_sisters_count(self):
        return f"{self.sisters_count}"

    def __repr__(self):
        return (
            f"Студент: {self.full_name}, \n "
            f"Отец: {self.father.full_name},\n "
            f"Мать: {self.mother.full_name} \n"
        )
