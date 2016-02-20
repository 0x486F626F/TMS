import numpy
from matplotlib.pyplot import plot, savefig
from Carpool import *

uniform = numpy.random.uniform
randint = numpy.random.randint

carpool = Carpool()

N_City = 20
N_Passenger = 1000
Range = 10
N_Trip = 0

Cities = []

def randLoc():
    loc = Cities[randint(0, N_City)]
    loc[0] += uniform(-Range, Range)
    loc[1] += uniform(-Range, Range)
    return loc

for i in range(N_City):
    Cities.append([uniform(0, 100), uniform(0, 100)])

for i in range(N_Passenger):
    origin = randLoc()
    destination = randLoc()
    leave = uniform(0, 120)
    arrive = leave + time_estimation(origin, destination) * uniform(1.2, 1.5)
    passenger = Passenger(origin, destination, leave, arrive)
    schedule = carpool.find_carpool(passenger)
    if len(schedule) > 0:
        carpool.join_carpool(schedule[0], passenger)
    else:
        carpool.add_new_trip(Trip(passenger, 4))
        N_Trip += 1

carpool.print_all_trip()
print N_Trip

for trip in carpool.scheduled_trips:
    x = []
    y = []
    for each in trip.pass_by:
        x.append(each['location'][0])
        y.append(each['location'][1])
    plot(x, y, color = numpy.random.rand(3,1), marker = '+')

for city in Cities:
    plot(city[0], city[1], color = numpy.random.rand(3,1), marker = 'o')

savefig('output.png', dpi=None, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None)
