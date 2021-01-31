import datetime
import json
import math

# Filtering parameters, can be adjusted when necessary
MAX_KM = 1.5
MAX_RESULTS = 10
MAX_DAYS = 122 # 4 months =~ 122 days

# Radius of the earth for calculating the coord difference in km
R = 6372.8



""" Dynamic method which is able to filter on most values """
def get_restaurants_with_filter(restaurants, filter, reverse):
    open_restaurants = restaurants[0]
    closed_restaurants = restaurants[1]
    filtered = sorted(open_restaurants, key=filter, reverse=reverse)   # sort by given lambda function

    # If there are less than 10 nearby open restaurants, apply the same filter on all offline restaurants
    if len(filtered) < 10:
        to_add = 10 - len(filtered)
        offline_filtered = sorted(closed_restaurants, key=filter,  reverse=reverse)

        # Add restaurants from offline list 
        for x, restaurant in enumerate(offline_filtered):
            if x == to_add-1:
                break
            filtered.append(restaurant)

    return filtered[0:10]

""" Unique method for getting the most recent restaurants """
def get_new_restaurants(restaurants):
    new = []
    open_restaurants = restaurants[0]
    closed_restaurants = restaurants[1]
    new_open = sorted(open_restaurants, key=lambda restaurant: abs(restaurant['launch_datetime'] - datetime.datetime.today()))   # sort by recent launch date
   
    # Loop through restaurants, validate whether or not the restaurant is new enough
    for restaurant in new_open:
        if abs(restaurant['launch_datetime'] - datetime.datetime.today()).days < MAX_DAYS:
            new.append(restaurant)

    # If there are less than 10 popular open restaurants, append most popular closed restaurants
    if len(new) < 10:
        to_add = 10 - len(new)
        new_closed = sorted(closed_restaurants, key=lambda restaurant: abs(restaurant['launch_datetime'] - datetime.datetime.today()))   # sort by recent launch date
        tmp = []

        # Loop through restaurants, validate whether or not the restaurant is new enough
        for restaurant in new_closed:
            if abs(restaurant['launch_datetime'] - datetime.datetime.today()).days < MAX_DAYS:
                tmp.append(restaurant)

        # Enumeration instead of for loop, to prevent indexoutofbound exception
        for x, restaurant in enumerate(tmp):
            if x == to_add-1:
                break
            new.append(restaurant)

    return new[0:10]

""" Returns all restaurants which fall within the 1.5km radius"""
def get_potential_restaurants(location):
    potentials_open = []
    potentials_closed = []

    # Open the json file and parse the data
    with open('restaurants.json') as data:
        restaurants = json.load(data)['restaurants']
        for restaurant in restaurants:

            # Check if coordinates are within the max given km range
            distance = coord_to_km(location,restaurant['location'])
            if(distance < MAX_KM):
                # Adding a new temporary value, to convert 
                restaurant['distance'] = distance

                # Creating a new temporary value, as to not convert this multiple times later on
                restaurant['launch_datetime'] = datetime.datetime.strptime(restaurant['launch_date'],'%Y-%m-%d')
                if(restaurant["online"] == True):
                    potentials_open.append(restaurant)
                else:
                    potentials_closed.append(restaurant)
    return (potentials_open, potentials_closed)


# Applying the haversine formula to calculate the difference in KM between location and destination
# Source: https://www.kite.com/python/answers/how-to-find-the-distance-between-two-lat-long-coordinates-in-python
def coord_to_km(location, destination):
    # Convert coordinates to radians
    lat1 = math.radians(location[0])
    lon1 = math.radians(location[1])
    lat2 = math.radians(destination[0])
    lon2 = math.radians(destination[1])

    # Calculate the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    #Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    #Calculate distance in km
    distance = R * c
    return distance