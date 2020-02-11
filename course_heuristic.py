
def course_heuristic(goal_conditions, course):

    if course.program() == goal_conditions.program():
        return 1
    return 0

