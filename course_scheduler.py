from collections import namedtuple
from pprint import pprint

from course_dictionary import create_course_dict


course_dict = create_course_dict()

Course = namedtuple('Course', 'program, designation')

key = Course('CS', '3251')
pprint(course_dict[key])

def course_scheduler (course_descriptions, goal_conditions, initial_state):

    return 0
