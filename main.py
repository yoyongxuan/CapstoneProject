import json,sqlite3
from database import initialise_database
from classes import Bus_stop, Bus_service
import sys
sys.setrecursionlimit(6969)
#This line checks if database has been initialised and initialises it if it hasnt
try:
    f = open("bus_data.db")
except IOError:
    initialise_database()
else:
    f.close()


conn = sqlite3.connect('bus_data.db')
c = conn.cursor()
c.execute(
    """
    SELECT * FROM bus_stops;
    """
)
bus_stop_tups = c.fetchall()
bus_stops = {}
for tup in bus_stop_tups:
    bus_stops[tup[0]] = Bus_stop(tup)

c.execute(
    """
    SELECT * FROM bus_services;
    """
)
bus_service_tups = c.fetchall()
bus_services = {}
for tup in bus_service_tups:
    bus_services[tup[0]] = Bus_service(tup)

c.execute(
    """
    SELECT * FROM bus_routes;
    """
)
bus_route_tups = c.fetchall()
bus_routes = {}
for tup in bus_route_tups:
    #tup = (Service No,Direction,Stop sequence,Bus stop code,Distance)
    bus_stop = bus_stops[tup[3]]
    bus_service = bus_services[tup[0]]
    bus_stop.insert_service(bus_service,tup)
    bus_service.insert_stop(bus_stop,tup)

print(len(bus_stops))
services = bus_stops[75009].Services
stops = bus_stops[75009].get_previous_stops()


def shortest_route(start):
    queue = [start]
    for stop in queue:
        for next_stop,distance,service in stop.get_next_stops():
            if (next_stop.shortest_stop == None):
                next_stop.shortest_stop = (stop,distance,service)
                #print([next_stop,service,next_stop.shortest_distance(start)])
                if next_stop not in queue:
                    queue.append(next_stop)
            elif (next_stop.shortest_stop[0] == stop):
                pass
            elif (stop.shortest_distance(start) + distance < next_stop.shortest_distance(start)):
                next_stop.shortest_stop = (stop,distance,service)
                #print([next_stop,service,next_stop.shortest_distance(start)])
                if next_stop not in queue:
                    queue.append(next_stop)
            else:
                pass

shortest_route(bus_stops[75009])
print('a')
#bus_stops[75009].shortest_route()

#print(bus_stops[96241].shortest_distance(bus_stops[75009]))

#data = []
# for bus_stop in bus_stops.values():
#     data.append(f'{bus_stop} {bus_stop.shortest_distance(bus_stops[75009])}\n')

    #print(bus_stop,end=' , ')
    #print(bus_stop.shortest_distance(bus_stops[75009]))

# with open('depth_first.txt','w') as f:
#     f.writelines(data)

#print(bus_stops[76131].get_route(bus_stops[75009]))
