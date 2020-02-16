"""
    Team Number: 10
    Members: Noah Popham, Arda Turkmen, Mark Weinstein, Harry Wilson
"""

def course_heuristic(schedule, course):
    """
    This heuristic function assigns a heuristic value to a course, based on problem details stored in the schedule class

    :param schedule: A class holding information about the current schedule we are building
    :param course: The course to assign a heuristic value to.
    :return: The heuristic value (smaller the number, higher the priority it will get in the search)
    """
    if course in schedule.heuristic_dictionary:
        return -schedule.heuristic_dictionary[course]
    return 0

