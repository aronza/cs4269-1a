from pprint import pprint
from queue import PriorityQueue
from schedule import Schedule
import sys

from course_heuristic import course_heuristic

DEBUG = len(sys.argv) > 1

def log(msg=""):
    if DEBUG:
        print(msg)

def append_to_queue(queue, courses, semester):
    for course in courses:
        # Calculate the heuristic of each sub-goal and queue them.
        # value = course_heuristic(schedule, queue, course)
        queue.append((0, course, semester))


def search(frontier, schedule):

    while frontier:
        log()
        log("Frontier")
        log(frontier)

        node = frontier.pop()
        course = node[1]
        semester = node[2]
        course_credits = schedule.get_credits(course)
        log("Sub-goal chosen")
        log(course)

        if not schedule.can_schedule(course, semester):
            log("Can't schedule")
            log()
            return False

        schedule.schedule(course, semester)
        log("New Schedule")
        log(schedule)

        possible_prerequisites = schedule.get_prereqs(course)
        log("Sub-goal possible prerequisites")
        log(possible_prerequisites)

        tried = 0
        for prerequisites in possible_prerequisites:
            log("Trying prerequisites:")
            log(prerequisites)

            if course_credits != 0:
                prerequisites = list(filter(schedule.not_have_course, prerequisites))
                log("Filtered prerequisites")
                log(prerequisites)

            # Copy frontier and add all the requirements in prerequisites with their heuristic
            # new_frontier = copy.deepcopy(frontier)
            new_semester = semester
            if course_credits != 0:
                new_semester = new_semester - 1
                if new_semester == 0:
                    return False
            append_to_queue(frontier, prerequisites, new_semester)

            if search(frontier, schedule):
                break
            else:
                # If no schedule found for any of possible_prerequisites, we failed to schedule this class and can't
                # pursue this path
                if tried == len(possible_prerequisites):
                    schedule.unschedule(course, semester)
                    log("No possible req works!")
                    return False
                tried += 1

    # If I schedule everything on the frontier and nothing is left to search, we succeeded
    return True


# TODO: Implement the backtracking DFS search
def course_scheduler(course_descriptions, goal_conditions, initial_state):
    """
        State consists of a conjunction of courses/high-level requirements that are to be achieved.
        When conjunction set is empty a viable schedule should be in the schedule_set.
    """
    schedule = Schedule(course_descriptions, initial_state)

    frontier = []
    semester = 8
    append_to_queue(frontier, goal_conditions, semester)

    result = search(frontier, schedule)
    return schedule if result else "No solution Found"
