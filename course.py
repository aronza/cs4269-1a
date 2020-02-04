from course_dictionary import create_course_dict

# TODO: Parses all the entries of the dictionary from course_dictionary to Course class and returns another dictionary.
def parseDictionary():
    courses = create_course_dict()

# TODO: Define publicly available enums to map string names like program (CS, HOD, ECON), possible terms(which terms
#  this course can be taken in like Fall, Spring), scheduling terms (Freshman Fall to Senior Spring) and any other
#  that makes sense to number IDs.

class Course:

    # TODO: Takes an entry from course_dictionary and parses it.
    def __init__(self, course_entry):
        self.program = 0
        self.scheduled_term = -1
        
    #  TODO: Return a list of Course(this class) classes that this course requires
    def requirements(self):
        return 0

    # TODO: Return number of credits for the course
    def credit(self):
        return 0

    # TODO: Return the program ID for the course
    def program(self):
        return 0

    # TODO: Return the ID for the course
    def number(self):
        return 0

    # TODO: Return Term ID's for the possible terms this course can be taken in.
    def possible_terms(self):
        return 0

    # TODO: Set a term entry to self.scheduled_term from defined enum
    def scheduleTerm(self, term):
        return 0

    # TODO: Parse the Course object to String to be printed.
    def __str__(self):
        return "foo"


