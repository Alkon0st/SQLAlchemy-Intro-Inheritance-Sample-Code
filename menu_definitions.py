from Menu import Menu
from Option import Option
"""
This little file just has the menus declared.  Each variable (e.g. menu_main) has 
its own set of options and actions.  Although, you'll see that the "action" could
be something other than an operation to perform.

Doing the menu declarations here seemed like a cleaner way to define them.  When
this is imported in main.py, these assignment statements are executed and the 
variables are constructed.  To be honest, I'm not sure whether these are global
variables or not in Python.
"""

# The main options for operating on Departments and Courses.
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(sess)"),
    Option("List", "list_objects(sess)"),
    Option("Delete", "delete(sess)"),
    Option("Boilerplate Data", "boilerplate(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Rollback", "session_rollback(sess)"),
    Option("Exit this application", "pass")
])

add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Department", "add_department(sess)"),
    Option("Course", "add_course(sess)"),
    Option("Major", "add_major(sess)"),
    Option("Student", "add_student(sess)"),
    Option("Section", "add_section(sess)"),
    Option("Student to Major", "add_student_major(sess)"),
    Option("Major to Student", "add_major_student(sess)"),
    Option("Student to Section", "add_student_section(sess)"),
    Option("Section to Student", "add_student_section(sess)"),
    Option("Student to PassFail", "add_student_PassFail(sess)"),
    Option("Exit", "pass")
])

delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Department", "delete_department(sess)"),
    Option("Course", "delete_course(sess)"),
    Option("Major", "delete_major(sess)"),
    Option("Student", "delete_student(sess)"),
    Option("Section", "delete_section(sess)"),
    Option("Student to Major", "delete_student_major(sess)"),
    Option("Major to Student", "delete_major_student(sess)"),
    Option("Student to Section", "delete_student_section(sess)"),
    Option("Section to Student", "delete_student_section(sess)"),
    Option("Exit", "pass")
])

list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Department", "list_department(sess)"),
    Option("Course", "list_course(sess)"),
    Option("Major", "list_major(sess)"),
    Option("Student", "list_student(sess)"),
    Option("Section", "list_section(sess)"),
    Option("Student to Major", "list_student_major(sess)"),
    Option("Major to Student", "list_major_student(sess)"),
    Option("Student to Section", "list_student_section(sess)"),
    Option("Section to Student", "list_section_student(sess)"),
    Option("Enrollment", "list_enrollment(sess)"),
    Option("Exit", "pass")
])

schedule_menu = Menu('schedule', 'Please indicate the section schedule:', [
    Option("Monday/Wednesday", "MW"),
    Option("Monday/Wednesday/Friday", "MWF"),
    Option("Tuesday/Thursday", "TuTh"),
    Option("Friday only", "F"),
    Option("Saturday only", "S"),
    Option("test bogus", "LOL")
])

semester_menu = Menu('semester', 'Please indicate the section semester:', [
    Option("Fall", "Fall"),
    Option("Spring", "Spring"),
    Option("Winter", "Winter"),
    Option("Summer I", "Summer I"),
    Option("Summer II", "Summer II"),
    Option("Summer III", "Summer III")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
