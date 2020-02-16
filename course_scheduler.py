"""
    Team Number: 10
    Members: Noah Popham, Arda Turkmen, Mark Weinstein, Harry Wilson
"""

import sys
import heapq

from course_heuristic import course_heuristic
from schedule import Schedule

DEBUG = (sys.argv[1] == "debug") if len(sys.argv) > 1 else False


def log(msg=""):
    """
    Helper Function to print out a debugging message if DEBUG mode is on. (Any parameters are given to program)

    :param msg: Message to be printed
    """
    if DEBUG:
        print(msg)


def append_to_queue(frontier, courses, schedule):
    """
    Add a list of courses to the search queue after assigning each a heuristic value

    :param frontier: The priority queue to add courses to
    :param courses: A list of courses to be added
    :param schedule: @see schedule.py
    """
    for course in courses:
        if course not in frontier:
            value = course_heuristic(schedule, course)
            heapq.heappush(frontier, (value, course))


def search(frontier, schedule):
    """
    Searches for a viable schedule to contain goal conditions in frontier. Recursive calls are made to schedule
     requirements. Requirements are given as new goal conditions

    :param frontier: Priority queue holding all the courses that have to be scheduled to fulfill goal_conditions
    :param schedule: Schedule object that holds course catalog information and storage for courses found and stored so
    far.
    :return: True if a scheduled found to fulfill all goal conditions, false if none can be found.
    """
    while frontier:  # AND
        log()
        log("Frontier")
        log(frontier)

        course = heapq.heappop(frontier)[1]
        log("Sub-goal chosen")
        log(course)

        possible_prerequisites = schedule.get_prereqs(course)
        chosen_prerequisites = None

        """
            Try all possible sets of prerequisites for the current course
        """
        for prerequisites in possible_prerequisites:  # OR
            """ 
                If this is an elective and we already have this specific requirement than look for another            
            """
            if schedule.is_elective(course) and set(prerequisites).issubset(schedule.courses_taken):
                continue

            prerequisites = set(prerequisites).difference(schedule.courses_taken)

            """ 
                If we already satisfy all the requirement for this course, we can go ahead and schedule it.            
            """
            if not prerequisites:
                break

            schedule_copy = schedule.copy()
            new_frontier = []
            append_to_queue(new_frontier, prerequisites, schedule)

            log("Trying Prerequisite")
            log(str(prerequisites))

            if search(new_frontier, schedule):
                chosen_prerequisites = prerequisites
                break
            else:
                schedule.assign(schedule_copy)
                log("Child returned false")

        """ By here we either have the requirements for this course or tried all possible requirement for this course. 
            If we still can't schedule it, then we failed to schedule it and must return False up the tree
        """
        if not schedule.schedule(course, chosen_prerequisites):
            log("Couldn't schedule " + str(course))
            log(schedule)
            return False

        log("New Schedule")
        log(schedule)

    return True


def course_scheduler(course_descriptions, goal_conditions, initial_state):
    """
    State consists of a conjunction of courses/high-level requirements that are to be achieved.
    When conjunction set is empty a viable schedule should be in the schedule_set.

    :param course_descriptions: Course catalog. A Python dictionary that uses Course as key and CourseInfo as value
    :param goal_conditions: A list of courses or high-level requirements that a viable schedule would need to fulfill
    :param initial_state: A list of courses the student has already taken
    :return: A List of scheduled courses in format (course, scheduled_term, course_credits)
    """
    depths = range(1, 9)
    best_schedule = None
    best_schedule_num = float('inf')

    for depth in depths:
        schedule = Schedule(course_descriptions, initial_state, goal_conditions)
        schedule.max_semester = depth

        frontier = []
        append_to_queue(frontier, goal_conditions, schedule)
        search(frontier, schedule)

        if 0 < schedule.num_of_courses_scheduled() < best_schedule_num:
            best_schedule = schedule
            best_schedule_num = schedule.num_of_courses_scheduled()

    print("num of courses: ")
    print(best_schedule.num_of_courses_scheduled())

    return best_schedule
