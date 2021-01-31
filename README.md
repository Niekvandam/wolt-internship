# Wolt internship project
This is the back-end assignment of the wolt-internship-project. This document will explain the code structure, as well as the unit tests. 

### Requirements
The requirements in order to make this project run are as follows:

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- Flask (can be installed using `pip3 install flask`)

## Api
The api contains the flask API, as well as 1 endpoint, which is the `/discovery` endpoint. This endpoint takes two parameters, lat and lon. It tries to parse these
to floats, and will throw either a code `200` or `400` based on the result of the parsing. 

This file also contains other API-related methods, like the `get_discovery_restaurants`, which will generate a list of the restaurants based on the given location. 

## Restaurantlogic
This file can be seen as the database communication layer, as this is the file which actively reads the JSON file and conjures lists based on the location. 
The method called  `get_restaurants_with_filter` is a dynamic method, which takes in a lambda statement and can filter on all restaurant parameters accordingly. The
exception to this rule is the date variable, as dates need to be uniquely compared and therefore require a seperate method. 

## Unittests
The unittests file uses a built-in python library called unittest. It tests the most prominent features of the API and validates the output. The reason we do not check for parsing errors in the unittests is because these are being handled by the discovery endpoint and use request arguments, which we cannot pass from the back-end code. 

# How to execute code
The API is executed by running the following command in your console: `path/to/python38/python.exe path/to/project/api.py`. Once the api is executed, it will locally host an api. The address of this will be output in the console.
The Unit tests can be ran using almost the same command, but replacing the `api.py` with `unittests.py`. 

