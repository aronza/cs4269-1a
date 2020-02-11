
from collections import namedtuple
Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')


class Schedule:
    def __init__(self, initial_state, course_catalog):
        self.dict = course_catalog
        self.scheduled = {0: initial_state, 1: [] , 2: [] , 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self.course_translation = {'Frosh': 1, 'Soph': 3, 'Junior': 5, 'Senior': 7}
        # for key in self.dict:
        #     print(key, self.dict[key])
        # Course = namedtuple('Course', 'program, designation')
        # CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')

    def get_prereqs(self, course):
        return self.dict.get(course).prereqs

    def schedule_course(self, course, year, semester):
        if semester == 'Fall':
            self.scheduled[self.course_translation[year]].append(course)
        else:
            self.scheduled[self.course_translation[year] + 1].append(course)






