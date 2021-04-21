import json,sqlite3
from database import initialise_database
from classes import Bus_stop, Bus_service,initialise_classes,shortest_route
import sys

#This checks if database has been initialised and initialises it if it hasnt
try:
    f = open("bus_data.db")
except IOError:
    initialise_database()
else:
    f.close()


conn = sqlite3.connect('bus_data.db')
c = conn.cursor()
bus_stops,bus_services = initialise_classes(c)
c.close()



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

print(bus_stops[96241].get_route(bus_stops[75009]))
