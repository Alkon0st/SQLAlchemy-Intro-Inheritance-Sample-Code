from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, Identity
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List                 # Use this for the list of courses offered by the department


class Department(Base):
    """An organization within a particular college within a university.  Each
    department offers one or more major fields of study to its students, and
    within each major, some number of courses.  Each course is offered on
    a regular basis as a scheduled section of a given course.

    Note, this is just a shell of the Department class.  There are additional
    columns needed, but this is enough to demonstrate one-to-many relationships."""
    __tablename__ = "departments"  # Give SQLAlchemy th name of the table.
    abbreviation: Mapped[str] = mapped_column('abbreviation', String,
                                              nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    # The list of majors in this department
    majors: Mapped[List["Major"]] = relationship(back_populates="department")
    # The list of courses offered by this department
    courses: Mapped[List["Course"]] = relationship(back_populates="department")
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want two separate uniqueness
    # constraints (candidate keys).
    __table_args__ = (UniqueConstraint("name", name="departments_uk_01"), )

    def __init__(self, abbreviation: str, name: str):
        self.abbreviation = abbreviation
        self.name = name

    def add_course(self, course):
        if course not in self.courses:
            self.courses.add(course)            # I believe this will update the course as well.

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department abbreviation: {self.abbreviation} name: {self.name} number course offered: {len(self.courses)}"
