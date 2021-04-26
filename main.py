import json,sqlite3
from database import initialise_database
from classes import Bus_stop, Bus_service,initialise_classes,shortest_route,get_distances
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

from flask import Flask, render_template, request

app = Flask("Gay Boy 9000")

@app.route("/")
def root():
    print(request.args.get('bus_stop',None))
    return render_template("home.html", info=None)

@app.route("/distances")
def distances():
    bus_stop = bus_stops[int(request.args.get('bus_stop',None))]
    shortest_route(bus_stop)
    result = get_distances(bus_stops,bus_stop)
    print(result)
    return request.args.get('bus_stop',None)

app.run("0.0.0.0")