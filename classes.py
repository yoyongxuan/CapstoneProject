class Bus_stop:
    def __init__(self,tup):
        self.BusStopCode = tup[0]
        self.Description = tup[1]
        self.Services = []
        #self.shortest_stop = (Bus_stop object,distance to stop, service)
        self.shortest_stop = None

    def __repr__(self):
        return f"{self.BusStopCode} Object"

    def insert_service(self,bus_service,tup):
        service_dict = {}
        service_dict['ServiceNo'] = tup[0]
        service_dict['Direction'] = tup[1]
        service_dict['StopSequence'] = tup[2]
        service_dict['Distance'] = tup[4]
        service_dict['Object'] = bus_service
        self.Services.append(service_dict)
    def get_next_stops(self):
        #Returns a list of tuples containing:
        #(bus stops one stop away from this bus stop,distance to next stop,bus service)
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

    def get_previous_stops(self):
        #Returns a list of tuples containing:
        #(bus stops one stop to this bus stop,distance to previous stop,bus service)
        result = []
        for service_dict in self.Services:
            #Gets the previous stop and its distance
            previous_stop,previous_stop_distance = service_dict['Object'].route[service_dict['Direction']].get(service_dict['StopSequence']-1,(None,None))
            yeet = False
            for stop in result:
                if previous_stop == stop[0]:
                    stop[2].append(service_dict['ServiceNo'])
                    yeet = True
            if previous_stop != None and not yeet:
                #Gets distance to next stop
                distance = round(service_dict['Distance'] - previous_stop_distance,1)
                if distance != 0:
                    result.append((previous_stop,distance,[service_dict['ServiceNo']]))
        return result
    
    def shortest_distance(self,destination):
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

    def shortest_route(self,destination=None):
        if destination == None:
            destination = self
        for stop,distance,service in self.get_next_stops():
            if (stop.shortest_stop == None):
                stop.shortest_stop = (self,distance,service)
                print([stop,service,stop.shortest_distance(destination)])
                stop.shortest_route(destination)
            elif (stop.shortest_stop[0] == self):
                pass
            elif (self.shortest_distance(destination) + distance < stop.shortest_distance(destination)):
                stop.shortest_stop = (self,distance,service)
                print([stop,service,stop.shortest_distance(destination)])
                stop.shortest_route(destination)
        
    def get_route(self,destination):
        result = []
        if destination == self:
            return result
        else:
            stop = self
            total_distance = 0
            while stop != destination:
                print(stop)
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
        self.route[tup[1]][tup[2]] = (bus_stop,tup[4])
    
    def calculate_distance(self,stop1,stop2,direction):
        pass
        
