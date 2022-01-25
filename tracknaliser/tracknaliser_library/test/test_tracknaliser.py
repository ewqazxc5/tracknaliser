import os
import pytest
import yaml
from tracknaliser_library.tracknaliser import greentrack
import pathlib
import json
from tracknaliser_library.class_definition import SingleTrack
from tracknaliser_library.class_definition import Tracks


TEST_DIR=pathlib.Path(__file__).parent
with open(TEST_DIR/'short_tracks.json','r') as fp:
        json_data = json.load(fp)

def read_fixture_invalids():
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures',
                           'invalid_samples.yaml')) as fixtures_file:
        fixtures = yaml.safe_load(fixtures_file)
    return fixtures

def read_fixture_valids():
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures',
                           'valid_samples.yaml')) as fixtures_file:
        fixtures = yaml.safe_load(fixtures_file)
    return fixtures

cc=json_data['tracks'][0]['cc']
road=json_data['tracks'][0]['road']
terrain=json_data['tracks'][0]['terrain']
elevation=json_data['tracks'][0]['elevation']
singletrack=SingleTrack([2,3],cc,road,terrain,elevation)

def test_singletrack_corners():
    assert singletrack.corners()==[[2, 3], [4, 3], [4, 4], [1, 4], [1, 2], [3, 2]]

def test_singletrack_co2():
    assert  singletrack.co2()==2.8484814847024316

def test_singletrack_distance():
    assert  singletrack.distance()==11.000185489326135

def test_singletrack_time():
    assert  singletrack.time()==0.2041692186152684

tracks=Tracks(2,3,4,2,-1)
def test_greenest():
    assert tracks.greenest().cc=='21144'
    assert tracks.greenest().road=='mmmlr'
    assert tracks.greenest().terrain=='ppggg'
    assert tracks.greenest().elevation==[17, 22, 23, 24, 19, 14]

def test_fastest():
    assert tracks.fastest().cc=='21144'
    assert tracks.fastest().road=='mmmlr'
    assert tracks.fastest().terrain=='ppggg'
    assert tracks.fastest().elevation==[17, 22, 23, 24, 19, 14]

def test_shortest():
    assert tracks.shortest().cc=='21144'
    assert tracks.shortest().road=='mmmlr'
    assert tracks.shortest().terrain=='ppggg'
    assert tracks.shortest().elevation==[17, 22, 23, 24, 19, 14]

def test_get():
    assert tracks.get_track(0).cc=='11233344111'
    assert tracks.get_track(0).road=='llmmmmlrrrr'
    assert tracks.get_track(0).terrain=='pggppdddppg'
    assert tracks.get_track(0).elevation==[17, 18, 19, 24, 23, 22, 21, 16, 11, 12, 13, 14]


@pytest.mark.parametrize("fixture", read_fixture_invalids())
def test_greentrack_invalids(fixture):
    answer = fixture.pop('answer')
    assert answer in greentrack(**fixture)

@pytest.mark.parametrize("fixture", read_fixture_valids())
def test_greentrack_valids(fixture):
    answer = fixture.pop('answer')
    assert answer in greentrack(**fixture)