# TheSignOutFront by nonetypes
# Last Revised on 03/01/2021
# Sign viewing simulator
#
# A sign cylces through a certain number of slides.
# What percentage of slides will be seen by a person driving by
# the sign x times per week?

from classes import Sign, Student, SignViewingSimulator
from time import time

simulations = []

sign = Sign(20, 20)

simulations = []
for n in range(1000):
    # Create students.
    students = []
    for i in range(1000):
        students.append(Student(i+1))

    start_time = time()
    simulation = SignViewingSimulator(sign, students)
    # simulation.create_schedule(7, 4)
    simulation.create_smart_schedule(1, 4)
    simulation.simulate()
    simulation.calculate_results()
    end_time = time()

    # for key, val in simulation.results.items():
    #     if key == 'Students':
    #         for k, v in simulation.results[key].items():
    #             # print(f'{k}: {v}')
    #             pass
    #     else:
    #         print(f'{key}: {val}')
    simulations.append(simulation.results['Average % of Slides Viewed'])
    print(n, end='\r')

print(round((sum(simulations) / len(simulations)), 2))

# print(end_time - start_time)
