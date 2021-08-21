# pseudo-code
# fetch data from api
# save relevant data into variables

import urllib.request
import json

def api_to_json(url):
    response = urllib.request.urlopen(url).read()
    return json.loads(response)

