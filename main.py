import logging
from datetime import time, datetime
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, semester_menu, schedule_menu, debug_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Department import Department
from Course import Course
from Major import Major
from Student import Student
from StudentMajor import StudentMajor
from Enrollment import Enrollment
from Section import Section
from PassFail import PassFail
from Option import Option
from Menu import Menu
from Enrollment import LetterGrade  
from pprint import pprint
from SQLAlchemyUtilities import check_unique


def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def add_department(session: Session):
    """
    Prompt the user for the information for a new department and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    name: str = ''
    abbreviation: str = ''
    violation = True
    new_department: Department = None
    while violation:                # Keep promting until we get a non-redundant department
        name = input("Department full name--> ")
        abbreviation = input("Department abbreviation--> ")
        new_department = Department(abbreviation, name)
        violated_constraints = check_unique(Session, new_department)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(new_department)



def add_course(session: Session):
    """
    This demonstrates how to use the utilities in SQLAlchemy Utilities for checking
    all the uniqueness constraints of a table in one method call.  The user
    experience is tougher to customize using this technique, but the benefit is that
    new uniqueness constraints will be automatically added to the list to be checked,
    without any change to the add_course code.

    Prompt the user for the information for a new course and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this course?")
    department: Department = select_department(sess)
    description: str = input('Please enter the course description-->')
    units: int = int(input('How many units for this course-->'))
    violation = True  # Flag that we still have to prompt for fresh values
    while violation:
        name = input("Course full name--> ")
        number = int(input("Course number--> "))
        course = Course(department, number, name, description, units)
        violated_constraints = check_unique(Session, course)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(course)

def add_letter_grade_enrollment(session: Session):
    """
    Prompt the user for the information to create a LetterGrade Enrollment
    and validate the input.
    :param session: The connection to the database.
    :return:        None
    """
    print("Adding a LetterGrade Enrollment")
    student: Student = select_student(session)
    section: Section = select_section(session)
    min_satisfactory: str = input("Enter the minimum satisfactory grade (A, B, C, D, F)--> ")

    # Ensure no existing enrollment for this student and section
    existing_enrollment = session.query(Enrollment).filter_by(
        studentID=student.studentID,
        departmentAbbreviation=section.departmentAbbreviation,
        courseNumber=section.courseNumber,
        sectionNumber=section.sectionNumber,
        semester=section.semester,
        sectionYear=section.sectionYear
    ).first()

    if existing_enrollment:
        print(f"Student {student} is already enrolled in {section}.")
        return

    new_enrollment = LetterGrade(section, student, min_satisfactory)
    session.add(new_enrollment)
    print(f"LetterGrade Enrollment added: {new_enrollment}")


