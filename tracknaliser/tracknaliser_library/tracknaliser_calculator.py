import numpy as np
import requests
import time
import json
from math import *
from random import *
from tracknaliser_library.input_validation import *
import sys



def json_track_calculator(track_details_dict, multi_stop_journey = False, previous_sample_elevation = 0): #accepts one track only in dict form
    """ Generate some list contains time , co2 emissions and distance.


    Parameters
    ----------
    track_details_dict: dictionary
        A dictionary contains basic information about a track, for example: {"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"}


    Returns
    -------
    list
        A list like [co2 emissions, time cost, distance]
        
    """
    flat_fuel_consumption = 0.054
    road_consumption_factors = {"r": [30,1.4], "l": [80,1], "m":[120,1.25]} #speed,factor
    terrain_consumption_factors = {"d": 2.5, "g": 1.25, "p": 1}
    elevation_consumption_factors = {  "-8":0.16,  "-4":0.45,  "0":1,  "4":1.3, "8":2.35,"12":2.9}

    full_stepped_route = []
    sum_of_emissions = []
    sum_of_times = []
    sum_of_distance = []
    chain_code = str(track_details_dict.get("cc"))
    elevation = track_details_dict.get("elevation")
    elevation_0 = int(elevation[0])
    elevation = elevation[1:]
    road = track_details_dict.get("road")
    terrain = track_details_dict.get("terrain")

    full_stepped_route.append([ [ chain_code[step], elevation[step], road[step], terrain[step] ] for step in range(0,len(chain_code)) ])
    full_stepped_route = np.array(full_stepped_route).reshape(-1,4)

    for i,step in enumerate(full_stepped_route):
        distance = 1

        delta_elevation = elevation_0 if i == 0 else int(step[1])-int(full_stepped_route[i-1][1])
        if multi_stop_journey == True:
            delta_elevation = previous_sample_elevation 

        net_distance = np.sqrt((distance*distance)+(delta_elevation/1000)**2)

        if delta_elevation/10>10:
            delta_elevation=12
        elif 6<delta_elevation/10<=10:
            delta_elevation=8
        elif 2<delta_elevation/10<=6:
            delta_elevation=4
        elif -2<=delta_elevation/10<=2:
            delta_elevation=0
        elif -6<=delta_elevation/10<-2:
            delta_elevation=-4
        else:
            delta_elevation=-8
        elevation_factor = elevation_consumption_factors.get(str(delta_elevation))

        road_factor_emission = road_consumption_factors.get(step[2])[1]
        terrain_factor = terrain_consumption_factors.get(step[3])
        time_contribution_seconds = 60*60*net_distance/road_consumption_factors.get(step[2])[0]
        sum_of_emissions.append(2.6391*float(flat_fuel_consumption)*float(net_distance)*float(elevation_factor)*float(road_factor_emission)*float(terrain_factor))
        sum_of_times.append(time_contribution_seconds)
        sum_of_distance.append(net_distance)

        #print("Assesing segment:", step);print("horizontal distance contribution", distance);print("elevation contribution:", delta_elevation);print("net distance contribution:", net_distance, "from root (", delta_elevation, "^2 +", distance, "^2)");print("road contribution:", road_factor_emission, "road travel speed", road_consumption_factors.get(step[2])[0]);print("terrain contribution:", terrain_factor);print("total emission from this step", float(flat_fuel_consumption)*float(net_distance)*float(elevation_factor)*float(road_factor_emission)*float(terrain_factor));print("time contribution from this step", time_contribution_seconds, "seconds");print("--------------------")

    #print("overall emission from this route", sum(sum_of_emissions), "overall time from this route", sum(sum_of_times), "seconds")
    return [sum(sum_of_emissions),sum(sum_of_times),sum(sum_of_distance)]

