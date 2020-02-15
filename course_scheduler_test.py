import sys
import os
import re
from collections import namedtuple
from pprint import pprint
import warnings

from openpyxl import load_workbook

from course_scheduler import course_scheduler

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')


def create_course_dict(file_path="data/CourseCatalogSpring2020.xlsx"):
    """
    Creates a dictionary containing course info.
    Keys: namedtuple of the form ('program, designation')
    Values: namedtuple of the form('name, prereqs, credits')
            prereqs is a tuple of prereqs where each prereq has the same form as the keys
    """
    wb = load_workbook(file_path)
    catalog = wb.get_sheet_by_name('catalog')

    course_dict = {}
    for row in range(1, catalog.max_row + 1):
        key = Course(get_val(catalog, 'A', row), get_val(catalog, 'B', row))
        prereqs = tuple(tuple(get_split_course(prereq) for prereq in prereqs.split())
                        for prereqs in none_split(get_val(catalog, 'E', row)))
        val = CourseInfo(get_val(catalog, 'C', row), tuple(get_val(catalog, 'D', row).split()), prereqs)
        course_dict[key] = val
    return course_dict


def get_split_course(course):
    """
    Parses a course from programdesignation into the ('program, designation') form.
    e.g. 'CS1101' -> ('CS', '1101')
    """
    return tuple(split_course for course_part in re.findall('((?:[A-Z]+-)?[A-Z]+)(.+)', course)
                 for split_course in course_part)


def none_split(val):
    """Handles calling split on a None value by returning the empty list."""
    return val.split(', ') if val else ()


def get_val(catalog, col, row):
    """Returns the value of a cell."""
    return catalog[col + str(row)].value


def print_dict(dict):
    """Simply prints a dictionary's key and values line by line."""
    for key in dict:
        print(key, dict[key])


def test(test_file_path, expected_result):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        catalog = create_course_dict(test_file_path)

        schedule = course_scheduler(course_descriptions=catalog, goal_conditions=[('CS', 'major')], initial_state=[])
        courses_scheduled = set(map(lambda scheduled_course: scheduled_course[0], schedule))

        if expected_result == "empty":
            return courses_scheduled == set()
        if expected_result == "have_all":
            return catalog.keys() == courses_scheduled
        raise NameError(expected_result + " is not a valid test option")


def main(argv):
    test = create_course_dict()

    # Test to see if all prereqs are in the file.
    prereq_list = [single_course for vals in test.values()
                   for some_prereqs in vals.prereqs for single_course in some_prereqs]
    for prereq in prereq_list:
        if prereq not in test:
            print(prereq)
    for key in test:
        # Test to see if every course has a term and credits.
        if not test[key].terms or not test[key].credits:
            print(key)
        # Test to see if a course's prereqs include the course itself
        if key in [course for prereq in test[key].prereqs for course in prereq]:
            print(key)

    # # Prints all the CS courses.
    # for key in test:
    #     print(key, test[key])

    # Prints the entire dictionary.
    # print_dict(test)
    # print(test[('CS', 'open3')])
    # print('Done')

    goal = [('CS', 'major')]
    courses_taken = []
    print("First search: ")
    print("Goal: " + str(goal))
    print("Initial State: " + str(courses_taken))
    print()
    schedule = course_scheduler(course_descriptions=test, goal_conditions=goal, initial_state=courses_taken)
    print()
    print("Result:")
    if type(schedule) is list:
        pprint(schedule)
    else:
        print(schedule)


if __name__ == "__main__":
    TEST = (sys.argv[1] == "test") if len(sys.argv) > 1 else False

    if TEST:
        test_folder = os.path.join(os.path.dirname(__file__), 'data/test_cases/')

        for test_filename in os.listdir(test_folder):
            file_path = os.path.join(test_folder, test_filename)

            expected = None
            if test_filename == "test_no_solution.xlsx":
                expected = "empty"
            else:
                expected = "have_all"

            print("Test " + expected + " " + file_path)
            test_result = test(file_path, expected)
            print("\tPASS" if test_result else "\tFAIL")
    else:
        main(sys.argv)