def add_major(session: Session):
    """
    Prompt the user for the information for a new major and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    print("Which department offers this major?")
    department: Department = select_department(sess)
    unique_name: bool = False
    name: str = ''
    while not unique_name:
        name = input("Major name--> ")
        name_count: int = session.query(Major).filter(Major.departmentAbbreviation == department.abbreviation,
                                                      ).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a major by that name in that department.  Try again.")
    description: str = input('Please give this major a description -->')
    major: Major = Major(department, name, description)
    session.add(major)


def add_student(session: Session):
    """
    Prompt the user for the information for a new student and validate
    the input to make sure that we do not create any duplicates.
    :param session: The connection to the database.
    :return:        None
    """
    unique_name: bool = False
    unique_email: bool = False
    last_name: str = ''
    first_name: str = ''
    email: str = ''
    violation = True
    new_student: Student = None
    while violation:
        last_name = input("Student last name--> ")
        first_name = input("Student first name-->")
        email = input("Student e-mail address--> ")
        new_student = Student(last_name, first_name, email)
        violated_constraints = check_unique(Session, new_student)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('please try again.')
        else:
            violation = False
    session.add(new_student)


def add_section(session: Session):
    """
    Prompt the user for the information for a new course section
    and validate the input to make sure that we do not create any
    duplicate sections.
    :param session: The connection to the database.
    :return:        None
    """
    unique_pk: bool = False
    unique_building: bool = False
    unique_instructor: bool = False
    courseNumber: int
    sectionNumber: int
    semester: str = ''
    sectionYear: int
    building: str = ''
    room: int
    schedule: str = ''
    startTime: time
    instructor: str = ''
    violation = True
    while violation:
        print('Please provide the course that this section belongs to:')
        course: Course = select_course(session)
        sectionNumber = int(input('What is the section number -->'))
        semester = semester_menu.menu_prompt()
        sectionYear = int(input('Which year is this section offered in? --> '))
        building = input('Which building is this section offered in? --> ')
        room = int(input(f'Which room of building {building} is this section offered in? --> '))
        schedule = schedule_menu.menu_prompt()
        start_hour = int(input('Start hour --> '))
        start_minute = int(input('Start minute --> '))
        startTime = time(start_hour, start_minute)
        instructor = input('Instructor full name --> ')
        new_section = Section(course, sectionNumber, semester, sectionYear, building, room,
                              schedule, startTime, instructor)
        violated_constraints = check_unique(Session, new_section)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    session.add(new_section)


def add_student_major(sess):
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    unique_student_major: bool = False
    while not unique_student_major:
        student = select_student(sess)
        major = select_major(sess)
        student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                                   StudentMajor.majorName == major.name).count()
        unique_student_major = student_major_count == 0
        if not unique_student_major:
            print("That student already has that major.  Try again.")
    student.add_major(major)
    """The student object instance is mapped to a specific row in the Student table.  But adding
    the new major to its list of majors does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Student's majors list inside of the
    add_major method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_major method.  So instead, I add the student to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this student 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(student)  # add the StudentMajor to the session
    sess.flush()


def add_section_student(sess):
    student: Student
    section: Section
    unique_section_student: bool = False
    while not unique_section_student:
        student = select_student(sess)
        section = select_section(sess)
        pk_count: int = sess.query(Enrollment).filter(
            Enrollment.departmentAbbreviation == section.departmentAbbreviation,
            Enrollment.courseNumber == section.courseNumber,
            Enrollment.sectionNumber == section.sectionNumber,
            Enrollment.sectionYear == section.sectionYear,
            Enrollment.semester == section.semester,
            Enrollment.studentID == student.studentID).count()
        unique_section_student = pk_count == 0
        if not unique_section_student:
            print("That student is already enrolled in that class.  Try again.")
    section.add_student(student)
    sess.add(section)
    sess.flush()


def count_student_section(sess, student: Student, section: Section):
    """Count the number of Enrollment instances for a given student & section.
    :param  sess        The current session.
    :param  student     The enrolling student.
    :param  section     The section that we want to see whether that student is enrolled."""
    pk_count: int = sess.query(Enrollment).filter(
        Enrollment.departmentAbbreviation == section.departmentAbbreviation,
        Enrollment.courseNumber == section.courseNumber,
        Enrollment.sectionNumber == section.sectionNumber,
        Enrollment.sectionYear == section.sectionYear,
        Enrollment.semester == section.semester,
        Enrollment.studentID == student.studentID).count()
    return pk_count


def add_student_section(sess):
    student: Student
    section: Section
    unique_student_section: bool = False
    while not unique_student_section:
        student = select_student(sess)
        section = select_section(sess)
        pk_count: int = count_student_section(sess, student, section)
        unique_student_section = pk_count == 0
        if not unique_student_section:
            print("That section already has that student enrolled in it.  Try again.")
    student.add_section(section)
    sess.add(student)
    sess.flush()