def request_track(start = (0,0), end = (299,299), min_steps_straight = 1, max_steps_straight = -99, n_tracks = 300):
    """ Get information from online webpage

    Parameters
    ----------
    start: tuple
        A start point in the map , such as (0,0) or (5,5) , between (0,0) to (300,300), default=(0,0)
    end: tuple
        An end point in the map , such as (10,10) or (100,100), between (0,0) to (300,300), default=(299,299)
    min_steps_straight: int
        define minimum step in a direction, default=1
    max_steps_straight: int
        define maximum step in a direction, default=-99
    n_tracks: int
        Number of tracks the webpage returns, default=300

    Returns
    -------
    dictionary
        A whole json file like {"metadata":{"datetime":"2021-12-11T21:12:20","end":[4,2],"mapsize":[5,5],"n_tracks":5,"rangesteps":[1,2],"resolution":1,"start":[2,3],"units_elevation":"m","units_steps":"km"},"tracks":[{"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"},{"cc":"443411122","elevation":[17,12,7,6,1,2,3,4,9,14],"road":"rrrrrrrrr","terrain":"ppddppggg"},{"cc":"3341111","elevation":[17,16,15,10,11,12,13,14],"road":"llrrrrr","terrain":"ddddppg"},{"cc":"21144","elevation":[17,22,23,24,19,14],"road":"mmmlr","terrain":"ppggg"},{"cc":"343411121","elevation":[17,16,11,10,5,6,7,8,13,14],"road":"lrrrrrrrr","terrain":"dddddpppg"}]}
        
    """
    if n_tracks==-1:
        return {"metadata":{"datetime":"2021-12-11T21:12:20","end":[4,2],"mapsize":[5,5],"n_tracks":5,"rangesteps":[1,2],"resolution":1,"start":[2,3],"units_elevation":"m","units_steps":"km"},"tracks":[{"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"},{"cc":"443411122","elevation":[17,12,7,6,1,2,3,4,9,14],"road":"rrrrrrrrr","terrain":"ppddppggg"},{"cc":"3341111","elevation":[17,16,15,10,11,12,13,14],"road":"llrrrrr","terrain":"ddddppg"},{"cc":"21144","elevation":[17,22,23,24,19,14],"road":"mmmlr","terrain":"ppggg"},{"cc":"343411121","elevation":[17,16,11,10,5,6,7,8,13,14],"road":"lrrrrrrrr","terrain":"dddddpppg"}]}
    else:
        if user_input_coordinate_check(start) and user_input_coordinate_check(end):
            start_x = start[0]; start_y=start[1]; end_x = end[0]; end_y=end[1]; 
            if max_steps_straight == -99 or max_steps_straight<min_steps_straight:
                max_steps_straight = int(min_steps_straight + 5) 
            else:
                max_steps_straight=max_steps_straight
            base_url = "http://ucl-rse-with-python.herokuapp.com/road-tracks/tracks/?"
            user_inputs_url = ["start_point_x=",start_x,"&start_point_y=",start_y,"&end_point_x=",end_x,"&end_point_y=",end_y,"&min_steps_straight=",min_steps_straight,"&max_steps_straight=",max_steps_straight,"&n_tracks=",n_tracks]
            user_inputs_url = str(user_inputs_url).replace(",","").replace("[","").replace("]","").replace(" ","").replace("'","")
            request = str(base_url + user_inputs_url)
            returned_request = requests.get(request).json()
            schema_pass_fail = valid_schema_check(returned_request)
            contents_pass_fail = json_contents_check(returned_request)
            if schema_pass_fail and contents_pass_fail:
                print("Fewer routes available than requested (default number of requested tracks is 300)") if returned_request.get("metadata").get("n_tracks") != int(n_tracks) else None
                return returned_request
            else:
                print("Invalid. webapp returned an invalid set of tracks")
                return "Invalid. webapp returned an invalid set of tracks"
        else:
            print("Invalid. webapp returned an invalid set of tracks")
            return "Invalid. webapp returned an invalid set of tracks"



def sort_results(returned_request_track):
    """ Get exact one track according to the criteria

    Parameters
    ----------
    returned_request_track: dictionary
        A dictionary contains basic information about a track, for example: {"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"}


    Returns
    -------
    list
        A list contain 3 tracks [greenest, fastest, shortest] , each element is a dictionary like {"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"}
    """
    dic_tracks={}
    for i,j in enumerate(returned_request_track):
        dic_tracks.update({i:j})
    results_from_tracks = [[index]+json_track_calculator(track) for index,track in enumerate(returned_request_track)]
    # Results are retruned as [time,emission] within a list of lists. 
    # Sorted method sorts by the first element in a 2d array element, the "key = " is required to sort by the second element.
    lowest_emission_route_index= sorted(results_from_tracks,key=lambda x: x[1])[0][0]
    fastest_route_index = sorted(results_from_tracks,key=lambda x: x[2])[0][0]
    shortest_route_index=sorted(results_from_tracks,key=lambda x: x[3])[0][0]
    lowest_emission_route=dic_tracks.get(lowest_emission_route_index)
    fastest_route=dic_tracks.get(fastest_route_index)
    shortest_route=dic_tracks.get(shortest_route_index)



    return [lowest_emission_route,fastest_route,shortest_route]


