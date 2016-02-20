import numpy
from matplotlib.pyplot import plot, savefig
from Carpool import *

uniform = numpy.random.uniform
randint = numpy.random.randint

carpool = Carpool()

N_City = 10
N_Passenger = 1000
Range = 5
N_Trip = 0

Cities = []

def randLoc():
    city = Cities[randint(0, N_City)]
    return [city[0] + uniform(-Range, Range), city[1] + uniform(-Range, Range)]

for i in range(N_City):
    Cities.append([uniform(0, 200), uniform(0, 200)])

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

savefig('output.eps', format='eps', dpi=1000)