def add_student_PassFail(sess):
    """
    Add a student to a section as a pass/fail.
    :param sess: The current database connection.
    :return:    None
    """
    student: Student
    section: Section
    unique_student_section: bool = False
    while not unique_student_section:
        student = select_student(sess)
        section = select_section(sess)
        pk_count: int = count_student_section(sess, student, section)
        unique_student_section = pk_count == 0
        if not unique_student_section:
            print("That section already has that student enrolled in it.  Try again.")
    pass_fail = PassFail(section, student, datetime.now())
    sess.add(pass_fail)
    sess.flush()


def add_major_student(sess):
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    student_major_count: int = sess.query(StudentMajor).filter(StudentMajor.studentId == student.studentID,
                                                               StudentMajor.majorName == major.name).count()
    unique_student_major: bool = student_major_count == 0
    while not unique_student_major:
        print("That major already has that student.  Try again.")
        major = select_major(sess)
        student = select_student(sess)
    major.add_student(student)
    """The major object instance is mapped to a specific row in the Major table.  But adding
    the new student to its list of students does not add the new StudentMajor instance to this session.
    That StudentMajor instance was created and added to the Major's students list inside of the
    add_student method, but we don't have easy access to it from here.  And I don't want to have to 
    pass sess to the add_student method.  So instead, I add the major to the session.  You would
    think that would cause an insert, but SQLAlchemy is smart enough to know that this major 
    has already been inserted, so the add method takes this to be an update instead, and adds
    the new instance of StudentMajor to the session.  THEN, when we flush the session, that 
    transient instance of StudentMajor gets inserted into the database, and is ready to be 
    committed later (which happens automatically when we exit the application)."""
    sess.add(major)  # add the StudentMajor to the session
    sess.flush()


def select_department(sess: Session) -> Department:
    """
    Prompt the user for a specific department by the department abbreviation.
    :param sess:    The connection to the database.
    :return:        The selected department.
    """
    found: bool = False
    abbreviation: str = ''
    while not found:
        abbreviation = input("Enter the department abbreviation--> ")
        abbreviation_count: int = sess.query(Department). \
            filter(Department.abbreviation == abbreviation).count()
        found = abbreviation_count == 1
        if not found:
            print("No department with that abbreviation.  Try again.")
    return_department: Department = sess.query(Department). \
        filter(Department.abbreviation == abbreviation).first()
    return return_department


def select_course(sess: Session) -> Course:
    """
    Select a course by the combination of the department abbreviation and course number.
    Note, a similar query would be to select the course on the basis of the department
    abbreviation and the course name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                                    Course.courseNumber == course_number).count()
        found = name_count == 1
        if not found:
            print("No course by that number in that department.  Try again.")
    course = sess.query(Course).filter(Course.departmentAbbreviation == department_abbreviation,
                                       Course.courseNumber == course_number).first()
    return course


def select_student(sess) -> Student:
    """
    Select a student by the combination of the last and first.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    last_name: str = ''
    first_name: str = ''
    while not found:
        last_name = input("Student's last name--> ")
        first_name = input("Student's first name--> ")
        name_count: int = sess.query(Student).filter(Student.lastName == last_name,
                                                     Student.firstName == first_name).count()
        found = name_count == 1
        if not found:
            print("No student found by that name.  Try again.")
    student: Student = sess.query(Student).filter(Student.lastName == last_name,
                                                  Student.firstName == first_name).first()
    return student


