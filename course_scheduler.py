import sys
import heapq

from course_heuristic import course_heuristic
from schedule import Schedule
from tree import Tree

DEBUG = (sys.argv[1] == "debug") if len(sys.argv) > 1 else False


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
            append_to_queue(new_frontier, prerequisites)

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
    """
    schedule = Schedule(course_descriptions, initial_state)
    print("this is my tree\n")


    myRoot = Tree("Root Node")
    myLength = len(goal_conditions)
    if myLength > 1:
        for condition in goal_conditions:
            myRoot.add_child(schedule.build_prereq_tree([condition]))
    else:
        myRoot = schedule.build_prereq_tree(goal_conditions)


    print(myRoot.calculate_depth())
    frontier = []
    append_to_queue(frontier, goal_conditions)
    search(frontier, schedule)
    return schedule.get_plan()