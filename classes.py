class Bus_stop:
    def __init__(self,tup):
        self.BusStopCode = tup[0]
        self.Description = tup[1]
        self.Services = []
        #List of dictionaries of bus services available at this bus stop
        self.shortest_stop = None
        #Tuple representing the bus stop to travel to to get closer to destination 
        #(Bus_stop object,distance to stop,list of bus services)

    def __repr__(self):
        return f"{self.BusStopCode} Object"

    def insert_service(self,bus_service,tup):
        '''
        Takes in a Bus_service object and a tuple and updates self.Services
        '''

        service_dict = {}
        service_dict['ServiceNo'] = tup[0]
        service_dict['Direction'] = tup[1]
        service_dict['StopSequence'] = tup[2]
        service_dict['Distance'] = tup[4]
        service_dict['Object'] = bus_service
        self.Services.append(service_dict)
    
    def get_next_stops(self):
        '''
        Returns a list of tuples containing bus stops one stop away from this stop
        (bus stop,distance to bus stop,list of bus services)
        '''
        result = []
        for service_dict in self.Services:
            #Gets the next stop and its distance
            next_stop,next_stop_distance = service_dict['Object'].route[service_dict['Direction']].get(service_dict['StopSequence']+1,(None,None))
            yeet = False
            for stop in result:
                if next_stop == stop[0]:
                    stop[2].append(service_dict['ServiceNo'])
                    yeet = True
            if next_stop != None and not yeet:
                #Gets distance to next stop
                distance = round(next_stop_distance - service_dict['Distance'],1)
                if distance != 0:
                    result.append((next_stop,distance,[service_dict['ServiceNo']]))
        return result
    
    def shortest_distance(self,destination):
        '''
        Returns the distance of the shortest route to the destination
        '''
        if destination == self:
            return 0
        else:
            stop = self
            total_distance = 0
            while stop != destination:
                if stop.shortest_stop == None:
                    return None
                next_stop,distance,serviceno = stop.shortest_stop
                total_distance += round(distance,1)
                stop = next_stop
            return round(total_distance,1)

    def get_route(self,destination):
        '''
        Returns the shortest route to the destination in the form of a list and the total distance of the route
        ([(next stop,[list of services to reach stop]),...],total distance)
        '''
        result = []
        if destination == self:
            return result
        else:
            stop = self
            total_distance = 0
            while stop != destination:
                next_stop,distance,serviceno = stop.shortest_stop
                result.append((next_stop,serviceno))
                total_distance += round(distance,1)
                stop = next_stop
            return result,round(total_distance,1)


class Bus_service:
    def __init__(self,tup):
        self.ServiceNo = tup[0]
        self.Category = tup[1]
        self.route = {1:{},2:{}}
        #self.route[Direction][stop sequence] = (bus stop,distance)
    def __repr__(self):
        return f"{self.ServiceNo} Object"
        
    def insert_stop(self,bus_stop,tup):
        #Inserts a bus stop into the bus route
        self.route[tup[1]][tup[2]] = (bus_stop,tup[4])
    
def initialise_classes(c):

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
    return bus_stops,bus_services

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
