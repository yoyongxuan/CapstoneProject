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




# from flask import Flask, render_template, request

# app = Flask("Gay Boy 9000")

# @app.route("/")
# def root():
#     return 'you are gay'#render_template("yes.html", info=None)

# @app.route("/gay")
# def gay():
#     return 'very gay'

# app.run("0.0.0.0")