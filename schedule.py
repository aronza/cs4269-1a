"""
    Team Number: 10
    Members: Noah Popham, Arda Turkmen, Mark Weinstein, Harry Wilson
"""

from collections import namedtuple
from copy import deepcopy
from tree import Tree

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
course_translation = {1: 'Frosh', 3: 'Soph', 5: 'Junior', 7: 'Senior'}
season_translation = {0: 'Spring', 1: 'Fall'}
max_semester = 8
MAX_CREDITS = 18


def flatten(list_of_lists):
    """
    Flattens a list of lists and then returns it as a set.

    :param list_of_lists: List ot flatten
    :return: A set containing every element in the given list_of_lists
    """
    flatten_list = set()
    for inner_list in list_of_lists:
        for element in inner_list:
            flatten_list.add(element)
    return flatten_list


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
    """
        A class that abstracts any detail/functionality about the scheduling problem.
        It also stores the courses scheduled so far.
    """
    def __init__(self, course_catalog, initial_state, goal_conditions):
        # Course catalog given in course_definitions used to lookup course information
        self.dict = course_catalog
        # Groups of high-level elective groups that must be satisfied by different courses.
        self.elective_groups = find_elective_groups(self.dict)
        self.heuristic_dictionary = {}
        self.goal_conditions = goal_conditions
        self.build_prereq_tree(goal_conditions)

        # List of sets of courses scheduled for self.elective_groups
        self.electives_taken = [set() for i in range(len(self.elective_groups))]
        # All the courses scheduled so far. Stored so that we don't have to union semester sets every time.
        self.courses_taken = set(initial_state)
        # List of sets of courses scheduled for each semester. 0 is initial state, 1 to 8 (inclusive) is Fall Frosh
        # to Spring Senior.
        self.scheduled = {i: set() for i in range(max_semester + 1)}

        self.scheduled[0] = set(initial_state)

    def get_prereqs(self, course):
        """
        :param course: Course to look up
        :return: Requirement list for the course
        """
        return self.dict[course].prereqs

    def get_credits(self, course):
        """
        :param course: Course to look up
        :return: Number of credits for the course
        """
        return int(self.dict[course].credits)

    def is_high_level(self, course):
        """
        :param course: Course to look up
        :return: True if course is a high-level requirement (if its credit is 0), false otherwise.
        """
        return self.get_credits(course) == 0

    def is_elective(self, course):
        """
        :param course: Course to look up
        :return: True if course belongs to a group of electives, false otherwise.
        """
        for group in self.elective_groups:
            if course in group:
                return True
        return False

    def is_program_in_goal(self, program):
        """
        Checks if a program is also the program of one of the courses in the goal

        :param program: Program to check
        :return: True if it is, false otherwise
        """
        for goal in self.goal_conditions:
            if program == goal[0]:
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
            if self.schedule_in(course, i, chosen_prerequisites):
                return True
        return False

    def schedule_in(self, course, semester, chosen_prerequisites=None):
        """Tries to schedule a course in a particular semester."""

        if self.__can_schedule(course, semester) and self.__requirements_satisfied(course, semester):
            self.scheduled[semester].add(course)
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
        """
        Returns the scheduled courses as a conjunctive list of courses as defined in the requirements

        :return: List of tuples in (course_key, scheduled_term, course_credits) format
        """
        plan = []

        for semester in range(1, max_semester + 1):
            for course in self.scheduled[semester]:
                plan.append((course, get_scheduled_term(semester), self.get_credits(course)))
        return plan

    def __is_course_offered(self, course, season):
        """
        Checks if the course can be scheduled in a given semester

        :param course: Course to check
        :param season: 0 for 'Spring', 1 for 'Fall'
        :return: True if course can be scheduled, false if it can't
        """
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
        """
        Checks if a schedule can be scheduled into a semester by following conditions:
            1. Total credits for a semester should not exceed MAX_CREDITS (defined at top) when course is added
            2. Course shouldn't already be scheduled for any semester
            3. Course should be offered in semester
        :param course: Course to be scheduled
        :param semester: 1 to MAX_SEMESTER representing which semester to schedule course
        :return: True if all above conditions are met, False otherwise
        """
        return self.get_total_credits(semester) + self.get_credits(course) <= MAX_CREDITS \
               and course not in self.courses_taken and self.__is_course_offered(course, semester % 2)

    def copy(self):
        """
        Deep copies all non-constant objects in this class to save space while copying this class
        :return: A copy of electives_taken, courses_taken, scheduled
        """
        return deepcopy(self.electives_taken), deepcopy(self.courses_taken), deepcopy(self.scheduled)

    def assign(self, copy):
        """
        Assigns back electives_taken, courses_taken, scheduled copy objects created with self.copy function.
        :return: A copy of electives_taken, courses_taken, scheduled
        """
        self.electives_taken, self.courses_taken, self.scheduled = copy

    def build_prereq_tree(self, goal_conditions):
        """
        Builds a tree of courses and their prerequisites to pre-calculate the depths of paths in the search tree.

        :param goal_conditions: @see course_scheduler(course_descriptions, goal_conditions, initial_state)
        :return: Root of the tree
        """
        for course in goal_conditions:
            prereqs = self.get_prereqs(course)
            root = Tree(course)
            prereqSet = flatten(prereqs)
            if prereqSet == set():
                root.max_depth = 0
                self.heuristic_dictionary[course] = root.max_depth
                return root
            else:
                depths = []
                for prereq in prereqSet:
                    toAdd = self.build_prereq_tree([prereq])
                    root.add_child(toAdd)
                    self.heuristic_dictionary[prereq] = toAdd.max_depth
                    depths.append(toAdd.max_depth + 1)
                root.max_depth = max(depths)

                return root

    def __str__(self):
        """
        Formats the scheduled courses into a pretty way to print.

        :return: Formatted Schedule
        """
        schedule_str = ""

        for i in range(1, max_semester + 1):
            schedule_str += str(get_scheduled_term(i)) + ": "
            schedule_str += str(list(filter(lambda course: not self.is_high_level(course), self.scheduled[i])))
            schedule_str += " Credits: " + str(self.get_total_credits(i))
            schedule_str += '\n\tDone with ' + str(
                list(filter(lambda course: self.is_high_level(course), self.scheduled[i])))
            schedule_str += '\n'

        return schedule_str


