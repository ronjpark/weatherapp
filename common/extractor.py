#
# Copyright and so on..
#

"""
Description of this file
"""

import json

# It is better to define this variable at another file
# Or read them as parameters from the caller
GEOCODE = 'geocode'
WEATHER = 'weather'
EXTRACT_ITEMS = {
    GEOCODE: {
        'location': ['results', 0, 'geometry', 'location'],
        'formatted_address': ['results', 0, 'formatted_address']
    },
    WEATHER: {
        'summary': ['daily', 'data', 0, 'summary'],
        'temperatureHigh': ['daily', 'data', 0, 'temperatureHigh'],
        'temperatureLow': ['daily', 'data', 0, 'temperatureLow']
    }
}


def extract(result_type, input_json, fields):
    """
    Extract the requested values from the posted json string and return the simplified json.
    """
    extract_items = EXTRACT_ITEMS.get(result_type)
    if not extract_items:
        return None
        
    # Get all fields if fields == None
    if fields is None:
        fields = extract_items.keys()

    output_json = {}
    for field in fields:
        path = extract_items.get(field)
        if not path:
            output_json[field] = None
            continue
        pt = input_json
        for key in path:
            if isinstance(key, int):
                pt = pt[key]
            else:
                pt = pt.get(key)
            if not pt:
                break
        output_json[field] = pt
    return output_json        
