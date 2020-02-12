from pprint import pprint
import sys
import heapq
from copy import deepcopy

from course_heuristic import course_heuristic
from schedule import Schedule

DEBUG = len(sys.argv) > 1


def log(msg=""):
    if DEBUG:
        print(msg)


def append_to_queue(frontier, courses):
    for course in courses:
        if course not in frontier:
            # Calculate the heuristic of each sub-goal and queue them.
            value = course_heuristic(frontier, course)
            heapq.heappush(frontier, (value, course))


def search(frontier, schedule):

    while frontier:  # AND
        log()
        log("Frontier")
        log(frontier)

        node = heapq.heappop(frontier)
        course = node[1]
        log("Sub-goal chosen")
        log(course)
        possible_prerequisites = schedule.get_prereqs(course)
        # log("Sub-goal possible prerequisites")
        # log(possible_prerequisites)

        tried = 0
        for prerequisites in possible_prerequisites:  # OR
            # log("Trying prerequisites:")
            # log(prerequisites)

            prerequisites = list(set(prerequisites) - schedule.courses_taken)
            log("Filtered prerequisites")
            log(str(prerequisites))

            append_to_queue(frontier, prerequisites)

            if search(frontier, schedule):
                break

        if not schedule.schedule(course):
            log("Couldn't schedule " + str(course))
            log(schedule)

            return False
        log("New Schedule")
        log(schedule)

    # If I schedule everything on the frontier and nothing is left to search, we succeeded
    return True


def course_scheduler(course_descriptions, goal_conditions, initial_state):
    """
        State consists of a conjunction of courses/high-level requirements that are to be achieved.
        When conjunction set is empty a viable schedule should be in the schedule_set.
    """
    schedule = Schedule(course_descriptions, initial_state)

    frontier = []
    append_to_queue(frontier, goal_conditions)

    return schedule if search(frontier, schedule) else "No solution Found"
