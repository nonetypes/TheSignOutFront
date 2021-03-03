# TheSignOutFront by nonetypes
# Last Revised on 03/01/2021
# Sign viewing simulator
#
# A sign cylces through a certain number of slides.
# What percentage of slides will be seen by a person driving by
# the sign x times per week?

from gui import SignSimulatorWindow
# from classes import Sign, Student, SignViewingSimulator
# from time import time

# sign = Sign(20, 20)

# simulations = []
# for n in range(1):
#     # Create students.
#     students = []
#     for i in range(1000):
#         students.append(Student(i+1))

#     start_time = time()
#     simulation = SignViewingSimulator(sign, students, 1)
#     simulation.create_schedule()
#     simulation.simulate()
#     simulation.calculate_results()
#     end_time = time()

#     for key, val in simulation.results['Averages'].items():
#         print(f'{key}: {val}')

# print(round((sum(simulations) / len(simulations)), 2))

# print(end_time - start_time)

simulator = SignSimulatorWindow()
