# GUI for TheSignOutFront
# SimulatorWindow

import tkinter as tk
from threading import Thread
from json import loads, dumps
from time import time
from classes import Sign, Student, SignViewingSimulator


class SignSimulatorWindow:
    """Tkinter window for entering simulation parameters and running simulations.
    """
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('SignViewingSimulator')
        self.entries = {}

        self.window.geometry('293x336')
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
        self.students_time_label = tk.Label(self.students_frame, text='View Duration',
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

        # Simulation Frame
        self.simulation_frame = tk.LabelFrame(self.window, text='Simulation')
        self.simulation_frame.grid(row=2, column=0, padx=4, pady=4, columnspan=2, sticky='w')
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
        # self.run() is threaded to allow real-time status updates e.g. when running many simulations.
        self.simulation_run_button = tk.Button(self.window, text='Run', width=8, command=self.start_thread)
        self.simulation_run_button.grid(row=3, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='n')
        # Bind Run to enter key.
        self.window.bind('<Return>', self.enter_key)

        # Status Label
        self.status_label = tk.Label(self.window)
        self.status_label.grid(row=4, column=0, padx=self.padx, pady=self.pady, columnspan=2, sticky='n')

        self.load_settings()
        self.window.mainloop()

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

    def run(self):
        """Run the simulation(s) from the entered parameters in the entry boxes.
        """
        self.get_entries()

        simulation_string = f"{self.entries['simulation_num']} Simulation"
        simulation_string += ':' if self.entries['simulation_num'] == 1 else 's:'
        print(simulation_string)

        simulations = {'Average Unique Slides Viewed': [],
                       'Average # of Slides Viewed': [],
                       'Average % of Slides Viewed': []}

        sign = Sign(self.entries['slide_num'], self.entries['slide_duration'])

        # Run n number of simulations
        for n in range(self.entries['simulation_num']):
            # Update status message.
            self.status_label.configure(text=f'Running Simulation {n+1}')
            print(f'Running Simulation {n+1}', end='\r')
            # Create Students
            students = []
            for i in range(self.entries['student_num']):
                students.append(Student(i+1, self.entries['student_duration'], self.entries['student_views']))

            simulation = SignViewingSimulator(sign, students, self.entries['simulation_duration'])
            simulation.create_schedule()
            simulation.simulate()
            simulation.calculate_results()

            for key, val in simulation.results['Averages'].items():
                simulations[key].append(val)

        # Print average results across any/all simulations.
        for key, val in simulations.items():
            print(f'{key}: {round((sum(val) / len(val)), 2)}')

        # for student in students:
            # print(student.arrival_times)
            # print(student.slides_seen)

        self.status_label.configure(text='Simulations Complete')

    def start_thread(self):
        """Execute run() when the "Run" button is pressed.

        run() is threaded to allow real-time updating of status messages.

        While run() is running, disable "Run" button with
        check_thread() until simulations are complete.

        https://stackoverflow.com/a/56953613
        """
        thread = Thread(target=self.run)
        thread.start()

        self.check_thread(thread)

    def check_thread(self, thread):
        """Used in self.start_thread to prevent "Run" button from beginning
        additional simulations until all current simulations have completed.

        If the thread is active, call check_thread() again after .5 seconds.
        """
        if thread.is_alive():
            self.simulation_run_button.configure(command=lambda: print('Simulations in Progress'))
            self.window.unbind('<Return>')
            self.window.after(500, lambda: self.check_thread(thread))
        else:
            self.simulation_run_button.configure(command=self.start_thread)
            self.window.bind('<Return>', self.enter_key)

    def enter_key(self, event):
        """For binding the enter key to start_thread() and ultimately run().
        """
        self.start_thread()

    def get_entries(self):
        """Retrieve and store the entries from the entry boxes.
        """
        entries = {}
        entries['slide_num'] = self.sign_num_entry.get()
        entries['slide_duration'] = self.sign_time_entry.get()
        entries['student_num'] = self.students_num_entry.get()
        entries['student_duration'] = self.students_time_entry.get()
        entries['student_views'] = self.students_views_entry.get()
        entries['simulation_num'] = self.simulation_num_entry.get()
        entries['simulation_duration'] = self.simulation_time_entry.get()

        # Typecast to integers.
        for key, val in entries.items():
            # If there was no entry, set it to 1.
            if not entries[key]:
                entries[key] = 1
            else:
                entries[key] = int(val)

        self.entries = entries

    def load_settings(self):
        """Attempt to load settings and apply entries to entry boxes.
        """
        try:
            settings = loads(open('settings', 'r').read())
        except Exception:
            print('No settings file found.')
        else:
            self.sign_num_entry.insert(0, str(settings['slide_num']))
            self.sign_time_entry.insert(0, str(settings['slide_duration']))
            self.students_num_entry.insert(0, str(settings['student_num']))
            self.students_time_entry.insert(0, str(settings['student_duration']))
            self.students_views_entry.insert(0, str(settings['student_views']))
            self.simulation_num_entry.insert(0, str(settings['simulation_num']))
            self.simulation_time_entry.insert(0, str(settings['simulation_duration']))

    def save_settings(self):
        """Save the last retrieved entries entered in entry boxes to settings file.
        """
        if self.entries:
            try:
                with open('settings', 'w') as stream:
                    stream.write(dumps(self.entries))
            except Exception as error:
                print(f'Settings not saved: {error}')
            else:
                print('Settings saved successfully.')
