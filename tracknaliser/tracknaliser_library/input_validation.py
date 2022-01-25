import re
import requests
def valid_schema_check(json_to_check):

    valid_schema = True if "metadata" in json_to_check.keys() else False
    valid_schema = valid_schema*True if "tracks" in json_to_check.keys() else False

    tracks_template = set(['terrain', 'elevation', 'road', 'cc'])
    metadata_template = set(['datetime', 'end', 'mapsize', 'n_tracks', 'rangesteps', 'resolution', 'start', 'units_elevation', 'units_steps'])
    
    if valid_schema:
        for track in json_to_check.get("tracks"):
            if set(track.keys()) != tracks_template:
                valid_schema = False
                return valid_schema
        valid_schema = False if json_to_check.get("metadata").keys() != metadata_template else True

    
    return bool(valid_schema)

def json_contents_check(json_to_check):
    if "list" not in str(type(json_to_check.get("tracks"))):
        return False
    for track in json_to_check.get("tracks"):
        cc = track.get("cc")
        cc_list = list(track.get("cc"))

        if "dict" not in str(type(track)):
            return False

        if cc.isdigit() == False:
            return False

        if int(max(cc_list)) > 4 or int(min(cc_list)) < 1:
            return False


        road = track.get("road")
        acceptable_road_inputs = set(re.sub(r'[^rlm]', "" , road))
        if acceptable_road_inputs.symmetric_difference(road):
            return False

        terrain = track.get("terrain")
        elevation = track.get("elevation")

        if len(cc) != len(road) != len(terrain) != len(elevation):
            return False
    return True

def internet_check():
    url = "http://google.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        return True
    except(requests.ConnectionError, requests.Timeout) as exception:
	    return False


def user_input_coordinate_check (coord):   
    input_valid = True
    if "list" in str(type(coord)) or "tuple" in str(type(coord)):
        if len(coord) != 2:
            return False   
            
        acceptable_coord_input = set(re.sub('[^0-9.-]', "" , str(coord[0])))
        if len(acceptable_coord_input.symmetric_difference(str(coord[0]))) == 0:
            input_valid = True*input_valid
        else:
            input_valid = False

        acceptable_coord_input = set(re.sub('[^0-9.-]', "" , str(coord[1])))
        if len(acceptable_coord_input.symmetric_difference(str(coord[1]))) == 0:
            input_valid = True*input_valid
        else:
            input_valid = False
        return bool(input_valid)
    else:
        coord = coord.split()
        if len(coord) != 2:
            return False  
        for element in coord:
            acceptable_coord_input = set(re.sub('[^0-9.-]', "" , str(element)))
            if len(acceptable_coord_input.symmetric_difference(str(element))) == 0:
                input_valid = True*input_valid
            else:
                input_valid = False

            acceptable_coord_input = set(re.sub('[^0-9.-]', "" , str(element)))
            if len(acceptable_coord_input.symmetric_difference(str(element))) == 0:
                input_valid = True*input_valid
            else:
                input_valid = False
        return bool(input_valid)