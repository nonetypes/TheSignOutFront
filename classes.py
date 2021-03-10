# Contains primary classes for TheSignOutFront
# Sign, Student, SignViewingSimulator

from random import choice, randint, shuffle
from numpy import random
from statistics import median
from linkedlist import LinkedList


class Sign:
    """Sign Object to be used in SignViewingSimulator

    Contains a circular LinkedList representing slides which
    display in a loop.

    time_per_slide is in seconds.
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


class Student:
    """Student object to be used in SignViewingSimulator.

    drive_by_time is in seconds with a normal distribution standard deviation of 5
    to simulate variance in driving speeds.
    """
    def __init__(self, number, drive_by_time=60, drive_by_time_sd=5, views_per_week=4):
        self.number = number
        self.drive_by_time = int(random.normal(drive_by_time, drive_by_time_sd))
        self.views_per_week = views_per_week
        self.view_time = 0
        self.time_on_road = 0
        self.slide_seen = False
        self.slides_seen = {}
        self.schedule = []
        self.arrival_times = []

    def __repr__(self):
        return str(self.number)

    def view_slide(self, slide):
        """Students will only "see" slides if they are able to view them for
        at least 2 seconds.
        """
        if self.view_time >= 2 and not self.slide_seen:
            self.slide_seen = True
            if slide.item not in self.slides_seen:
                self.slides_seen[slide.item] = 1
            else:
                self.slides_seen[slide.item] += 1

    def get_arrival_time(self, time_in_seconds):
        """For confirmation that student schedules are functioning as intended.

        Convert seconds to a string of '2, Mon, 14:52:23' (week, day, time)

        Add it to self.arrival_times. Collected as students enter road.
        """
        day = 60 * 60 * 24
        week = day * 7
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        output = ''
        # Week
        output += str((time_in_seconds//week) + 1)+', '
        time_in_seconds = time_in_seconds % week
        # Day
        output += days[time_in_seconds//day]+', '
        time_in_seconds = time_in_seconds % day
        # Hour
        output += str(int(time_in_seconds / 3600)).zfill(2)+':'
        # Minutes
        output += str(int(time_in_seconds / 60 % 60)).zfill(2)+':'
        # Seconds
        output += str(int(time_in_seconds % 60)).zfill(2)

        self.arrival_times.append(output)


class SignViewingSimulator:
    """Simulator class.

    Create schedules for students and a schedule for the simulation itself.
    Run simulation and calculate results.
    """
    def __init__(self, sign, list_of_students, duration_in_weeks, thread=None):
        self.sign = sign
        self.students = list_of_students
        self.weeks = duration_in_weeks
        self.thread = thread
        self.schedule = []
        self.results = {'Students': {}, 'Totals': {}}

    def create_random_schedule(self):
        """Create a randomized schedule.

        Students will still drive by the sign a consistent number of times per week.

        Warning: Students may have a greater chance to appear on the road with themselves.
        """
        week_in_seconds = 60 * 60 * 24 * 7

        for week in range(self.weeks):
            schedule = []
            # Add empty seconds (Nones) to schedule
            for i in range(week_in_seconds - (len(self.students) * self.students[0].views_per_week)):
                schedule.append(None)

            # Add students
            for student in self.students:
                for i in range(student.views_per_week):
                    schedule.append(student)

            shuffle(schedule)
            self.schedule += schedule

    def create_schedule(self, arrival_sd=300):
        """Only simultates weeks at a time.

        Attempt to create a "realistic" schedule where students are randomly assigned
        one of three schedule types:

        Day: They arrive for classes during daylight hours.
        Night: They arrive for classes during evening hours.
        Mix: They arrive for classes during the day or evening.

        Students will be assigned times on the hour of specific days in which they will arrive.
        This will be consistent week to week but they will likely arrive early
        or late with a normal distribution standard deviation of 5 minutes (default).

        If students will be coming to campus more than 7 times per week, a time is
        chosen randomly, but this time will be consistent week to week.
        """
        # Day, night, mix schedules are represented by a list of possible
        # arrival times in seconds of a day on the hour.
        # daytime:   28800 - 57600 (08:00 - 16:00)
        # nighttime: 61200 - 79200 (17:00 - 22:00)
        # mix:       32400 - 79200 (09:00 - 22:00)
        daytime = []
        for hour in range(8, 17):
            daytime.append(hour * 3600)
        nighttime = []
        for hour in range(17, 23):
            nighttime.append(hour * 3600)
        mix = daytime + nighttime

        # Create student schedules.
        for student in self.students:
            # Interrupt simulation when cancel is pressed.
            if self.canceled():
                return
            # Assign which days a student will arrive every week.
            student_days = []
            weekdays = [1, 2, 3, 4, 5, 6, 7]
            for i in range(student.views_per_week):
                if weekdays:
                    day = choice(weekdays)
                    # Don't pick the same day twice.
                    weekdays.remove(day)
                # If the student is visiting more than 7 days/week:
                else:
                    day = choice([1, 2, 3, 4, 5, 6, 7])
                student_days.append(day)
            student_days.sort()
            # Create arrival times in seconds of a week. These serve as times
            # to aim for but will vary by several minutes from week to week.
            arrival_times = choice([daytime, nighttime, mix])
            for day in student_days:
                if len(student_days) <= 7:
                    time = choice(arrival_times)
                # If visiting more than 7 times/week, choose a random time.
                else:
                    time = randint(0, 86399)
                # Convert to time in seconds of the week.
                student.schedule.append(time + ((day - 1) * 86400))

        # Create schedule of simulation.
        for week in range(self.weeks):
            schedule = []
            # Fill up the week with Nones.
            for second in range(60 * 60 * 24 * 7):
                schedule.append(None)
            # Replace Nones with students.
            for student in self.students:
                # Interrupt simulation when cancel is pressed.
                if self.canceled():
                    return
                for time in student.schedule:
                    # Arriving early or late in seconds. Default of 5 minutes sd.
                    variance = int(random.normal(0, arrival_sd))
                    new_time = time + variance
                    # In cases where a time was randomly determined and the variance
                    # pushed it over into the next week, time will be without variance.
                    if new_time >= 604800:
                        new_time = time
                    # Make sure the time slot is not already taken.
                    # Move forward in schedule until there isn't a student.
                    while schedule[new_time] is not None:
                        if self.canceled():
                            return
                        new_time += 1
                        # If time moves into next week, reset time.
                        if new_time >= 604800:
                            new_time = 0
                    schedule[new_time] = student
            self.schedule += schedule

    def simulate(self, random_slides=False):
        """Run simulation.

        Step through each second in self.schedule and add students to the road.
        Slides change every x seconds.
        Students in the road see a slide if seen for at least 2 seconds.
        """
        if random_slides:
            slides = []
            for slide in self.sign.slides:
                slides.append(slide)

        current_slide = self.sign.slides.head
        road = []
        for second in range(len(self.schedule)):

            # Interrupt simulation when cancel is pressed.
            if self.canceled():
                return

            # Add students to road.
            if self.schedule[second] is not None:
                road.append(self.schedule[second])
                # Record arrival time.
                self.schedule[second].get_arrival_time(second)

            for student in road:
                student.time_on_road += 1
                student.view_time += 1
                # Students will only "see" the slide if they've been viewing it for at least 2 seconds.
                student.view_slide(current_slide)
                # Students leaving road:
                if student.time_on_road >= student.drive_by_time:
                    student.time_on_road = 0
                    student.view_time = 0
                    student.slide_seen = False
                    road.remove(student)

            # Change slides every x seconds (time_per_slide)
            if second != 0 and not second % self.sign.time_per_slide:
                if random_slides:
                    slides_choices = slides[:]
                    # Don't choose the same slide two times in a row.
                    slides_choices.remove(current_slide)
                    current_slide = choice(slides_choices)
                else:
                    current_slide = current_slide.next_node
                for student in road:
                    student.view_time = 0
                    student.slide_seen = False

    def calculate_results(self):
        """Tally the results based on slides seen by all students.

        Calculate averages and medians.

        Store results in self.results.
        """
        unique_slides_viewed = 0
        num_of_slides_viewed = 0
        per_of_slides_viewed = 0
        median_unique_slides = []

        # Create results for each student.
        for student in self.students:
            self.results['Students'][student] = {}
            self.results['Students'][student]['Unique Slides Viewed'] = len(student.slides_seen)
            total_viewed = 0
            for times_seen in student.slides_seen.values():
                total_viewed += times_seen
            self.results['Students'][student]['Total Slides Viewed'] = total_viewed
            student_per_slides_viewed = round((len(student.slides_seen) / self.sign.num_of_slides) * 100, 2)
            self.results['Students'][student]['% of Slides Viewed'] = student_per_slides_viewed
            per_of_slides_viewed += self.results['Students'][student]['% of Slides Viewed']
            num_of_slides_viewed += self.results['Students'][student]['Total Slides Viewed']
            unique_slides_viewed += self.results['Students'][student]['Unique Slides Viewed']
            median_unique_slides.append(self.results['Students'][student]['Unique Slides Viewed'])

        # Create averages and median
        self.results['Totals']['Median of Unique Slides Viewed'] = int(median(median_unique_slides))
        self.results['Totals']['Average Unique Slides Viewed'] = round(unique_slides_viewed / len(self.students), 2)
        self.results['Totals']['Average # of Slides Viewed'] = round(num_of_slides_viewed / len(self.students), 2)
        self.results['Totals']['Average % of Slides Viewed'] = round(per_of_slides_viewed / len(self.students), 2)

    def canceled(self):
        """Boolean test to see if cancel button was pressed.

        Placed periodically within schedule building and simulation where
        simulation can take long periods of time due to certain parameter entries.
        """
        if self.thread and self.thread.canceled.is_set():
            return True
        else:
            return False
