from tracknaliser import query_tracks
tracks=query_tracks((0,0),(5,5),save=False)
tracks.greenest().visualise(show=False,filename='my_track')