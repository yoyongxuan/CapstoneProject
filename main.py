import json,sqlite3
from database import initialise_database
from classes import Bus_stop, Bus_service,initialise_classes,shortest_route
from interface import Interface
from flask import Flask, render_template, request
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

app = Flask("Gay Boy 9000")
info = Interface()

@app.route("/")
def root():
    print(request.args.get('bus_stop',None))
    return render_template("home.html")

@app.route("/distances")
def distances():
    bus_stop = bus_stops[int(request.args.get('bus_stop',None))]
    info.start = bus_stop
    shortest_route(bus_stop)
    info.add_distances(bus_stops,bus_stop)
    print(info.distances)
    return render_template("distances.html", info=info)

@app.route("/route")
def route():
    start = info.start
    destination = bus_stops[int(request.args.get('destination',None))]
    print(destination.get_route(start))
    return destination.Description

app.run("0.0.0.0")