# pseudo-code
# fetch data from api
# save relevant data into variables

import urllib.request
# import urllib3.request
import json

def api_to_json(url_str):
    # response = urllib.urlopen(url).read()
    # response = urllib3.request.urlopen(url).read()
    with urllib.request.urlopen(url_str) as url:
        response = url.read()
        # I'm guessing this would output the html source code ?
        return json.loads(response)
