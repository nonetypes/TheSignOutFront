# TheSignOutFront by nonetypes
# Last Revised on 03/01/2021
# Sign viewing simulator

from random import choice, shuffle, randint
from numpy import random
from linkedlist import LinkedList


class Student:
    """
    drive_by_time is in seconds with a normal distribution standard deviation of 5.
    """
    def __init__(self, number, drive_by_time=60, views_per_week=4):
        self.number = number
        self.drive_by_time = int(random.normal(drive_by_time, 5))
        self.views_per_week = views_per_week
        self.slides_seen = {}
        self.slide_seen = False
        self.view_time = 0
        self.time_on_road = 0
        self.schedule = {}
        self.arrival_times = {}

    def __repr__(self):
        return str(self.number)

    def view_slide(self, slide):
        """
        """
        if self.view_time >= 5 and not self.slide_seen:
            self.slide_seen = True
            if slide not in self.slides_seen:
                self.slides_seen[slide] = 1
            else:
                self.slides_seen[slide] += 1


class Sign:
    """
    time_per_slide is in seconds
    """
    def __init__(self, num_of_slides, time_per_slide):
        self.num_of_slides = num_of_slides
        self.time_per_slide = time_per_slide
        # Populate slides.
        self.slides = LinkedList()
        for i in range(num_of_slides):
            self.slides.append(f'Slide {i+1}')
        # Turn sign into a circle.
        self.slides[-1].next_node = self.slides[0]


class SignViewingSimulator:
    """a
    """
    def __init__(self, sign, list_of_students, duration_in_weeks):
        self.sign = sign
        self.students = list_of_students
        self.weeks = duration_in_weeks
        self.schedule = []
        self.results = {'Students': {}, 'Averages': {}}

    def create_schedule(self, sd=300):
        """Only simultates weeks at a time.

        Attempt to create a "realistic" schedule where students are randomly assigned
        one of three schedule types:

        Day: They only ever arrive during daylight hours.
        Night: They only ever arrive during evening hours.
        Mix: They arrive during the day or evening.

        Students will be assigned times on the hour of specific days in which they will arrive.
        This will be consistent week to week but they will likely arrive early
        or late with a normal distribution standard deviation of 5 minutes.

        If students will be coming to campus more than available classes, a time is
        chosen randomly, but this time will be consistent week to week.
        """
        self.schedule = []

        # Create student schedules.
        for student in self.students:
            # Day, night, mix schedules are represented by a list of possible
            # arrival times in seconds of a day on the hour.
            # Day:   32400 - 57600 (09:00 - 16:00)
            # Night: 61200 - 79200 (17:00 - 22:00)
            # Mix:   32400 - 79200 (09:00 - 22:00)
            schedules = [[32400, 36000, 38600, 43200, 46800, 50400, 54000, 57600],
                         [61200, 64800, 68400, 72000, 75600, 79200],
                         [32400, 36000, 38600, 43200, 46800, 50400, 54000, 57600,
                          61200, 64800, 68400, 72000, 75600, 79200]]
            # Assign which days a student will arrive every week.
            student_days = []
            for i in range(student.views_per_week):
                day = choice([1, 2, 3, 4, 5, 6, 7])
                student_days.append(day)
            student_days.sort()
            # Create arrival times in seconds of a week. These serve as times
            # to aim for but will vary by several minutes from week to week.
            student.schedule = []
            arrival_times = choice(schedules)
            for day in student_days:
                if arrival_times:
                    time = choice(arrival_times)
                    # Don't pick the same time twice.
                    # arrival_times.remove(time)
                # If there is no available hour, choose a time randomly.
                else:
                    time = randint(0, 86399)
                student.schedule.append(time * day)

        # Create simulation schedule.
        for week in range(self.weeks):
            schedule = []
            # Fill up the week with Nones.
            for second in range(60 * 60 * 24 * 7):
                schedule.append(None)
            # Replace Nones with students.
            for student in self.students:
                for time in student.schedule:
                    # Arriving early or late in seconds. Default of 5 minutes sd.
                    variance = int(random.normal(0, sd))
                    new_time = time + variance
                    # In cases where a time was randomly determined and the variance
                    # pushed it over into the next week, time will be without variance.
                    if new_time >= 604800:
                        new_time = time
                    # Make sure the time slot is not already taken.
                    if schedule[new_time] is None:
                        schedule[new_time] = student
                    # Another student was in the schedule -- avoid conflict.
                    else:
                        # Move forward in schedule until there isn't a student.
                        while schedule[new_time] is not None:
                            new_time += 1
                        schedule[new_time] = student
            self.schedule += schedule

    def simulate(self, random_slides=False):
        """
        """
        if random_slides:
            slides = []
            for slide in self.sign.slides:
                slides.append(slide)

        current_slide = self.sign.slides.head
        road = []
        seconds = 0
        for item in self.schedule:

            # Add students to road.
            if item is not None:
                road.append(item)

            for student in road:
                student.time_on_road += 1
                student.view_time += 1
                # Students will only "see" the slide if they've been viewing it for at least 5 seconds.
                student.view_slide(current_slide)
                # Students leaving road:
                if student.time_on_road >= student.drive_by_time:
                    student.time_on_road = 0
                    student.view_time = 0
                    student.slide_seen = False
                    road.remove(student)

            # Change slides every x seconds (time_per_slide)
            if seconds != 0 and not seconds % self.sign.time_per_slide:
                if random_slides:
                    slides_choices = slides[:]
                    slides_choices.remove(current_slide)
                    current_slide = choice(slides_choices)
                else:
                    current_slide = current_slide.next_node
                for student in road:
                    student.slide_seen = False
                    student.view_time = 0

            seconds += 1

    def calculate_results(self):
        unique_slides_viewed = 0
        num_of_slides_viewed = 0
        per_of_slides_viewed = 0
        for student in self.students:
            self.results['Students'][student] = {}
            self.results['Students'][student]['Unique Slides Viewed'] = len(student.slides_seen)
            total_viewed = 0
            for times_seen in student.slides_seen.values():
                total_viewed += times_seen
            self.results['Students'][student]['Total Slides Viewed'] = total_viewed
            self.results['Students'][student]['% of Slides Viewed'] = round((len(student.slides_seen) / self.sign.num_of_slides) * 100, 2)
            per_of_slides_viewed += self.results['Students'][student]['% of Slides Viewed']
            num_of_slides_viewed += self.results['Students'][student]['Total Slides Viewed']
            unique_slides_viewed += self.results['Students'][student]['Unique Slides Viewed']
        self.results['Averages']['Average Unique Slides Viewed'] = round(unique_slides_viewed / len(self.students), 2)
        self.results['Averages']['Average # of Slides Viewed'] = round(num_of_slides_viewed / len(self.students), 2)
        self.results['Averages']['Average % of Slides Viewed'] = round(per_of_slides_viewed / len(self.students), 2)
