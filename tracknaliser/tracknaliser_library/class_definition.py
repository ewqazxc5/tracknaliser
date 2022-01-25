import json
from xxlimited import Str
from tracknaliser_library.tracknaliser_calculator import *
from math import *
from random import *
import time
import matplotlib.pyplot as plt
from tracknaliser_library.clustering import cluster
import os
import datetime


class SingleTrack(object):
    '''
    The definition of SinleTrack

    Parameters
    ----------
    start:tuple
        A start point in the map , such as (0,0) or (5,5) , between (0,0) to (300,300)
    cc:str
        A string for chain code, for example:"11233344111"
    road:str
        A string for description of the road, for example:"llmmmmlrrrr"(r:residential,l:local,m:motorway)
    terrain:str
        A string for decription of the road for example:"pggppdddppg"(d:dirty,g:gravel,p:paved)
    elevation:list
        To describe the height, for example:[17,18,19,24,23,22,21,16,11,12,13,14]
    
    Attributes
    ----------
    start:tuple
        A start point in the map , such as (0,0) or (5,5) , between (0,0) to (300,300)
    cc:str
        A string for chain code, for example:"11233344111"
    road:str
        A string for description of the road, for example:"llmmmmlrrrr"(r:residential,l:local,m:motorway)
    terrain:str
        A string for decription of the road for example:"pggppdddppg"(d:dirty,g:gravel,p:paved)
    elevation:list
        To describe the height, for example:[17,18,19,24,23,22,21,16,11,12,13,14]
    dic:dictionary
        Combination of the information of the track
    '''
    def __init__(self,start,cc,road,terrain,elevation):
        self.start = start
        self.cc = cc
        self.road = road
        self.terrain = terrain
        self.elevation = elevation
        self.dic={'cc':cc,"elevation":elevation,"road":road,"terrain":terrain}

        self.__dx = [1, 0, -1, 0]
        self.__dy = [0, 1, 0, -1]
        self.__terrain_map = {'d': 2.5, 'g': 1.25, 'p': 1}
        self.__road_map = {'r': (30, 1.4), 'l': (80, 1), 'm': (120, 1.25)}
        self.__slope = [
            (-6, 0.16),
            (-2, 0.45),
            (2, 1.0),
            (6, 1.3),
            (10, 2.35),
            (None, 2.90)
        ]

    def __len__(self):
        return len(self.cc)

    def __str__(self):
        return f"<SingleTrack: starts at {self.start} - {self.__len__()} steps>"

    def __coords(self):
        coords = [self.start]

        cur = self.start

        for i in range(self.__len__() - 1):
            chaincode = int(self.cc[i]) - 1
            nc = [None, None]
            nc[0] = cur[0] +  self.__dx[chaincode]
            nc[1] = cur[1] + self.__dy[chaincode]

            cur = nc

            coords.append(cur)

        return coords

    def corners(self):

        coords = self.__coords()

        corners = [self.start]

        cur = self.start

        for i in range(self.__len__() - 1):
            if self.cc[i] != self.cc[i+1]:
                corners.append(coords[i+1])

        corners.append(coords[-1])

        return corners

    def visualise(self, show=True, filename=None):

        coords = self.__coords()

        dis_arr, _, _, _, _ = self.__calculate()
        for i in range(1, len(dis_arr)):
            dis_arr[i] += dis_arr[i-1]

        
        x = [int(c[0]) for c in coords]
        y = [int(c[1]) for c in coords]
        max_x = max(x)
        max_y = max(y)
        x_ticks = [i for i in range(max_x + 1)]
        y_ticks = [i for i in range(max_y + 1)]

        dis_arr = [0, *dis_arr]

        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(dis_arr, self.elevation)

        plt.subplot(1, 2, 2)
        plt.xticks(x_ticks)
        plt.yticks(y_ticks)
        plt.plot(x, y)
        if show:
            plt.show()
        else:
            if filename:
                plt.savefig(filename+'.png')

    def __calculate(self):

        length = self.__len__()

        dis_arr = []
        time_arr = []
        f_slope = []
        f_road = []
        f_terrain = []

        for i in range(length):
            delta = self.elevation[i+1] - self.elevation[i]
            slope = delta / 10.0
            dis = sqrt(delta**2 + 1000**2) / 1000
            speed, f_r = self.__road_map[self.road[i]]

            time = dis * 3600 / speed

            f_s = None
            for ele in self.__slope:
                if slope <= ele[0]:
                    f_s = ele[1]
                    break

            dis_arr.append(dis)
            f_slope.append(f_s)
            f_road.append(f_r)
            f_terrain.append(self.__terrain_map[self.terrain[i]])
            time_arr.append(time)

        return dis_arr, f_slope, f_road, f_terrain, time_arr

    def co2(self):

        return json_track_calculator(self.dic)[0]

    def distance(self):
        return json_track_calculator(self.dic)[2]

    def time(self):

        return json_track_calculator(self.dic)[1]/3600