def select_major(sess) -> Major:
    """
    Select a major by its name.
    :param sess:    The connection to the database.
    :return:        The selected student.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Major's name--> ")
        name_count: int = sess.query(Major).filter(Major.name == name).count()
        found = name_count == 1
        if not found:
            print("No major found by that name.  Try again.")
    major: Major = sess.query(Major).filter(Major.name == name).first()
    return major


def select_section(session) -> Section:
    """
    Select a section by the primary key.
    :param session: The connection to the database.
    :return:        The selected section.
    """
    found: bool = False
    while not found:
        print('Please provide the course that this section belongs to:')
        course: Course = select_course(session)
        sectionNumber = int(input('What is the section number -->'))
        semester = semester_menu.menu_prompt()
        sectionYear = int(input('Which year is this section offered in? --> '))
        pk_count: int = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                                      Section.courseNumber == course.courseNumber,
                                                      Section.sectionNumber == sectionNumber,
                                                      Section.sectionYear == sectionYear,
                                                      Section.semester == semester).count()
        found = pk_count == 1
        if not found:
            print("No section found by that course, section#, semester & year.  Try again.")
    section: Section = session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                                     Section.courseNumber == course.courseNumber,
                                                     Section.sectionNumber == sectionNumber,
                                                     Section.sectionYear == sectionYear,
                                                     Section.semester == semester).first()
    return section


def delete_student(session: Session):
    """
    Prompt the user for a student to delete and delete them.
    :param session:     The current connection to the database.
    :return:            None
    """
    student: Student = select_student(session)
    """This is a bit ghetto.  The relationship from Student to StudentMajor has 
    cascade delete, so this delete will work even if a student has declared one
    or more majors.  I could write a method on Student that would return some
    indication of whether it has any children, and use that to let the user know
    that they cannot delete this particular student.  But I'm too lazy at this
    point.
    """
    session.delete(student)


def delete_department(session: Session):
    """
    Prompt the user for a department by the abbreviation and delete it.
    :param session: The connection to the database.
    :return:        None
    """
    print("deleting a department")
    department = select_department(session)
    n_courses = session.query(Course).filter(Course.departmentAbbreviation == department.abbreviation).count()
    if n_courses > 0:
        print(f"Sorry, there are {n_courses} courses in that department.  Delete them first, "
              "then come back here to delete the department.")
    else:
        session.delete(department)


def delete_student_major(sess):
    """Undeclare a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the major that they no longer have.")
    student: Student = select_student(sess)
    major: Major = select_major(sess)
    student.remove_major(major)


def delete_major_student(sess):
    """Remove a student from a particular major.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the major and the student who no longer has that major.")
    major: Major = select_major(sess)
    student: Student = select_student(sess)
    major.remove_student(student)


def delete_student_section(sess):
    """Remove a student from a particular class.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the student and the class they are dropping.")
    student: Student = select_student(sess)
    section: Section = select_section(sess)
    student.remove_section(section)


def delete_section_student(sess):
    """Remove a student from a particular class.
    :param sess:    The current database session.
    :return:        None
    """
    print("Prompting you for the class and the student dropping that class.")
    section: Section = select_section(sess)
    student: Student = select_student(sess)
    section.remove_student(student)


def list_department(session: Session):
    """
    List all departments, sorted by the abbreviation.
    :param session:     The connection to the database.
    :return:            None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    departments: [Department] = list(session.query(Department).order_by(Department.abbreviation))
    for department in departments:
        print(department)


def list_course(sess: Session):
    """
    List all courses currently in the database.
    :param sess:    The connection to the database.
    :return:        None
    """
    # session.query returns an iterator.  The list function converts that iterator
    # into a list of elements.  In this case, they are instances of the Student class.
    courses: [Course] = list(sess.query(Course).order_by(Course.courseNumber))
    for course in courses:
        print(course)


def list_student(sess: Session):
    """
    List all Students currently in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    students: [Student] = list(sess.query(Student).order_by(Student.lastName, Student.firstName))
    for student in students:
        print(student)


