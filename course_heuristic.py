
def course_heuristic(dictionary, course):
    if course in dictionary:
        return -1 * dictionary[course]
    return 0

