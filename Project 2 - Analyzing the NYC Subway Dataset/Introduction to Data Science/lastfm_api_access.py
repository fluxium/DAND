import json
import requests

#def api_get_request(url):
    # In this exercise, you want to call the last.fm API to get a list of the
    # top artists in Spain.
    #
    # Once you've done this, return the name of the number 1 top artist in Spain.
url = "http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=spain&api_key=4cd7f584a440c68db93e306697acc14c&format=json"
rawText = requests.get(url).text
rawJSON = json.loads(rawText)

for i in rawJSON['topartists']['artist']:
    if int(i['@attr']['rank']) == 1:
        print(i['name'])
        #return i['name']

#print(i['@attr']['rank'])
    
#print("/n/n ARTIST /n/n")
#print(rawJSON['topartists']['artist'['@attr']['rank'])
    #return 1 #rawJSON['artist'] # return the top artist in Spain
