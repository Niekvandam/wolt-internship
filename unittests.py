import unittest
import restaurantlogic

class TestAPIMethods(unittest.TestCase):

    """ Test if the coordinate to km calculation works """
    def test_km_calculation(self):
        helsinki = (60.1699, 24.9384)
        eindhoven = (51.4416, 5.4697)
        self.assertEqual(1547, round(restaurantlogic.coord_to_km(eindhoven, helsinki)))
    
    """" Test if given coordinate returns expected results """
    def test_potential_restaurants(self):
        location = (24.935326,60.15621)
        restaurants = restaurantlogic.get_potential_restaurants(location)
        self.assertEqual(len(restaurants[0]), 32)
        self.assertEqual(len(restaurants[1]), 22)

    """ Validate that no restaurants are suggested when the coordinates are out of range"""
    def test_potential_restaurants_out_range(self):
        location = (123.456, 345,678)
        restaurants = restaurantlogic.get_potential_restaurants(location)
        self.assertEqual(len(restaurants[0]), 0)
        self.assertEqual(len(restaurants[1]), 0)

    """ Validate that no restaurants are suggested when the coordinates are out of range"""
    def test_new_restaurants_max_return(self):
        location = (24.935326,60.15621)
        restaurants = restaurantlogic.get_potential_restaurants(location)

        result = restaurantlogic.get_new_restaurants(restaurants)

        self.assertLessEqual(len(result), 10)

    """ Test whether or not the max return value is 10 of getting restaurants with filter"""
    def test_get_restaurants_with_filter_max_return(self):
        location = (24.935326,60.15621)
        restaurants = restaurantlogic.get_potential_restaurants(location)

        result = restaurantlogic.get_restaurants_with_filter(restaurants, lambda restaurant: restaurant['popularity'], True)

        self.assertLessEqual(len(result), 10)

    """ Test whether or not popularity is decreasing """
    def test_popular_rankings(self):
        location = (24.935326,60.15621)
        restaurants = restaurantlogic.get_potential_restaurants(location)

        result = restaurantlogic.get_restaurants_with_filter(restaurants, lambda restaurant: restaurant['popularity'], True)

        for x, restaurant in enumerate(result[1:]):
            self.assertLessEqual(restaurant['popularity'], result[x]['popularity'])

    """`test whether or not distance ordering is working """
    def test_distance_rankings(self):
        location = (24.935326,60.15621)
        restaurants = restaurantlogic.get_potential_restaurants(location)

        result = restaurantlogic.get_restaurants_with_filter(restaurants, lambda restaurant:  restaurant['distance'], False)

        for x, restaurant in enumerate(result[1:]):
            self.assertGreaterEqual(restaurant['distance'], result[x]['distance'])

if __name__ == '__main__':
    unittest.main()