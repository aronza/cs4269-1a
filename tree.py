"""
    Team Number: 10
    Members: Noah Popham, Arda Turkmen, Mark Weinstein, Harry Wilson
"""


class Tree(object):

    def __init__(self, data):
        self.data = data
        self.children = []
        self.max_depth = 0

    def add_child(self, obj):
        self.children.append(obj)

    def has_children(self):
        if self.children == []:
            return False;
        return True;

    def get_depth(self):
        return self.max_depth

    def calculate_depth(self):
        if not self.has_children():
            return 1
        else:
            maxDepth = 0
            for allChildren in self.children:
                newMax = allChildren.calculate_depth()
                if newMax > maxDepth:
                    maxDepth = newMax
            return 1 + maxDepth
