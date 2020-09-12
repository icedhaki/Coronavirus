import warnings
import requests

import folium 
import webbrowser
import os

import pandas as pd
from googlemaps import convert

import googlemaps
from IPython.display import HTML


gmaps = googlemaps.Client(key='AIzaSyAAlKbMkLx5wF1XelCl3IYr9iMFzQH4BoQ')


PLACES_FIND_FIELDS_BASIC = set(
    [
        "business_status",
        "formatted_address",
        "geometry",
        "geometry/location",
        "geometry/location/lat",
        "geometry/location/lng",
        "geometry/viewport",
        "geometry/viewport/northeast",
        "geometry/viewport/northeast/lat",
        "geometry/viewport/northeast/lng",
        "geometry/viewport/southwest",
        "geometry/viewport/southwest/lat",
        "geometry/viewport/southwest/lng",
        "icon",
        "name",
        "permanently_closed",
        "photos",
        "place_id",
        "plus_code",
        "types",
    ]
)

PLACES_FIND_FIELDS_CONTACT = set(["opening_hours"])

PLACES_FIND_FIELDS_ATMOSPHERE = set(["price_level", "rating", "user_ratings_total"])

PLACES_FIND_FIELDS = (
    PLACES_FIND_FIELDS_BASIC
    ^ PLACES_FIND_FIELDS_CONTACT
    ^ PLACES_FIND_FIELDS_ATMOSPHERE
)

PLACES_DETAIL_FIELDS_BASIC = set(
    [
        "address_component",
        "adr_address",
        "business_status",
        "formatted_address",
        "geometry",
        "geometry/location",
        "geometry/location/lat",
        "geometry/location/lng",
        "geometry/viewport",
        "geometry/viewport/northeast",
        "geometry/viewport/northeast/lat",
        "geometry/viewport/northeast/lng",
        "geometry/viewport/southwest",
        "geometry/viewport/southwest/lat",
        "geometry/viewport/southwest/lng",
        "icon",
        "name",
        "permanently_closed",
        "photo",
        "place_id",
        "plus_code",
        "type",
        "url",
        "utc_offset",
        "vicinity",
    ]
)

PLACES_DETAIL_FIELDS_CONTACT = set(
    ["formatted_phone_number", "international_phone_number", "opening_hours", "website"]
)

PLACES_DETAIL_FIELDS_ATMOSPHERE = set(
    ["price_level", "rating", "review", "user_ratings_total"]
)

PLACES_DETAIL_FIELDS = (
    PLACES_DETAIL_FIELDS_BASIC
    ^ PLACES_DETAIL_FIELDS_CONTACT
    ^ PLACES_DETAIL_FIELDS_ATMOSPHERE
)

DEPRECATED_FIELDS = {"permanently_closed"}
DEPRECATED_FIELDS_MESSAGE = (
    "Fields, %s, are deprecated. "
    "Read more at https://developers.google.com/maps/deprecations."
)


def find_place(
    client, input, input_type, fields=['geometry/location','formatted_address'], location_bias=None, language=None
):
    """
    A Find Place request takes a text input, and returns a place.
    The text input can be any kind of Places data, for example,
    a name, address, or phone number.
    :param input: The text input specifying which place to search for (for
                  example, a name, address, or phone number).
    :type input: string
    :param input_type: The type of input. This can be one of either 'textquery'
                  or 'phonenumber'.
    :type input_type: string
    :param fields: The fields specifying the types of place data to return. For full details see:
                   https://developers.google.com/places/web-service/search#FindPlaceRequests
    :type fields: list
    :param location_bias: Prefer results in a specified area, by specifying
                          either a radius plus lat/lng, or two lat/lng pairs
                          representing the points of a rectangle. See:
                          https://developers.google.com/places/web-service/search#FindPlaceRequests
    :type location_bias: string
    :param language: The language in which to return results.
    :type language: string
    :rtype: result dict with the following keys:
            status: status code
            candidates: list of places
    """
    params = {"input": input, "inputtype": input_type}

    if input_type != "textquery" and input_type != "phonenumber":
        raise ValueError(
            "Valid values for the `input_type` param for "
            "`find_place` are 'textquery' or 'phonenumber', "
            "the given value is invalid: '%s'" % input_type
        )

    if fields:
        deprecated_fields = set(fields) & DEPRECATED_FIELDS
        if deprecated_fields:
            warnings.warn(
                DEPRECATED_FIELDS_MESSAGE % str(list(deprecated_fields)),
                DeprecationWarning,
            )

        invalid_fields = set(fields) - PLACES_FIND_FIELDS
        if invalid_fields:
            raise ValueError(
                "Valid values for the `fields` param for "
                "`find_place` are '%s', these given field(s) "
                "are invalid: '%s'"
                % ("', '".join(PLACES_FIND_FIELDS), "', '".join(invalid_fields))
            )
        params["fields"] = convert.join_list(",", fields)

    if location_bias:
        valid = ["ipbias", "point", "circle", "rectangle"]
        if location_bias.split(":")[0] not in valid:
            raise ValueError("location_bias should be prefixed with one of: %s" % valid)
        params["locationbias"] = location_bias
    if language:
        params["language"] = language
    return client._request("/maps/api/place/findplacefromtext/json", params)

df = pd.read_excel('data.xlsx', sheet_name='Sheet1') # can also index sheet by name or fetch all sheets
mylist = df['final score'].tolist()
print(mylist)
names = df['Health System/Hospital'].tolist()
print(names)

array = []
for i in range(0,len(names)):
    name=names[i]+" Michigan"
    data=find_place(gmaps,name,"textquery")
    print(data)
    can=data['candidates']
    if len(can)>0:
        loc=can[0]
        geo=loc['geometry']
        lat=geo['location']
        lat1=lat['lat']
        lng1=lat['lng']
        tuple1=(lat1,lng1)
        array.append(tuple1)

print(array)




#for i in range(0,len(names)):
#    val=

m = folium.Map(
    location=[44.3148, -85.6024],
    zoom_start=7.5,
    tiles='Stamen Terrain'
)

for i in range(0,len(names)):
   folium.Circle(
      location=array[i],
      popup=names[i],
      radius=1000*mylist[i],
      color='red',
      fill=True,
      fill_color='red'
   ).add_to(m)

filepath = "map.html"
m.save(filepath)
webbrowser.open('file://' + filepath)




'''
for lat, lon, traffic_q, traffic, bike, city in zip(df['latitude'], df['longitude'], df['traffic_index_quartile'], df['traffic_index'], df['bike_score'], df['city']):
    folium.CircleMarker(
        [lat, lon],
        radius=.15*bike,
        popup = ('City: ' + str(city).capitalize() + '<br>'
                 'Bike score: ' + str(bike) + '<br>'
                 'Traffic level: ' + str(traffic) +'%'
                ),
        color='b',
        key_on = traffic_q,
        threshold_scale=[0,1,2,3],
        fill_color=colordict[traffic_q],
        fill=True,
        fill_opacity=0.7
        ).add_to(traffic_map)
traffic_map
'''