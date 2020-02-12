from collections import namedtuple

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')
course_translation = {1: 'Frosh', 3: 'Soph', 5: 'Junior', 7: 'Senior'}
season_translation = {0: 'Spring', 1: 'Fall'}
max_semester = 8


class Schedule:
    def __init__(self, course_catalog, initial_state):
        self.dict = course_catalog
        self.courses_taken = set(initial_state)
        self.scheduled = {0: set(initial_state), 1: set(), 2: set(), 3: set(), 4: set(), 5: set(), 6: set(), 7: set(),
                          8: set()}

    def get_prereqs(self, course):
        return self.dict[course].prereqs

    def get_credits(self, course):
        return int(self.dict[course].credits)

    def schedule(self, course):
        if course in self.courses_taken:
            return True

        for i in range(1, max_semester + 1):
            if self.__can_schedule(course, i) and self.__requirements_satisfied(course, i):
                self.scheduled[i].add(course)
                self.courses_taken.add(course)
                return True
        return False
        # raise NameError(str(course) + " couldn't be scheduled in bound 8")

    def unschedule(self, course, semester):
        self.scheduled[semester].remove(course)

    def get_total_credits(self, semester):
        total = 0
        for course in self.scheduled[semester]:
            total += self.get_credits(course)
        return total

    def __is_course_offered(self, course, season):
        terms = self.dict[course].terms
        return season_translation[season] in terms

    def __requirements_satisfied(self, course, semester):
        possible_prerequisites = self.get_prereqs(course)
        courses_taken = self.scheduled[0]

        if not possible_prerequisites:
            return True

        for i in range(1, semester + (1 if self.get_credits(course) == 0 else 0)):
            courses_taken = courses_taken | self.scheduled[i]

        for prerequisites in possible_prerequisites:
            if set(prerequisites) - courses_taken == set():
                return True
        return False

    def __can_schedule(self, course, semester):
        return self.get_total_credits(semester) + self.get_credits(course) <= 18 and self.not_have_course(course) \
               and self.__is_course_offered(course, semester % 2)

    def not_have_course(self, course):
        for key in self.scheduled:
            if course in self.scheduled[key]:
                return False
        return True

    def __str__(self):
        schedule_str = ""

        for i in range(1, 9):
            season = season_translation[i % 2]
            year = course_translation[i if i % 2 == 1 else i - 1]
            schedule_str += season + ", " + year + ": "
            schedule_str += str(list(filter(lambda course: self.get_credits(course) != 0, self.scheduled[i])))
            schedule_str += str(self.get_total_credits(i)) + '\n'
        return schedule_str
