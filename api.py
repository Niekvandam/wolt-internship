# Api libraries
import flask
from flask import request, jsonify
# Used for calculating the distance between two coords
import math

# Used for parsing potential restaurants
import json
import datetime

import restaurantlogic

# Return status codes
BAD_REQUEST = 400
OK = 200



app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/discovery', methods=["GET"])
def discovery():
    # Check if lat & lon params were supplied, if so, convert to float
    if 'lat' and 'lon' in request.args:
        try:
            lat = float(request.args['lat'])
            lon = float(request.args['lon'])
            location = (lat, lon)
            values = get_discovery_restaurants(location)
        except ValueError:
            return "The supplied coordinates are invalid", BAD_REQUEST
        except TypeError:
            return "The supplied coordinates could not be parsed to a Float", BAD_REQUEST
        return values,  OK
    else:
        return "Invalid location parameters were supplied", BAD_REQUEST

""" Retrieve the 3 different lists of restaurants and parse them """
def get_discovery_restaurants(location):
    restaurants = restaurantlogic.get_potential_restaurants(location)
    popular = restaurantlogic.get_restaurants_with_filter(restaurants, lambda restaurant: restaurant['popularity'], True)
    nearby = restaurantlogic.get_restaurants_with_filter(restaurants, lambda restaurant:  restaurant['distance'], False)
    new = restaurantlogic.get_new_restaurants(restaurants)
    values = format_return_json(popular, new, nearby)
    return values

""" Format the 3 result lists into a json dictionary"""
def format_return_json(popular, new, nearby):
    # Used as index for clearing unused dictionaries
    removed = 0
    values = {"sections": [{},{},{}]}
    if(len(popular) != 0):
        values['sections'][0]['title'] = "Popular Restaurants"
        values['sections'][0]['restaurants'] = popular
    else:
        removed +=1
        del values['sections'][0]
    if(len(new) != 0):
        values['sections'][1]['title'] = "New Restaurants"
        values['sections'][1]['restaurants'] = new
    else:
        removed +=1
        del values['sections'][1 - removed]
    if(len(nearby) != 0):
        values['sections'][2]['title'] = "Nearby Restaurants"
        values['sections'][2]['restaurants'] = nearby
    else:
        del values['sections'][2 - removed]
    return values


app.run()