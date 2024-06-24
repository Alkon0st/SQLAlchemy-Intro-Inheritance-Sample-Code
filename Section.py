from typing import List
from orm_base import Base
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Course import Course
from Enrollment import Enrollment
from datetime import time


class Section(Base):
    """An offering of a Course in a specific place and time."""
    __tablename__ = "sections"
    course: Mapped["Course"] = relationship(back_populates="sections")
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation",
                                                        primary_key=True)
    courseNumber: Mapped[int] = mapped_column("course_number",
                                              primary_key=True)
    sectionNumber: Mapped[int] = mapped_column("section_number",
                                               primary_key=True)
    semester: Mapped[str] = mapped_column("semester", String(20),
                                          CheckConstraint("semester IN('Fall', 'Spring', 'Winter',\
 'Summer I', 'Summer II', 'Summer III')", name="sections_semester_constraint"),
                                          primary_key=True)
    sectionYear: Mapped[int] = mapped_column("section_year", nullable=False,
                                             primary_key=True)
    building: Mapped[str] = mapped_column("building", String(10))
    room: Mapped[int] = mapped_column("room")
    schedule: Mapped[str] = mapped_column("schedule",
                                          CheckConstraint("schedule IN('MW', 'MWF', 'TuTh', 'F', 'S')",
                                                          name="sections_schedule_constraint"))
    startTime: Mapped[time] = mapped_column("start_time")
    instructor: Mapped[str] = mapped_column("instructor", String(80))
    students: Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                        cascade="all, save-update, delete-orphan")

    __table_args__ = (UniqueConstraint("semester", "section_year", "schedule",
                                       "start_time", "building", "room",
                                       name="sections_uk_01"),
                      UniqueConstraint("semester", "section_year", "schedule",
                                       "start_time", "instructor",
                                       name="sections_uk_02"),
                      ForeignKeyConstraint([departmentAbbreviation, courseNumber],
                                           [Course.departmentAbbreviation,
                                            Course.courseNumber],
                                           name="sections_courses_fk_01"))

    def __init__(self, course: Course, sectionNumber: int, semester: str,
                 sectionYear: int, building: str, room: int, schedule: str,
                 startTime: time, instructor: str):
        self.departmentAbbreviation = course.departmentAbbreviation
        self.courseNumber = course.courseNumber
        self.sectionNumber = sectionNumber
        self.semester = semester
        self.sectionYear = sectionYear
        self.building = building
        self.room = room
        self.schedule = schedule
        self.startTime = startTime
        self.instructor = instructor

    def add_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                return
        enrollment = Enrollment(self, student)

    def remove_student(self, student):
        for next_student in self.students:
            if next_student.student == student:
                self.students.remove(next_student)
                return

    def __str__(self):
        return f"Section: dept: {self.departmentAbbreviation} course#: {self.courseNumber} " + \
               f"Section#: {self.sectionNumber} semester: {self.semester} year:{self.sectionYear}"
