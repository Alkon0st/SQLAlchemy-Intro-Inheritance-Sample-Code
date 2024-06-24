from orm_base import Base
from sqlalchemy import String, ForeignKeyConstraint, ForeignKey, Integer, Identity, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship


# Note that I do NOT migrate in any other classes in Enrollment.  I had to do that
# to avoid a cyclic import situation where Section imports Enrollment and Enrollment
# imports Section.


class Enrollment(Base):
    """An agreement between the university and a student that allows that student
    to participate in a specific section."""
    __tablename__ = "enrollments"
    # Enrollment has 6 columns in its primary key.  Time for a surrogate.
    enrollmentId: Mapped[int] = mapped_column('enrollment_id', Integer, Identity(start=1, cycle=True),
                                              primary_key=True)
    section: Mapped["Section"] = relationship(back_populates="students")
    # I decided to demonstrate that you COULD do the relationship from Section to
    # Enrollment without resorting to a surrogate in Section.  Rather a lot of work
    # to do so, but it IS possible, as you can see below.
    departmentAbbreviation: Mapped[str] = mapped_column("department_abbreviation",
                                                        nullable=False)
    courseNumber: Mapped[int] = mapped_column("course_number",
                                              nullable=False)
    sectionNumber: Mapped[int] = mapped_column("section_number",
                                               nullable=False)
    # Since no one will input the semester directly (it comes from Section), I
    # am removing the check constraint as it would be redundant.  The check
    # constraint here could get out of sync with the one in Section
    semester: Mapped[str] = mapped_column("semester", String(20),
                                          nullable=False)
    sectionYear: Mapped[int] = mapped_column("section_year", nullable=False)
    student: Mapped["Student"] = relationship(back_populates="sections")
    studentID: Mapped[int] = mapped_column("student_id", ForeignKey("students.student_id"),
                                           nullable=False)
    type: Mapped[str] = mapped_column("type", String(50), nullable=False)
    # You'll notice that the elements in the two lists for the foreign key constraint are
    # all strings.  Normally we would put a list of the migrated OO attributes in the
    # first list, and in the second list you would call out Parent.primary_key_attribute
    # for each of the primary key attributes migrating down from the parent.  But we
    # cannot do that here because that would require that we import Section from Section
    # here in Enrollments.  That, in turn, would cause a cyclic import since we have to
    # import Enrollment in Section so that adding a student to a Section can create an
    # instance of Enrollment using Enrollment's constructor.
    # Using character strings this way means that SQLAlchemy is not able to resolve these
    # names right away, which works fine for us.  I found that if I used the OO attribute
    # names, I got errors, and I'm not able to tell you why that is.  BUT, if I used the
    # table column names, that worked.  Not sure what the deep reason for that is.
    __table_args__ = (UniqueConstraint("department_abbreviation", "course_number",
                                       "section_number", "section_year", "semester",
                                       "student_id", name="enrollment_uk_01"),
                      ForeignKeyConstraint(["department_abbreviation", "course_number",
                                            "section_number", "semester", "section_year"],
                                           ["sections.department_abbreviation",
                                            "sections.course_number", "sections.section_number",
                                            "sections.semester", "sections.section_year"],
                                           name="enrollments_sections_fk_01"),)
    __mapper_args__ = {"polymorphic_identity": "enrollment",
                       "polymorphic_on": "type"}

    def __init__(self, section, student):
        self.section = section
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionNumber = section.sectionNumber
        self.semester = section.semester
        self.sectionYear = section.sectionYear
        self.student = student
        self.studentID = student.studentID

    def __str__(self):
        return f"Enrollment- section: {self.section} student: {self.student}"