def list_major(sess: Session):
    """
    List all majors in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    majors: [Major] = list(sess.query(Major).order_by(Major.departmentAbbreviation))
    for major in majors:
        print(major)


def list_section(sess: Session):
    """
    List all of the sections in the database.
    :param sess:    The current connection to the database.
    :return:
    """
    sections: [Section] = list(sess.query(Section).order_by(Section.departmentAbbreviation,
                                                            Section.courseNumber,
                                                            Section.sectionNumber,
                                                            Section.sectionYear,
                                                            Section.semester))
    for section in sections:
        print(section)


def list_student_major(sess: Session):
    """Prompt the user for the student, and then list the majors that the student has declared.
    :param sess:    The connection to the database
    :return:        None
    """
    student: Student = select_student(sess)
    recs = sess.query(Student).join(StudentMajor, Student.studentID == StudentMajor.studentId).join(
        Major, StudentMajor.majorName == Major.name).filter(
        Student.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_major_student(sess: Session):
    """Prompt the user for the major, then list the students who have that major declared.
    :param sess:    The connection to the database.
    :return:        None
    """
    major: Major = select_major(sess)
    recs = sess.query(Major).join(StudentMajor, StudentMajor.majorName == Major.name).join(
        Student, StudentMajor.studentId == Student.studentID).filter(
        Major.name == major.name).add_columns(
        Student.lastName, Student.firstName, Major.description, Major.name).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, Major: {stu.name}, Description: {stu.description}")


def list_student_section(sess: Session):
    """Prompt the user for the student, then list the sections they are enrolled in.
    :param sess:    The connection to the database.
    :return:        None
    """
    student: Student = select_student(sess)
    # I went old school with this because I was unable to find a way to get the join to work
    # when I had multiple columns in the ON clause.  Essentially this join does a Cartesian
    # product between Student, Enrollment, & Section & then uses the filter to correlate
    # between them based on migrated foreign keys.
    recs = sess.query(Student, Enrollment, Section).filter(
        Student.studentID == Enrollment.studentID,
        Enrollment.departmentAbbreviation == Section.departmentAbbreviation,
        Enrollment.courseNumber == Section.courseNumber,
        Enrollment.sectionNumber == Section.sectionNumber,
        Enrollment.sectionYear == Section.sectionYear,
        Enrollment.semester == Section.semester,
        Enrollment.studentID == student.studentID).add_columns(
        Student.lastName, Student.firstName, Section.departmentAbbreviation,
        Section.courseNumber, Section.sectionNumber, Section.sectionYear,
        Section.semester).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, " +
              f"Course#: {stu.courseNumber}, Section: {stu.sectionNumber}")


def list_section_student(sess: Session):
    """Prompt the user for the section, then list the students that are enrolled.
    :param sess:    The connection to the database.
    :return:        None
    """
    section: Section = select_section(sess)
    # I went old school with this because I was unable to find a way to get the join to work
    # when I had multiple columns in the ON clause.  Essentially this join does a Cartesian
    # product between Student, Enrollment, & Section & then uses the filter to correlate
    # between them based on migrated foreign keys.
    recs = sess.query(Section, Enrollment, Student).filter(
        Student.studentID == Enrollment.studentID,
        Enrollment.departmentAbbreviation == Section.departmentAbbreviation,
        Enrollment.courseNumber == Section.courseNumber,
        Enrollment.sectionNumber == Section.sectionNumber,
        Enrollment.sectionYear == Section.sectionYear,
        Enrollment.semester == Section.semester,
        Section.departmentAbbreviation == section.departmentAbbreviation,
        Section.courseNumber == section.courseNumber,
        Section.sectionNumber == section.sectionNumber,
        Section.sectionYear == section.sectionYear,
        Section.semester == section.semester).add_columns(
        Student.lastName, Student.firstName, Section.departmentAbbreviation,
        Section.courseNumber, Section.sectionNumber, Section.sectionYear,
        Section.semester).all()
    for stu in recs:
        print(f"Student name: {stu.lastName}, {stu.firstName}, " +
              f"Course#: {stu.courseNumber}, Section: {stu.sectionNumber} " +
              f"Year: {stu.sectionYear} Semester: {stu.semester}")


def list_enrollment(sess: Session):
    """
    List out all enrollment records sorted by department, course,
    section number.
    :param sess:    The current connection.
    :return:        None
    """
    recs = sess.query(Enrollment).order_by(Enrollment.departmentAbbreviation,
                                           Enrollment.courseNumber,
                                           Enrollment.sectionYear).all()
    for rec in recs:
        print(rec)


def move_course_to_new_department(sess: Session):
    """
    Take an existing course and move it to an existing department.  The course has to
    have a department when the course is created, so this routine just moves it from
    one department to another.

    The change in department has to occur from the Course end of the association because
    the association is mandatory.  We cannot have the course not have any department for
    any time the way that we would if we moved it to a new department from the department
    end.

    Also, the change in department requires that we make sure that the course will not
    conflict with any existing courses in the new department by name or number.
    :param sess:    The connection to the database.
    :return:        None
    """
    print("Input the course to move to a new department.")
    course = select_course(sess)
    old_department = course.department
    print("Input the department to move that course to.")
    new_department = select_department(sess)
    if new_department == old_department:
        print("Error, you're not moving to a different department.")
    else:
        # check to be sure that we are not violating the {departmentAbbreviation, name} UK.
        name_count: int = sess.query(Course).filter(Course.departmentAbbreviation == new_department.abbreviation,
                                                    Course.name == course.name).count()
        unique_name = name_count == 0
        if not unique_name:
            print("We already have a course by that name in that department.  Try again.")
        if unique_name:
            # Make sure that moving the course will not violate the {departmentAbbreviation,
            # course number} uniqueness constraint.
            number_count = sess.query(Course). \
                filter(Course.departmentAbbreviation == new_department.abbreviation,
                       Course.courseNumber == course.courseNumber).count()
            if number_count != 0:
                print("We already have a course by that number in that department.  Try again.")
            else:
                course.set_department(new_department)


def select_student_from_list(session):
    """
    This is just a cute little use of the Menu object.  Basically, I create a
    menu on the fly from data selected from the database, and then use the
    menu_prompt method on Menu to display characteristic descriptive data, with
    an index printed out with each entry, and prompt the user until they select
    one of the Students.
    :param session:     The connection to the database.
    :return:            None
    """
    # query returns an iterator of Student objects, I want to put those into a list.  Technically,
    # that was not necessary, I could have just iterated through the query output directly.
    students: [Department] = list(sess.query(Department).order_by(Department.lastName, Department.firstName))
    options: [Option] = []  # The list of menu options that we're constructing.
    for student in students:
        # Each time we construct an Option instance, we put the full name of the student into
        # the "prompt" and then the student ID (albeit as a string) in as the "action".
        options.append(Option(student.lastName + ', ' + student.firstName, student.studentId))
    temp_menu = Menu('Student list', 'Select a student from this list', options)
    # text_studentId is the "action" corresponding to the student that the user selected.
    text_studentId: str = temp_menu.menu_prompt()
    # get that student by selecting based on the int version of the student id corresponding
    # to the student that the user selected.
    returned_student = sess.query(Department).filter(Department.studentId == int(text_studentId)).first()
    # this is really just to prove the point.  Ideally, we would return the student, but that
    # will present challenges in the exec call, so I didn't bother.
    print("Selected student: ", returned_student)


def list_department_courses(sess):
    department = select_department(sess)
    dept_courses: [Course] = department.get_courses()
    print("Course for department: " + str(department))
    for dept_course in dept_courses:
        print(dept_course)


def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department('CECS', 'Computer Engineering Computer Science')
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    course1: Course = Course(department, 323, "Database Design Fundamentals",
                             "Basics of database design", 3)
    course2: Course = Course(department, 174, "Intro to Programming",
                             "First real programming course", 3)
    section1: Section = Section(course1, 1, 'Fall', 2023, 'ECS', 416, 'MW', time(8, 0, 0), 'Brown')
    sess.add(department)
    sess.add(course1)
    sess.add(course2)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.add(section1)
    sess.flush()  # Force SQLAlchemy to update the database, although not commit


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
