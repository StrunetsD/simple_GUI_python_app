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
        foreign_keys='Student.father_id'
    )

    children_as_mother = relationship(
        'Student',
        back_populates='mother',
        foreign_keys='Student.mother_id'
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def __repr__(self):
        return f"<Parent(id={self.id}, name={self.first_name}, gender={self.gender})>"


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
        back_populates='children_as_father'
    )

    mother = relationship(
        'Parent',
        foreign_keys=[mother_id],
        back_populates='children_as_mother'
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"

    def __repr__(self):
        return (
            f"<Student(id={self.id}, "
            f"name={self.full_name}, "
            f"father={self.father.full_name}, "
            f"mother={self.mother.full_name})>"
        )