class Tracks():
    '''
    The definition of Tracks

    Parameters
    ----------
    x0:int
        x axis of start point
    y0:int
        y axis of start point
    x1:int
        x axis of end point
    y1:int
        y axis of end point
    n_tracks:int
        The number of tracks this object contains, default = 300
    
    Attributes
    ----------
    x0:int
        x axis of start point
    y0:int
        y axis of start point
    x1:int
        x axis of end point
    y1:int
        y axis of end point
    track_data:list
        Getting a list of information about n_tracks tracks, each element in it is a dictionary and has the format like {"cc":"11233344111","elevation":[17,18,19,24,23,22,21,16,11,12,13,14],"road":"llmmmmlrrrr","terrain":"pggppdddppg"}
    dic_tracks:dictionary
        A dictionary combining the index and the elements in track_data list
    '''
    def __init__(self,x0,y0,x1,y1,n_tracks=300):
        self.n_tracks=n_tracks
        self.x0=x0
        self.y0=y0
        self.x1=x1
        self.y1=y1
        try:
            requested_track_data = request_track(start=(self.x0,self.y0),end=(self.x1,self.y1),n_tracks=self.n_tracks).get("tracks")
            self.track_data=requested_track_data 
            dic_tracks={}
            for i,j in enumerate(self.track_data):
                dic_tracks.update({i:j})
            self.dic_tracks=dic_tracks
        except:
            print("Invalid. webapp returned an invalid set of tracks")
            sys.exit("Invalid. webapp returned an invalid set of tracks")



    def __len__(self):
        return self.n_tracks

    def __str__(self):
        return '<Tracks: {%d} from (%d,%d) to (%d,%d)>'%(self.n_tracks,self.x0,self.y0,self.x1,self.y1)

    def kmeans(self,clusters=3,iterations=10):
        points_data=[]
        for i in range(self.n_tracks):
            points_data+=[tuple(json_track_calculator(self.dic_tracks[i]))]
        
        m, alloc = cluster(points_data, iterations, clusters)
        dic_clusters={}
        for i in range(clusters):
            alloc_ps=[p for j, p in enumerate(points_data) if alloc[j] == i]
            dic_clusters.update({i:alloc_ps})
        return dic_clusters

    def greenest(self):
        greenest_data=sort_results(self.track_data)[0]
        cc=greenest_data.get('cc')
        road=greenest_data.get('road')
        terrain=greenest_data.get('terrain')
        elevation=greenest_data.get('elevation')
        return SingleTrack((self.x0,self.y0),cc,road,terrain,elevation)

    def fastest(self):
        fastest_data=sort_results(self.track_data)[1]
        cc=fastest_data.get('cc')
        road=fastest_data.get('road')
        terrain=fastest_data.get('terrain')
        elevation=fastest_data.get('elevation')
        return SingleTrack((self.x0,self.y0),cc,road,terrain,elevation)
        
    def shortest(self):
        shortest_data=sort_results(self.track_data)[2]
        cc=shortest_data.get('cc')
        road=shortest_data.get('road')
        terrain=shortest_data.get('terrain')
        elevation=shortest_data.get('elevation')
        return SingleTrack((self.x0,self.y0),cc,road,terrain,elevation)

        
    def get_track(self,x):
        track_get=self.dic_tracks.get(x)
        cc=track_get.get('cc')
        road=track_get.get('road')
        terrain=track_get.get('terrain')
        elevation=track_get.get('elevation')
        return SingleTrack((self.x0,self.y0),cc,road,terrain,elevation)

        

    @property
    def start(self):
        return (self.x0,self.y0)
    @property
    def end(self):
        return (self.x1,self.y1)
    @property
    def map_size(self):
        return [300,300]
    @property
    def date(self):
        return time.strftime

    


