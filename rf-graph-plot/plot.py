import json
import matplotlib.pyplot as pyplot

MAX_DURATION = 3

f = open('output5.json',)

data = json.load(f)

pyplot.plot(data[0], data[1])
pyplot.axis([0, MAX_DURATION, -1, 2])
pyplot.show()
