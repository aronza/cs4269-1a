from collections import namedtuple

Course = namedtuple('Course', 'program, designation')
CourseInfo = namedtuple('CourseInfo', 'credits, terms, prereqs')


class Schedule:
    def __init__(self, course_catalog, initial_state):
        self.dict = course_catalog
        self.scheduled = {0: initial_state, 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
        self.course_translation = {'Frosh': 1, 'Soph': 3, 'Junior': 5, 'Senior': 7}
        self.season_translation = {0: 'Spring', 1: 'Fall'}

    def get_prereqs(self, course):
        return self.dict.get(course).prereqs

    def get_credits(self, course):
        return int(self.dict[course].credits)

    def schedule_course(self, course, year, semester):
        if semester == 'Fall':
            self.scheduled[self.course_translation[year]].append(course)
        else:
            self.scheduled[self.course_translation[year] + 1].append(course)

    def schedule(self, course, semester):
        self.scheduled[semester].append(course)

    def unschedule(self, course, semester):
        self.scheduled[semester].remove(course)

    def get_total_credits(self, semester):
        total = 0
        for course in self.scheduled[semester]:
            total += self.get_credits(course)
        return total

    def is_course_offered(self, course, season):
        terms = self.dict[course].terms
        return self.season_translation[season] in terms

    def can_schedule(self, course, semester):
        return self.get_total_credits(semester) < 18 and self.not_have_course(course) \
               and self.is_course_offered(course, semester % 2)

    def not_have_course(self, course):
        for key in self.scheduled:
            if course in self.scheduled[key]:
                return False
        return True

    def __str__(self):
        return str(self.scheduled)
