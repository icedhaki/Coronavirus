import warnings
import requests

import folium 
import webbrowser
import os

import pandas as pd
from googlemaps import convert

import googlemaps
from IPython.display import HTML

# def findplace():
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
#print(names)

array = []
for i in range(0,len(names)):
    name=names[i]+" Michigan"
    data=find_place(gmaps,name,"textquery")
    #print(data)
    can=data['candidates']
    if len(can)>0:
        loc=can[0]
        geo=loc['geometry']
        lat=geo['location']
        lat1=lat['lat']
        lng1=lat['lng']
        tuple1=(lat1,lng1)
        array.append(tuple1)

#print(array)

df1 = pd.read_excel('data1.xlsx', sheet_name='Sheet1')
covid = df1['COVID-19 Patients'].tolist()
icu = df1['COVID-19 Patients in ICU'].tolist()
bed = df['Bed occupancy'].tolist()
#for i in range(0,len(names)):
#    val=

m = folium.Map(
    location=[44.3148, -85.6024],
    zoom_start=7.5,
    tiles='Stamen Terrain'
)

new = []
for i in range(0,len(mylist)):
    s=6-mylist[i]
    new.append(s)

#print(new)

for i in range(0,len(names)):
    string=names[i]+"<br> Number of COVID patients: "+str(covid[i])+"<br> Number of ICU patients: "+str(icu[i]) + "\n <a href=\"https://www.munsonhealthcare.org/munson-healthcare-foundations/ways-to-give/covid-19-response/covid-19-how-you-can-help\">Donate Here</a>"
    if mylist[i]>=0.0 and mylist[i]<0.25:
        c='red'
    elif mylist[i]>=0.25 and mylist[i]<0.5:
        c='orange'
    elif mylist[i]>=0.5 and mylist[i]<0.75:
        c='yellow'
    else:
        c='green'
    
    folium.Circle(
        location=array[i],
        popup=folium.Popup(string, max_width=300,min_width=0),
        radius=5000*(bed[i]+1),
        color=c,
        fill=True,
        fill_color=c
    ).add_to(m)

filepath = "templates/map2.html"
m.save(filepath)