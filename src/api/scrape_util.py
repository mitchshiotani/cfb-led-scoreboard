# pseudo-code
# fetch data from api
# save relevant data into variables

import urllib
# import urllib3.request
import json

def api_to_json(url):
    response = urllib.urlopen(url).read()
    # response = urllib3.request.urlopen(url).read()
    return json.loads(response)
