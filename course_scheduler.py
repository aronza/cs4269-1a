# def aStarSearch(problem, heuristic=nullHeuristic):
#     """Search the node that has the lowest combined cost and heuristic first."""
#     from util import PriorityQueue
#
#     "Closed set keeps track of nodes already visited"
#     closed = set()
#     "Fringe holds the nodes we might want to visit and the path we got to them with"
#     fringe = PriorityQueue()
#     fringe.push((problem.getStartState(), [], 0), 0)
#
#     while not fringe.isEmpty():
#         "Take the next node to visit on stack"
#         node = fringe.pop()
#         "If it is the goal state return the path so far"
#         if problem.isGoalState(node[0]):
#             return node[1]
#         "If we didn't visit this node yet visit it"
#         if node[0] not in closed:
#             closed.add(node[0])
#             "Get the states accessible from this node"
#             children = problem.getSuccessors(node[0])
#
#             "For every state make a copy of path until here and add the direction to go this child"
#             for child in children:
#                 path_before = node[1].copy()
#                 path_before.append(child[1])
#                 cost = node[2]+child[2]
#                 fringe.push((child[0], path_before, cost), cost + heuristic(child[0], problem))
#
#     "If we didn't find any node throw an exception saying there no solution found"
#     if fringe.isEmpty():
#         raise Exception('No solution found')
from queue import PriorityQueue
from schedule import Schedule

from course_heuristic import course_heuristic

# TODO: Implement the backtracking DFS search
def course_scheduler(course_descriptions, goal_conditions, initial_state):
    schedule = Schedule(initial_state, course_descriptions)

    fringe = PriorityQueue()
    for goal in goal_conditions:
        fringe.put_nowait((course_heuristic(goal_conditions, goal), goal))

    for i in range(3):
        node = fringe.get_nowait()
        print(node)

        prereqs = schedule.get_prereqs(node[1])

        for req in prereqs:
            print(req)
            # value = course_heuristic(goal, req)
            # fringe.put((value, req))
    return 0
