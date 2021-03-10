# TheSignOutFront by nonetypes
# Last Revised on 03/09/2021
# Sign viewing simulator
#
# A sign cylces through a certain number of slides.
# What percentage of slides will be seen by a person driving by
# the sign x times per week?
#
# Answer: 1000 simulations were run with 1000 students where each student
# drove past a sign with 20 slides on a circular cycle which were displayed
# for 20 seconds each. Students drove by the sign 4 times per week and could see
# the sign for 60 seconds (normal distribution standard deviation of 5 seconds).
# Students only saw a slide when viewed for a minimum of 2 seconds.
# Students were given a schedule where they aimed to arrive at a certain time
# on a given day each week with a standard deviation of 300 seconds.
# Across all simulations, students saw an average of
# 57.56% of the slides after 1 week,
# 81.91% of the slides after 2 weeks, and
# 92.28% of the slides after 3 weeks.
# Displaying slides randomly where the same slide could not be chosen two times in a row
# effected the percentage of slides seen negatively. Students saw an average of
# 56.05% of the slides after 1 week,
# 80.62% of the slides after 2 weeks, and
# 91.43% of the slides after 3 weeks.

from gui import SignSimulatorWindow

simulator = SignSimulatorWindow()
