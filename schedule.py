import string
from collections import namedtuple
from pprint import pprint

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
course_translation = {1: 'Frosh', 3: 'Soph', 5: 'Junior', 7: 'Senior'}
season_translation = {0: 'Spring', 1: 'Fall'}
max_semester = 8


def find_groups(catalog):
    reverse_catalog = {}
    for key in catalog:
        if catalog[key].credits == '0':
            if catalog[key] in reverse_catalog:
                reverse_catalog[catalog[key]].append(key)
            else:
                reverse_catalog[catalog[key]] = [key]

    groups = []
    for key in reverse_catalog:
        if len(reverse_catalog[key]) > 1:
            groups.append(reverse_catalog[key])

    return groups


class Schedule:
    def __init__(self, course_catalog, initial_state):
        self.dict = course_catalog
        self.elective_groups = find_groups(self.dict)

        self.courses_taken = set(initial_state)
        self.electives_taken = [set() for i in range(len(self.elective_groups))]
        self.scheduled = {0: set(initial_state), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(),
                          8: set()}

    def get_prereqs(self, course):
        return self.dict[course].prereqs

    def get_credits(self, course):
        return int(self.dict[course].credits)

    def is_high_level(self, course):
        return self.get_credits(course) == 0

    def is_elective(self, course):
        for group in self.elective_groups:
            if course in group:
                return True
        return False

    def schedule(self, course):
        if course in self.courses_taken:
            return True

        for i in range(1, max_semester + 1):
            if self.__can_schedule(course, i) and self.__requirements_satisfied(course, i):
                self.scheduled[i].add(course)
                self.courses_taken.add(course)

                return True
        return False
        # raise NameError(str(course) + " couldn't be scheduled in bound 8")

    def have_elective_course(self, elective, courses):
        for index, group in enumerate(self.elective_groups):
            if elective in group:
                return courses[0] in self.electives_taken[index]
        raise NameError(str(elective) + " couldn't be found in any elective groups")

    def add_elective_course(self, elective, courses):
        for index, group in enumerate(self.elective_groups):
            if elective in group:
                self.electives_taken[index].add(courses[0])
                if len(courses) > 1:
                    raise NameError("Courses have multiple courses " + str(courses))
                return
        raise NameError(str(elective) + " couldn't be found in any elective groups")

    def get_total_credits(self, semester):
        total = 0
        for course in self.scheduled[semester]:
            total += self.get_credits(course)
        return total

    def __is_course_offered(self, course, season):
        terms = self.dict[course].terms
        return season_translation[season] in terms

    def __requirements_satisfied(self, course, semester):
        possible_prerequisites = self.get_prereqs(course)
        courses_taken = self.scheduled[0]

        if not possible_prerequisites:
            return True

        for i in range(1, semester + (1 if self.get_credits(course) == 0 else 0)):
            courses_taken = courses_taken | self.scheduled[i]

        for prerequisites in possible_prerequisites:
            if set(prerequisites) - courses_taken == set():
                return True
        return False

    def __can_schedule(self, course, semester):
        return self.get_total_credits(semester) + self.get_credits(course) <= 18 and self.not_have_course(course) \
               and self.__is_course_offered(course, semester % 2)

    def not_have_course(self, course):
        for key in self.scheduled:
            if course in self.scheduled[key]:
                return False
        return True

    def __str__(self):
        schedule_str = ""

        for i in range(1, 9):
            season = season_translation[i % 2]
            year = course_translation[i if i % 2 == 1 else i - 1]
            schedule_str += season + ", " + year + ": "
            schedule_str += str(list(filter(lambda course: not self.is_high_level(course), self.scheduled[i])))
            schedule_str += " Credits: " + str(self.get_total_credits(i))
            schedule_str += '\n\tDone with ' + str(
                list(filter(lambda course: self.is_high_level(course), self.scheduled[i])))
            schedule_str += '\n'

        return schedule_str
