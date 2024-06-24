from typing import List                     # So that we can manage the list of Students in this Major
from orm_base import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from Department import Department
from datetime import datetime
# I have to import StudentMajor because I need to create an instance of StudentMajor
# and hence I need its constructor.  But StudentMajor canNOT import Major or that
# would create a cyclic import.
from StudentMajor import StudentMajor


class Major(Base):
    """A distinct field of study.  Each major has a degree program that a student
    can pursue towards a college diploma.  Many universities offer specializations
    within a major to accommodate students who have a more focused set of
    objectives for their education.  Several Departments have multiple majors.
    For instance the CECS department has both a Computer Engineering as well as
    a Computer Science major."""
    __tablename__ = "majors"
    department: Mapped[Department] = relationship(back_populates="majors")
    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation',
                                                        ForeignKey("departments.abbreviation"),
                                                        primary_key=False)
    # The major name is unique across the entire college.  The Department is
    # NOT a namespace for the majors.  --> The relationship from Department to Major is
    # NON-identifying.  Makes it easier for the many to many since this is not a composite PK.
    name: Mapped[str] = mapped_column('name', String(50), nullable=False, primary_key=True)
    description: Mapped[str] = mapped_column('description', String(500), nullable=False)
    """We need to be able to delete the association class rows without using session.delete.
    The way that we will DISassociate a Major from a Student is to delete an instance
    of this list of StudentMajors that connects this Major to the Student that we want
    to disassociate.  But to get that to work in the database, we need to configure
    the relationship such that breaking the association at this end propagates a 
    deletion in the association table to go along with it."""
    students: Mapped[List["StudentMajor"]] = relationship(back_populates="major",
                                                          cascade="all, save-update, delete-orphan")

    def set_department(self, department: Department):
        """
        The Major has to have the department OO attribute set, as well as the
        migrated foreign key coming down from Department.  Since they both
        have to happen in tandem, I thought to make this a method to encapsulate
        the fact that we are getting the abbreviation from the Department object.
        :param department:  The Department object that offers this Major
        :return:            None
        """
        self.department = department
        self.departmentAbbreviation = department.abbreviation

    def __init__(self, department: Department, name: str, description: str):
        self.set_department(department)
        self.name = name
        self.description = description

    def add_student(self, student):
        """Add a new student to the list of students in the major.  We are not adding a
        Student per se, but rather creating an instance of StudentMajor, and adding that
        new instance to our list of "students".  A parallel construct will exist on the
        Student side to manage instances of StudentMajor to keep track of the various
        major(s) that the student has.
        """
        # Make sure that this Major does not already have this Student.
        for next_student in self.students:
            if next_student.student == student:
                return              # This student is already in this major.
        # create the necessary Association Class instance that connects This major to
        # the supplied student.
        student_major = StudentMajor(student, self, datetime.now())
#        student.majors.append(student_major)        # Add this new junction entry to the Student
#        self.students.append(student_major)         # Add this new junction entry to this Major

    def remove_student(self, student):
        """Remove a student from this major, and remove this major from that student.
        :param student:     The Student to be removed from this major.
        :return:            None
        """
        for next_student in self.students:
            if next_student.student == student:
                # Remove this major from the student's list of majors.
                self.students.remove(next_student)
                return

    def __str__(self):
        return f"Major: Department - {self.departmentAbbreviation} Major Name: {self.name}"