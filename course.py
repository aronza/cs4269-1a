from course_dictionary import create_course_dict

#TODO: Define publicly avaialble enums to map string names like program, term and such to number ids.

class Course:

    def __init__(self):
        courses = create_course_dict()

    #  TODO: Return a list of Course classes that this course requires
    def requirements(self):
        return 0

    # TODO: Return number of credits for the course
    def credit(self):
        return 0

    # TODO: Return the program id for the course
    def program(self):
        return 0

    # TODO: Return the id for the course
    def number(self):
        return 0

    # TODO: Return Term id for the course
    def terms(self):
        return 0

