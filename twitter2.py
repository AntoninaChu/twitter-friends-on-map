import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
geolocator = Nominatim()

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

def twitter_data(acct):
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    while True:
        if (len(acct) < 1): break
        url = twurl.augment(TWITTER_URL,
                            {'screen_name': acct, 'count': '5'})
        # print('Retrieving', url)
        connection = urllib.request.urlopen(url, context=ctx)
        data = connection.read().decode()

        js = json.loads(data)
        # print (json.dumps(js, indent=2))
        return js

        headers = dict(connection.getheaders())
        # print('Remaining', headers['x-rate-limit-remaining'])

        for u in js['users']:
            print(u['screen_name'])
            if 'status' not in u:
                print('   * No status found')
                continue
            s = u['status']['text']
            # print('  ', s[:50])

def create_map(acct):
    data = twitter_data(acct)
    name = []
    location = []
    for i in data['users']:
        name.append(i['screen_name'])
        location.append(i['location'])

    maps = folium.Map(location=[34.14391585, -118.761143806617],  zoom_start=5)

    fg_y = folium.FeatureGroup(name='your_friends')

    for n, l in zip(name, location):
        try:
            location2 = geolocator.geocode(l)
            coordinates = (location2.latitude, location2.longitude)
        except AttributeError:
            pass
        fg_y.add_child(folium.Marker(location=coordinates,
                                     icon=folium.Icon(),
                                     popup=n))

    maps.add_child(fg_y)
    maps.add_child(folium.LayerControl())
    maps.save('MAP_NEW.html')
    html_code = ""
    with open("MAP_NEW.html","r") as map_file:
        for line in map_file.readlines():
            html_code += line
    return html_code
    
acct = input("Enter twitter account: ")
create_map(acct)
