from collections import namedtuple
from copy import deepcopy
from tree import Tree
from itertools import chain

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
course_translation = {1: 'Frosh', 3: 'Soph', 5: 'Junior', 7: 'Senior'}
season_translation = {0: 'Spring', 1: 'Fall'}
max_semester = 8
MAX_CREDITS = 18


def flatten (list):
    toReturn = set()
    for prereqs in list:
        for course in prereqs:
            print course
            toReturn.add(course)
    return toReturn

def find_elective_groups(catalog):
    """
    Find and store electives that share prerequisites. This is a special case of high-level requirements. Since in
    normal credited courses one course can fulfill unlimited requirements but in electives one course can fulfill
    one requirement in the same group.

    :param catalog: Dictionary holding all Course (key) to CourseInfo (value) information. See above for definition of
     each.
    :return: List of groups of electives that share the same prerequisites. Ex group: [(CS, open1), (CS, open2)...]
    """
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



def get_scheduled_term(semester):
    """
    Translate indexes to expected String representation

    :param semester: Integer number of semester, 1 to max_semester
    :return: (Fall/Spring, Frosh/Soph/Junior/Semester)
    """
    season = season_translation[semester % 2]
    year = course_translation[semester if semester % 2 == 1 else semester - 1]
    return season, year


class Schedule:
    def __init__(self, course_catalog, initial_state):
        # Course catalog given in course_definitions used to lookup course information
        self.dict = course_catalog
        # Groups of high-level elective groups that must be satisfied by different courses.
        self.elective_groups = find_elective_groups(self.dict)

        # List of sets of courses scheduled for self.elective_groups
        self.electives_taken = [set() for i in range(len(self.elective_groups))]
        # All the courses scheduled so far. Stored so that we don't have to union semester sets every time.
        self.courses_taken = set(initial_state)
        # List of sets of courses scheduled for each semester. 0 is initial state, 1 to 8 (inclusive) is Fall Frosh
        # to Spring Senior.
        self.scheduled = {i: set() for i in range(max_semester + 1)}

        self.scheduled[0] = set(initial_state)

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

    def schedule(self, course, chosen_prerequisites=None):
        """
        Attempts to schedule the class in the earliest semester possible. A semester has to have less than 18 credits
        with this class scheduled, course needs to be offered in that semester, course shouldn't have been scheduled and
        the requirement for this course must have been scheduled before the semester if it's a course with credit or
        requirements can be completed during the semester if it's a high-level course.

        :param chosen_prerequisites: The prerequisite scheduled to fulfill the requirement for this course
        :param course: Course to schedule
        :return: True if course is scheduled or False if it can't be scheduled
        """
        if course in self.courses_taken:
            return True

        for i in range(1, max_semester + 1):
            if self.__can_schedule(course, i) and self.__requirements_satisfied(course, i):
                self.scheduled[i].add(course)
                self.courses_taken.add(course)

                """ 
                If the course we scheduled is a high-level elective requirement, then we want to store the course 
                we used to fulfill this elective requirement so that the course is not used again for the same elective.
                """
                if self.is_elective(course):
                    self.add_elective_course(course, chosen_prerequisites)
                return True
        return False

    def add_elective_course(self, elective, courses):
        """

        :param elective: The high-level elective requirement course is meant to fulfill.
        :param courses: The course being scheduled.
        :return: Error if given elective parameter doesn't exist in catalog as an elective
        """
        for index, group in enumerate(self.elective_groups):
            if elective in group:
                for course in courses:
                    self.electives_taken[index].add(course)
                return
        raise NameError(str(elective) + " couldn't be found in any elective groups")

    def get_total_credits(self, semester):
        """
        :param semester: Integer representation of a semester.
        :return: Return the total number of credits scheduled for a semester.
        """
        total = 0
        for course in self.scheduled[semester]:
            total += self.get_credits(course)
        return total

    def get_plan(self):
        plan = []

        for semester in range(1, max_semester + 1):
            for course in self.scheduled[semester]:
                plan.append((course, get_scheduled_term(semester), self.get_credits(course)))
        return plan

    def __is_course_offered(self, course, season):
        return season_translation[season] in self.dict[course].terms

    def __requirements_satisfied(self, course, semester):
        """
        Checks if all the prerequisites for a course is satisfied by the given semester.

        :param course: Course to schedule
        :param semester: Integer representation of the semester to schedule
        :return: Returns if all the prerequisites for a course is satisfied by the given semester.
        """
        possible_prerequisites = self.get_prereqs(course)
        courses_taken = self.scheduled[0]

        if not possible_prerequisites:
            return True

        for i in range(1, semester + (1 if self.get_credits(course) == 0 else 0)):
            courses_taken = courses_taken | self.scheduled[i]

        for prerequisites in possible_prerequisites:
            if set(prerequisites).issubset(courses_taken):
                return True
        return False

    def __can_schedule(self, course, semester):
        return self.get_total_credits(semester) + self.get_credits(course) <= MAX_CREDITS and course not in self.courses_taken \
               and self.__is_course_offered(course, semester % 2)

    def copy(self):
        return deepcopy(self.electives_taken), deepcopy(self.courses_taken), deepcopy(self.scheduled)

    def assign(self, copy):
        self.electives_taken, self.courses_taken, self.scheduled = copy

    def __str__(self):
        schedule_str = ""

        for i in range(1, max_semester + 1):
            schedule_str += str(get_scheduled_term(i)) + ": "
            schedule_str += str(list(filter(lambda course: not self.is_high_level(course), self.scheduled[i])))
            schedule_str += " Credits: " + str(self.get_total_credits(i))
            schedule_str += '\n\tDone with ' + str(
                list(filter(lambda course: self.is_high_level(course), self.scheduled[i])))
            schedule_str += '\n'

        return schedule_str

    def build_prereq_tree(self, goal_conditions):
        for course in goal_conditions:
            prereqs = self.get_prereqs(course)
            root = Tree(course)
            prereqSet = flatten(prereqs)
            if prereqSet == set():
                return root
            else:
                for prereq in prereqSet:
                    # if not self.is_elective(prereq):
                        toAdd = self.build_prereq_tree([prereq])
                        root.add_child(toAdd)
                return root


    # def have_elective_course(self, elective, courses):
    #     """
    #
    #     :param elective: Elective course that parameter courses will satisfy.
    #     :param courses: Requirement courses for the elective course
    #     :return: Return True if the parameter course is scheduled for the group elective course is in.
    #     """
    #     for index, group in enumerate(self.elective_groups):
    #         if elective in group:
    #             return courses[0] in self.electives_taken[index]
    #     raise NameError(str(elective) + " couldn't be found in any elective groups")
