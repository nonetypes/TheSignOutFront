# Tkinter GUI for TheSignOutFront
# SignSimulatorWindow

import tkinter as tk
from threading import Thread, Event
from json import loads, dumps
from random import shuffle
from classes import Sign, Student, SignViewingSimulator


class SignSimulatorWindow:
    """Tkinter window for entering simulation parameters and running simulations for TheSignOutFront.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('SignViewingSimulator')
        self.entries = {}
        self.thread = None

        self.padx = 2
        self.pady = 2
        self.entry_width = 14
        self.label_width = 19

        # vcmd will be used to restrict entry boxes to receive numbers with validatecommand.
        # https://stackoverflow.com/questions/8959815/restricting-the-value-in-tkinter-entry-widget
        vcmd = (self.window.register(self.validate_digit))

        # Sign Frame
        self.sign_frame = tk.LabelFrame(self.window, text='Sign')
        self.sign_frame.grid(row=0, column=0, padx=4, pady=4, columnspan=2, sticky='w')
        # Sign Slides Number
        self.sign_num_label = tk.Label(self.sign_frame, text='Number of Slides',
                                       width=self.label_width, anchor='w')
        self.sign_num_label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.sign_num_entry = tk.Entry(self.sign_frame, width=self.entry_width,
                                       validate='key', validatecommand=(vcmd, '%P'))
        self.sign_num_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Sign Slides Time
        self.sign_time_label = tk.Label(self.sign_frame, text='Seconds Per Slide',
                                        width=self.label_width, anchor='w')
        self.sign_time_label.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.sign_time_entry = tk.Entry(self.sign_frame, width=self.entry_width,
                                        validate='key', validatecommand=(vcmd, '%P'))
        self.sign_time_entry.grid(row=1, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Sign Random Slides
        self.sign_random_var = tk.BooleanVar()
        self.sign_random_check = tk.Checkbutton(self.sign_frame, text='Choose slides randomly',
                                                command=self.toggle_random_slides, variable=self.sign_random_var,
                                                onvalue=True, offvalue=False)
        self.sign_random_check.grid(row=2, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='w')

        # Students Frame
        self.students_frame = tk.LabelFrame(self.window, text='Students')
        self.students_frame.grid(row=1, column=0, padx=4, pady=4, columnspan=2, sticky='w')
        # Students Number
        self.students_num_label = tk.Label(self.students_frame, text='Number of Students',
                                           width=self.label_width, anchor='w')
        self.students_num_label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.students_num_entry = tk.Entry(self.students_frame, width=self.entry_width,
                                           validate='key', validatecommand=(vcmd, '%P'))
        self.students_num_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Students View Time
        self.students_time_label = tk.Label(self.students_frame, text='View Time in Seconds',
                                            width=self.label_width, anchor='w')
        self.students_time_label.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.students_time_entry = tk.Entry(self.students_frame, width=self.entry_width,
                                            validate='key', validatecommand=(vcmd, '%P'))
        self.students_time_entry.grid(row=1, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Students View Number
        self.students_views_label = tk.Label(self.students_frame, text='Views Per Week',
                                             width=self.label_width, anchor='w')
        self.students_views_label.grid(row=2, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.students_views_entry = tk.Entry(self.students_frame, width=self.entry_width,
                                             validate='key', validatecommand=(vcmd, '%P'))
        self.students_views_entry.grid(row=2, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Students Random Schedules
        self.students_random_var = tk.BooleanVar()
        self.students_random_check = tk.Checkbutton(self.students_frame, text='Random student schedules',
                                                    command=self.toggle_random_students,
                                                    variable=self.students_random_var, onvalue=True, offvalue=False)
        self.students_random_check.grid(row=5, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='w')

        # Standard Deviations Frame
        self.sd_frame = tk.LabelFrame(self.window, text='Standard Deviations')
        self.sd_frame.grid(row=2, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='w')
        # Standard Deviation Student View Time
        self.sd_student_time_label = tk.Label(self.sd_frame, text='View Time in Seconds',
                                         width=self.label_width, anchor='w')
        self.sd_student_time_label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.sd_student_time_entry = tk.Entry(self.sd_frame, width=self.entry_width,
                                         validate='key', validatecommand=(vcmd, '%P'))
        self.sd_student_time_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Standard Deviation Student Arrival Time
        self.sd_student_arrival_label = tk.Label(self.sd_frame, text='Early/Late Arrival Time',
                                         width=self.label_width, anchor='w')
        self.sd_student_arrival_label.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.sd_student_arrival_entry = tk.Entry(self.sd_frame, width=self.entry_width,
                                         validate='key', validatecommand=(vcmd, '%P'))
        self.sd_student_arrival_entry.grid(row=1, column=1, padx=self.padx, pady=self.pady, sticky='w')

        # Simulation Frame
        self.simulation_frame = tk.LabelFrame(self.window, text='Simulation')
        self.simulation_frame.grid(row=3, column=0, padx=4, pady=4, columnspan=2, sticky='w')
        # Simulation Length
        self.simulation_time_label = tk.Label(self.simulation_frame, text='Duration in Weeks',
                                              width=self.label_width, anchor='w')
        self.simulation_time_label.grid(row=0, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.simulation_time_entry = tk.Entry(self.simulation_frame, width=self.entry_width,
                                              validate='key', validatecommand=(vcmd, '%P'))
        self.simulation_time_entry.grid(row=0, column=1, padx=self.padx, pady=self.pady, sticky='w')
        # Simulation Number
        self.simulation_num_label = tk.Label(self.simulation_frame, text='Number of Simulations',
                                             width=self.label_width, anchor='w')
        self.simulation_num_label.grid(row=1, column=0, padx=self.padx, pady=self.pady, sticky='w')
        self.simulation_num_entry = tk.Entry(self.simulation_frame, width=self.entry_width,
                                             validate='key', validatecommand=(vcmd, '%P'))
        self.simulation_num_entry.grid(row=1, column=1, padx=self.padx, pady=self.pady, sticky='w')

        # Run Simulation Button
        # self.run() is threaded to allow real-time status updates
        # and to cancel sumulations when running many of them.
        self.simulation_run_button = tk.Button(self.window, text='Run', width=8, command=self.start_thread)
        self.simulation_run_button.grid(row=4, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='n')
        # Bind Run to enter key.
        self.window.bind('<Return>', self.enter_key)

        # Status Label
        self.status_label = tk.Label(self.window)
        self.status_label.grid(row=5, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='n')

        self.load_settings()
        self.window.mainloop()

        # In the event that simulations are still running when window is closed, cancel them.
        if self.thread:
            self.thread.canceled.set()

        # Save most recent entries to settings upon close.
        self.save_settings()

    def validate_digit(self, entry):
        """Digit validation for tkinter entry boxes.

        Will only allow digits to be entered in entry boxes.
        """
        if str(entry).isdigit() or entry == "":
            return True
        else:
            return False

    def toggle_random_slides(self):
        """Print state of sign_random_var when random slides checkbox is clicked.
        """
        print(f'Random slides set to {self.sign_random_var.get()}')

    def toggle_random_students(self):
        """Print state of studends_random_var when random student schedules checkbox is clicked.
        """
        print(f'Random student schedules set to {self.students_random_var.get()}')        

    def run(self):
        """Run the simulation(s) from the entered parameters in the entry boxes.
        """
        self.get_entries()

        # Collect averages from every simulation that is run.
        simulations_results = {'Average Unique Slides Viewed': [],
                               'Average # of Slides Viewed': [],
                               'Average % of Slides Viewed': []}

        # Print "n Simulations:"
        simulation_string = f"{self.entries['simulation_num']} Simulation"
        simulation_string += ':' if self.entries['simulation_num'] == 1 else 's:'
        print(simulation_string)

        # Create sign.
        sign = Sign(self.entries['slide_num'], self.entries['slide_time'])

        # Run n number of simulations
        for n in range(self.entries['simulation_num']):

            # Interrupt simulations when cancel is pressed or window is closed.
            if self.thread and self.thread.canceled.is_set():
                print('Simulations Canceled')
                return

            # Update status message.
            self.status_label.configure(text=f'Running Simulation {n+1}')
            print(f'Running Simulation {n+1}', end='\r')

            # Create Students
            students = []
            for i in range(self.entries['student_num']):
                students.append(Student(i+1, self.entries['student_time'], self.entries['sd_student_time'],
                                        self.entries['student_views']))

            # Create and run simulation.
            simulation = SignViewingSimulator(sign, students, self.entries['simulation_time'], self.thread)
            if self.entries['students_random']:
                simulation.create_random_schedule()
            else:
                simulation.create_schedule(arrival_sd=self.entries['sd_student_arrival'])
            simulation.simulate(random_slides=self.entries['slides_random'])
            simulation.calculate_results()

            # Check again if simulation was canceled while it was running.
            if self.thread and self.thread.canceled.is_set():
                print('Simulations Canceled')
                return

            # Collect results.
            for key, val in simulation.results['Averages'].items():
                simulations_results[key].append(val)

            # print(len(simulation.schedule))

        # Print average results across any/all simulations.
        results_string = ''
        for key, val in simulations_results.items():
            results_string += f'{key}: {round((sum(val) / len(val)), 2)}\n'
        print(results_string[:-1])

        # Write results to results.txt
        self.write_results(simulation, results_string)

        if self.entries['simulation_num'] == 1:
            self.status_label.configure(text='Simulation Complete')
        else:
            self.status_label.configure(text='Simulations Complete')

    def start_thread(self):
        """Execute run() when the "Run" button is pressed.

        run() is threaded to allow real-time updating of status messages and
        the ability to cancel the execution of numerous simulations.

        While run() is running, "Run" button is replaced with "Cancel".
        check_thread() determines when thread is complete and reconfigures
        run button.

        https://stackoverflow.com/a/56953613
        """
        self.thread = Thread(target=self.run)
        # Create an event flag so thread can be interrupted. It is initially false.
        self.thread.canceled = Event()
        self.thread.start()

        # Reconfigure "Run" button to "Cancel". Unbind enter key.
        self.simulation_run_button.configure(text='Cancel', command=self.cancel_thread)
        self.window.unbind('<Return>')

        # Repeatedly check if thread is completed, reconfiguring "Run" button when it is.
        self.check_thread()

    def check_thread(self):
        """Used in self.start_thread() to check if simulations have completed,
        reconfiguring "Run" button to allow simulations to be run again.

        If the thread is active, call check_thread() again after .1 seconds.
        """
        if self.thread.is_alive():
            self.window.after(100, self.check_thread)
        else:
            self.simulation_run_button.configure(text='Run', command=self.start_thread)
            self.window.bind('<Return>', self.enter_key)

    def cancel_thread(self):
        """Called when "Cancel" button is pressed.

        Sets the thread's event flag to true. This is checked before every simulation is run,
        returning out of function when found to be true.

        Reset "Run" button and rebind enter key.
        """
        print('Canceling Simulations')
        self.thread.canceled.set()
        self.simulation_run_button.configure(text='Run', command=self.start_thread)
        self.window.bind('<Return>', self.enter_key)
        self.status_label.configure(text='Canceled')

    def enter_key(self, event):
        """For binding the enter key to start_thread() and ultimately run().
        """
        self.start_thread()

    def get_entries(self):
        """Retrieve and store the entries from the entry boxes.
        """
        # Put tkinter entry boxes in dictionary to be easily called.
        entry_boxes = {}
        entry_boxes['slide_num'] = self.sign_num_entry
        entry_boxes['slide_time'] = self.sign_time_entry
        entry_boxes['student_num'] = self.students_num_entry
        entry_boxes['student_time'] = self.students_time_entry
        entry_boxes['student_views'] = self.students_views_entry
        entry_boxes['sd_student_time'] = self.sd_student_time_entry
        entry_boxes['sd_student_arrival'] = self.sd_student_arrival_entry
        entry_boxes['simulation_time'] = self.simulation_time_entry
        entry_boxes['simulation_num'] = self.simulation_num_entry

        # Collect user entries.
        entries = {}
        for key, val in entry_boxes.items():
            entries[key] = val.get()

        # Typecast to integers.
        for key, val in entries.items():
            # Standard Deviations are defaulted to 0.
            if key in ['sd_student_time', 'sd_student_arrival']:
                if not val:
                    entries[key] = 0
                    # Reflect changes in entry box.
                    entry_boxes[key].delete(0, 'end')
                    entry_boxes[key].insert(0, 0)
                else:
                    entries[key] = int(val)
            else:
                # If there was no entry, set it to 1.
                if not val or int(val) == 0:
                    entries[key] = 1
                    # Reflect changes in entry box.
                    entry_boxes[key].delete(0, 'end')
                    entry_boxes[key].insert(0, 1)
                else:
                    entries[key] = int(val)

        # Get random checkboxes.
        entries['slides_random'] = self.sign_random_var.get()
        entries['students_random'] = self.students_random_var.get()

        # Impose limitation on slides to prevent hanging.
        if entries['slide_num'] > 10000:
            entries['slide_num'] = 9999
            self.sign_num_entry.delete(0, 'end')
            self.sign_num_entry.insert(0, 9999)

        # Limitation on number of students/views per week to
        # avoid infinite loops when creating simulation schedule.
        if entries['student_num'] * entries['student_views'] >= 600_000:
            if entries['student_num'] > 10000:
                entries['student_num'] = 10000
                # Delete old entry box entry and update it.
                self.students_num_entry.delete(0, 'end')
                self.students_num_entry.insert(0, str(10000))
            if entries['student_views'] > 10:
                entries['student_views'] = 10
                self.students_views_entry.delete(0, 'end')
                self.students_views_entry.insert(0, str(100))

        # Limitation on early/late arrival time standard deviation to avoid index out of range error.
        if entries['sd_student_arrival'] > 100000:
            entries['sd_student_arrival'] = 100000
            self.sd_student_arrival_entry.delete(0, 'end')
            self.sd_student_arrival_entry.insert(0, str(100000))

        self.entries = entries

    def load_settings(self):
        """Attempt to load settings and apply entries to entry boxes.

        Called during initialization.
        """
        try:
            settings = loads(open('settings', 'r').read())
        except Exception:
            print('No settings file found.')
        else:
            self.sign_num_entry.insert(0, str(settings['slide_num']))
            self.sign_time_entry.insert(0, str(settings['slide_time']))
            self.students_num_entry.insert(0, str(settings['student_num']))
            self.students_time_entry.insert(0, str(settings['student_time']))
            self.students_views_entry.insert(0, str(settings['student_views']))
            self.simulation_num_entry.insert(0, str(settings['simulation_num']))
            self.simulation_time_entry.insert(0, str(settings['simulation_time']))
            self.sd_student_time_entry.insert(0, str(settings['sd_student_time']))
            self.sd_student_arrival_entry.insert(0, str(settings['sd_student_arrival']))
            self.sign_random_var.set(settings['slides_random'])
            self.students_random_var.set(settings['students_random'])

    def save_settings(self):
        """Save the last retrieved entries entered in entry boxes to settings file.

        Called after tkinter window is closed.
        """
        if self.entries:
            try:
                with open('settings', 'w') as stream:
                    stream.write(dumps(self.entries))
            except Exception as error:
                print(f'Settings not saved: {error}')
            else:
                print('Settings saved successfully.')

    def write_results(self, simulation, all_results_string):
        """Format and write various results to results.txt

        Parameters, averages, and a sampling of 10 random students are formatted and written.
        """
        string = ''

        # Simulation Parameters
        readable_params = {'slide_num': 'Number of Slides', 'slide_time': 'Seconds Per Slide',
                           'student_num': 'Number of Students', 'student_time': 'Viewing Time',
                           'student_views': 'Views Per Week', 'sd_student_time': 'Viewing Time SD',
                           'sd_student_arrival': 'Early/Late Arrival Time SD', 'simulation_time': 'Duration in Weeks',
                           'simulation_num': 'Number of Simulations', 'slides_random': 'Random Slides',
                           'students_random': 'Random Student Schedules'}
        string += 'Simulation Parameters:\n'
        for key, val in self.entries.items():
            string += f'{readable_params[key]}: {val}\n'

        # Total averages
        string += '\nAll Simulations:\n'
        string += all_results_string

        # Averages from last simulation
        if self.entries['simulation_num'] > 1:
            string += '\nMost Recent Simulation:\n'
            for key, val in simulation.results['Averages'].items():
                string += f'{key}: {val}\n'

        # Individualized data -- Randomize and use first 10 students.
        shuffle(simulation.students)
        string += '\nStudent Sampling From Most Recent Simulation:\n'
        for student in simulation.students[:10]:
            string += f'Student {str(student).zfill(len(str(len(simulation.students))))}: '
            for key, val in simulation.results["Students"][student].items():
                string += f'{key}: {val}, '
            string = string[:-2]+'\n'

        # Slides seen by individual students
        string += '\nSlides Seen:\n'
        for student in simulation.students[:10]:
            string += f'Student {str(student).zfill(len(str(len(simulation.students))))}: '
            slides_seen = []
            for key, val in student.slides_seen.items():
                slides_seen.append(f'{key}: {val}')
            string += ', '.join(slides_seen)+'\n'

        # Arrival Times
        string += '\nArrival Times:\n'
        for student in simulation.students[:10]:
            string += f'Student {str(student).zfill(len(str(len(simulation.students))))}:\n'
            # Divide total arrival times by simulation weeks and put each on a new line for readablity in txt file.
            arrivals = student.arrival_times[:]
            for week in range(simulation.weeks):
                weekly_arrivals = []
                for i in range(int(len(student.arrival_times) / simulation.weeks)):
                    weekly_arrivals.append(arrivals.pop(0))
                string += f'Week {week + 1} Arrival Times: {"; ".join(weekly_arrivals)}\n'

        try:
            with open('results.txt', 'w') as stream:
                stream.write(string)
        except Exception as error:
            print(f'Failed to write results to results.txt: {error}')
        else:
            print('Results written to results.txt')
