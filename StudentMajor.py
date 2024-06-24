from orm_base import Base
from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
# We canNOT import Student and Major here because Student and Major
# are both importing StudentMajor.  So we have to go without the
# ability to validate the Student or Major class references in
# this class.  Otherwise, we get a circular import.
# from Student import Student
# from Major import Major
from datetime import datetime


class StudentMajor(Base):
    """The association class between Student and Major.  I resorted to using
    this style of implementing a Many to Many because I feel that it is the
    most versatile approach, and we only have time for one Many to Many
    protocol in this class."""
    __tablename__ = "student_majors"
    major: Mapped["Major"] = relationship(back_populates="students")
    majorName: Mapped[str] = mapped_column('major_name', ForeignKey("majors.name"), primary_key=True)
    student: Mapped["Student"] = relationship(back_populates="majors")
    studentId: Mapped[int] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)
    declarationDate: Mapped[Date] = mapped_column('declaration_date', Date, nullable=False)

    def __init__(self, student, major, declaration_date: datetime):
        self.student = student
        self.major = major
        self.studentId = student.studentID
        self.majorName = major.name
        self.declarationDate = declaration_date

    def __str__(self):
        return f"Student major - student: {self.student} major: {self.major}"
