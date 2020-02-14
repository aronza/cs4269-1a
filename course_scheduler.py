from pprint import pprint
import sys
import heapq
from copy import deepcopy

from course_heuristic import course_heuristic
from schedule import Schedule

DEBUG = len(sys.argv) > 1


def log(msg=""):
    """
    Helper Function to print out a debugging message if DEBUG mode is on. (Any parameters are given to program)
    """
    if DEBUG:
        print(msg)


def append_to_queue(frontier, courses):
    """
        Add a list of courses to the search queue after assigning each a heuristic value
    """
    for course in courses:
        if course not in frontier:
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
        chosen_prerequisites = None

        for prerequisites in possible_prerequisites:  # OR
            """ 
                If this is an elective and we already have this specific requirement than look for another            
            """
            if schedule.is_elective(course) and set(prerequisites) - schedule.courses_taken == set():
                   # schedule.have_elective_course(course, prerequisites):
                continue

            prerequisites = list(set(prerequisites) - schedule.courses_taken)

            """ 
                If we already satisfy all the requirement for this course, we can go ahead and schedule it.            
            """
            if not prerequisites:
                break
            log("Trying Prerequisite")
            log(str(prerequisites))

            scheduled_old = deepcopy(schedule.scheduled)
            courses_taken_old = deepcopy(schedule.courses_taken)

            new_frontier = []
            append_to_queue(new_frontier, prerequisites)

            if search(new_frontier, schedule):
                chosen_prerequisites = prerequisites
                break
            else:
                schedule.courses_taken = courses_taken_old
                schedule.scheduled = scheduled_old
                log("Child returned false")

        """ By here we either have the requirements for this course or tried all possible requirement for this course. 
            If we still can't schedule it, then we failed to schedule it and must return False up the tree
        """
        if not schedule.schedule(course):
            log("Couldn't schedule " + str(course))
            log(schedule)
            return False

        """ If the course we scheduled is a high-level elective requirement, then we want to store the course we used
            to fulfill this elective requirement so that the course is not used again for the same elective.
        """
        if schedule.is_elective(course):
            schedule.add_elective_course(course, chosen_prerequisites)
        log("Scheduled new course " + str(course))
        log("New Schedule")
        log(schedule)

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