def query_tracks(start = (0,0), end = (299,299), min_steps_straight = 1, max_steps_straight = -99, n_tracks = 300,save=True):
    """ Generate an object related to the routes

    Parameters
    ----------
    start: tuple
        A start point in the map , such as (0,0) or (5,5) , between (0,0) to (300,300)
    end: tuple
        An end point in the map , such as (10,10) or (100,100), between (0,0) to (300,300)
    min_steps_straight: int
        define minimum step in a direction
    max_steps_straight: int
        define maximum step in a direction
    save: bool
        True for a saving file operation , False for not saving.

    Returns
    -------
    object
        An object with methods to get appropriate information based on the start and end points
        
    """
    returned_request=request_track(start=start,end=end,min_steps_straight=min_steps_straight,max_steps_straight=max_steps_straight,n_tracks=n_tracks)
    if save:
        str_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()).replace(' ','T').replace('-','').replace(':','')
        str_details='_'+str(n_tracks)+'_'+str(start[0])+'_'+str(start[1])+'_'+str(end[0])+'_'+str(end[1])+'.json'
        file_name='tracks_'+str_time+str_details
        with open(file_name,'w') as file_obj:
            json.dump(returned_request,file_obj)
    tracks=Tracks(start[0],start[1],end[0],end[1],n_tracks)
    return tracks
    #return json

def greentrack(start,end,verbose=False):
    """ Generate some lines of string to describe the greenest track

    Parameters
    ----------
    start: tuple
        A start point in the map , such as (0,0) or (5,5) , between (0,0) to (300,300)
    end: tuple
        An end point in the map , such as (10,10) or (100,100), between (0,0) to (300,300)
    verbose: bool
        True for description with more details , False for simple description.

    Returns
    -------
    string
        An appropriate description for the greenest track
        
    """
    if user_input_coordinate_check(start) and user_input_coordinate_check(end):
        tracks_object=Tracks(start[0],start[1],end[0],end[1])
    else:
        return "Invalid. Input parameters contain invalid characters"
    greenest_track=tracks_object.greenest()
    cc=greenest_track.cc
    co2=greenest_track.co2()
    time_spend=str(datetime.timedelta(hours=greenest_track.time()))
    output='Path : '+str(tuple(start))
    output_detail='Path : \n- Start from '+str(tuple(start))+'\n'
    location=list(start)
    dic_direction2={'12':'turn left at ','14':'turn right at ','13':'turn back at ','23':'turn left at ','21':'turn right at ','24':'turn back at ','34':'turn left at ','32':'turn right at ','31':'turn back at ','41':'turn left at ','43':'turn right at ','42':'turn back at '}
    dic_direction4={'1':'Go east for ','2':'Go north for ','3':'Go west for ','4':'Go south for '}
    m=0
    for i in range(1,len(cc)):
        if cc[i]!=cc[i-1]:           # find in which step the direction changes

            if cc[i-1]=='1':        # get the direction before it changes and calculate the corner points
                location[0]+=i-m 
            if cc[i-1]=='2':
                location[1]+=i-m
            if cc[i-1]=='3':
                location[0]-=i-m
            if cc[i-1]=='4':
                location[1]-=i-m
            
            output+=','+str(tuple(location))    # output with verbose=False
            key=cc[i-1]+cc[i]
            output_detail+='- '+dic_direction4.get(cc[i-1])+str(i-m)+' km, '+dic_direction2.get(key)+str(tuple(location))+'\n'    # output with verbose=True
            m=i
    last_index=len(cc)-1        # following codes just repeat the operation above, but pay attention to the index
    if cc[last_index]=='1':
        location[0]+=last_index-m+1
    if cc[last_index]=='2':
        location[1]+=last_index-m+1
    if cc[last_index]=='3':
        location[0]-=last_index-m+1
    if cc[last_index]=='4':
        location[1]-=last_index-m+1
    output+=','+str(tuple(location))
    output_detail+='- '+dic_direction4.get(cc[last_index])+str(last_index-m+1)+' km, \n- reach your estination at '+str(tuple(location))
    if verbose:
        return output_detail+'\n'+'CO2: '+str(co2)+' kg \nTime: '+time_spend
    else:
        return output+'\nCO2: '+str(co2)+' kg \nTime: '+time_spend


def load_tracksfile(path):
    
    if not os.path.exists(path):
        return 'json file does not exist'
    else:
        with open(path,'r')as fp:
            json_data = json.load(fp)
        if valid_schema_check(json_data):
            return json_data
        else:
            return 'The json file has wrong structure'