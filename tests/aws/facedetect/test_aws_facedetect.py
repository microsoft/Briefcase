import mlbriefcase
import pytest
import os
import json
import logging

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.mark.skipif(os.environ.get('myserviceprincipal2') is None,
                     reason='Environment variable myserviceprincipal2 must be set to service principals secret')
def test_aws_facedetect(test_subdir, caplog):
	# caplog.set_level(logging.DEBUG, logger='briefcase')

	ws = mlbriefcase.Briefcase()

	image = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../face1.jpg'), "rb").read() 

	reko_client = ws['faceaws1'].get_client()
	
	result = reko_client.detect_faces(Image={"Bytes": image})
	assert 'FaceDetails' in result