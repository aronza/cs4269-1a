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


def append_to_queue(frontier, courses, depth):
    for course in courses:
        if course not in frontier:
            # Calculate the heuristic of each sub-goal and queue them.
            value = course_heuristic(frontier, course) - depth
            heapq.heappush(frontier, (value, course))


def search(frontier, schedule, depth):
    while frontier:  # AND
        log()
        log("Frontier")
        log(frontier)

        node = heapq.heappop(frontier)
        course = node[1]
        log("Sub-goal chosen")
        log(course)
        possible_prerequisites = schedule.get_prereqs(course)
        chosen_prerequisites = None
        # if schedule.is_high_level(course)

        for prerequisites in possible_prerequisites:  # OR
            # If this is an elective and we already have this specific requirement than look for another
            if schedule.is_elective(course) and schedule.have_elective_course(course, prerequisites):
                continue

            prerequisites = list(set(prerequisites) - schedule.courses_taken)

            # If we already satisfy all the requirement for this course, we can go ahead and schedule it.
            if not prerequisites:
                break
            log("Trying Prerequisite")
            log(str(prerequisites))

            frontier_old = deepcopy(frontier)
            scheduled_old = deepcopy(schedule.scheduled)
            courses_taken_old = deepcopy(schedule.courses_taken)

            new_depth = depth
            if not schedule.is_high_level(course):
                new_depth += 1

            new_frontier = []
            append_to_queue(new_frontier, prerequisites, new_depth)

            if search(new_frontier, schedule, new_depth):
                chosen_prerequisites = prerequisites
                break
            else:
                frontier = frontier_old
                schedule.courses_taken = courses_taken_old
                schedule.scheduled = scheduled_old
                log("Child returned false")

        if not schedule.schedule(course):
            log("Couldn't schedule " + str(course))
            log(schedule)

            return False

        if schedule.is_elective(course):
            schedule.add_elective_course(course, chosen_prerequisites)
        log("Scheduled new course " + str(course))
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
    append_to_queue(frontier, goal_conditions, 0)

    return schedule if search(frontier, schedule, 0) else "No solution Found"
