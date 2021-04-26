
class Interface():
    def __init__(self):
        self.distances = None
        self.start = None
    def add_distances(self,bus_stops,start):
        result = []
        for bus_stop_code in bus_stops:
            bus_stop = bus_stops[bus_stop_code]
            distance = bus_stop.shortest_distance(start)
            result.append([bus_stop.Description,distance,bus_stop_code])
        self.distances = result