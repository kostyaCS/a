"""
This module includes function, that makes map with distance between two points.
"""
from functools import lru_cache
import googlemaps
import folium
import polyline
from html2image import Html2Image
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')


@lru_cache(maxsize=None)
def distance_betweeen_points(home_point: str, final_distance: str) -> None:
    """
    This function search distance between two points on map with help of Google Maps API.
    The first point is user's destination and the second one - is car's place.
    :param home_point: user's destination point

    :home_point type: str
    :param final_distance: car's place
    :final_distance: str
    :return: None
    """
    gmaps = googlemaps.Client(key=API_KEY)
    distance = gmaps.distance_matrix(home_point, final_distance)['rows'][0]\
    ['elements'][0]['distance']['text']
    return distance


def make_a_map_of_distances(home_point, final_distance) -> None:
    """
    This function builds a map to represent way between two
    dots on map with google api.
    """
    gmaps = googlemaps.Client(key=API_KEY)
    origin_geocode = gmaps.geocode(home_point)[0]['geometry']['location']
    destination_geocode = gmaps.geocode(final_distance)[0]['geometry']['location']
    directions = gmaps.directions(home_point, final_distance, mode='walking')
    polylines = directions[0]['overview_polyline']['points']
    coordinates = polyline.decode(polylines)
    my_map = folium.Map(location=[origin_geocode['lat'], origin_geocode['lng']], zoom_start=15)
    folium.Marker(location=[origin_geocode['lat'], origin_geocode['lng']],\
    icon=folium.Icon(color='lightgray', icon='home', popup=home_point)).add_to(my_map)
    folium.Marker(location=[destination_geocode['lat'], destination_geocode['lng']],\
 icon=folium.Icon(color='lightgray', icon='car', prefix='fa', popup=final_distance)).add_to(my_map)
    folium.PolyLine(locations=coordinates, weight=5, color='blue').add_to(my_map)
    my_map.save('map.html')
    hti = Html2Image()
    with open('map.html') as file_to_write:
        hti.screenshot(file_to_write.read(), save_as='out.png')
