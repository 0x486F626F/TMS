import math

CAR_SPEED = 1.67

def time_estimation(origin, destination):
    dist = math.sqrt((origin[0] - destination[0]) ** 2 + \
            (origin[1] - destination[1]) ** 2)
    return dist / CAR_SPEED

class Passenger:
    def __init__(self, origin, destination, leave_after, arrive_by):
        self.origin = origin
        self.destination = destination
        self.leave_after = leave_after
        self.arrive_by = arrive_by

class Trip: #{{{
    def __init__(self, driver, max_seats):
        self.driver = driver
        self.max_seats = max_seats

        self.travel_time = time_estimation(driver.origin, driver.destination)
        self.passengers = [driver]
        self.pass_by = [
                {'location': driver.origin, 
                    'time': 0,
                    'action': 'Pick',
                    'passenger': driver,
                    'occupied_seats': 1},
                {'location': driver.destination, 
                    'time': self.travel_time,
                    'action': 'Drop',
                    'passenger': driver,
                    'occupied_seats': 0}]

    def check_availability(self, passenger):
        min_extra_time = self.driver.arrive_by - self.driver.leave_after - self.travel_time
        info = None
        for pick in range(1, len(self.pass_by)):
            for drop in range(pick, len(self.pass_by)):

                available = True
                count = 0
                for idx in range(len(self.pass_by)):
                    if self.pass_by[idx]['action'] == 'Pick':
                        count += 1
                    if idx == pick - 1:
                        count += 1
                    if self.pass_by[idx]['action'] == 'Drop':
                        count -= 1
                    if idx == drop:
                        count -= 1
                    if count > self.max_seats:
                        available = False
                if not available:
                    continue

                pick_time = self.pass_by[pick - 1]['time'] + time_estimation(self.pass_by[pick - 1]['location'], passenger.origin)

                extra_time = 0
                drop_time = pick_time
                extra_time += time_estimation(self.pass_by[pick - 1]['location'], passenger.origin)
                extra_time += time_estimation(passenger.destination, self.pass_by[drop]['location'])
                if pick == drop:
                    pick_to_drop = time_estimation(passenger.origin, passenger.destination)
                    extra_time += pick_to_drop
                    extra_time -= (self.pass_by[drop]['time'] - self.pass_by[pick - 1]['time'])
                    drop_time += pick_to_drop
                else:
                    after_pick = time_estimation(passenger.origin, self.pass_by[pick]['location'])
                    before_drop = time_estimation(self.pass_by[drop - 1]['location'], passenger.destination)
                    extra_time += after_pick + before_drop
                    extra_time -= (self.pass_by[pick]['time'] - self.pass_by[pick - 1]['time'])
                    extra_time -= (self.pass_by[drop]['time'] - self.pass_by[drop - 1]['time'])
                    drop_time += after_pick + before_drop + \
                            (self.pass_by[drop - 1]['time'] - self.pass_by[pick]['time'])

                latest_pick_time = self.driver.arrive_by - (self.travel_time + extra_time) + pick_time
                earliest_drop_time = self.driver.leave_after + drop_time

                if latest_pick_time >= passenger.leave_after and \
                        earliest_drop_time <= passenger.arrive_by and \
                        extra_time < min_extra_time: 
                            min_extra_time = extra_time
                            info = {
                                    'extra_time': extra_time,
                                    'pick_time': pick_time,
                                    'drop_time': drop_time,
                                    'index': [pick, drop + 1]}
        return info

    def join(self, passenger, index):
        self.pass_by.insert(index[0], 
                {'location': passenger.origin, 
            'action': 'Pick',
            'passenger': passenger})
        self.pass_by.insert(index[1], 
                {'location': passenger.destination, 
            'action': 'Drop',
            'passenger': passenger})
        for idx in range(index[0], len(self.pass_by)):
            self.pass_by[idx]['time'] = self.pass_by[idx - 1]['time'] + \
                    time_estimation(self.pass_by[idx - 1]['location'], self.pass_by[idx]['location'])
            if self.pass_by[idx]['action'] == 'Pick':
                self.pass_by[idx]['occupied_seats'] = self.pass_by[idx - 1]['occupied_seats'] + 1
            else:
                self.pass_by[idx]['occupied_seats'] = self.pass_by[idx - 1]['occupied_seats'] - 1

        self.travel_time = self.pass_by[-1]['time']

    def print_summary(self):
        for each in self.pass_by:
            print each
#}}}

class Carpool:
    def __init__(self):
        self.scheduled_trips = []

    def add_new_trip(self, trip):
        self.scheduled_trips.append(trip)

    def find_carpool(self, passenger):
        available_list = []
        for trip in self.scheduled_trips:
            info = trip.check_availability(passenger)
            if info is not None:
                available_list.append({'trip': trip, 'info': info})
        available_list.sort(key = lambda x: x['info']['extra_time'])
        return available_list

    def join_carpool(self, schedule, passenger):
        schedule['trip'].join(passenger, schedule['info']['index'])

    def print_all_trip(self):
        for trip in self.scheduled_trips:
            trip.print_summary()
            print '======================='
