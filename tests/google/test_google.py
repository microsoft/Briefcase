import mlbriefcase
import pytest
import os
import json
import logging
import io
from google.cloud.language import enums
from google.cloud.language import types

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.mark.skipif(os.environ.get('myserviceprincipal2') is None,
                    reason='Environment variable myserviceprincipal2 must be set to service principals secret')
def test_google_facedetect(test_subdir, caplog):
	# caplog.set_level(logging.DEBUG, logger='briefcase')

	ws = mlbriefcase.Briefcase()

	image = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../face1.jpg'), "rb").read() 

	client = ws['face'].get_client()
	
	result = client.face_detection(io.BytesIO(image))

	assert result.face_annotations[0].joy_likelihood > 4

@pytest.mark.skipif(os.environ.get('myserviceprincipal2') is None,
                    reason='Environment variable myserviceprincipal2 must be set to service principals secret')
def test_google_language(test_subdir, caplog):
	# caplog.set_level(logging.DEBUG, logger='briefcase')

	ws = mlbriefcase.Briefcase()

	client = ws['language'].get_client()
	
	document = types.Document(content="The moon is visible from New York City.", language="en", type=enums.Document.Type.PLAIN_TEXT)
	result = client.analyze_entities(document)

	assert result.entities[0].name == 'moon'
	assert result.entities[0].type == enums.Entity.Type.LOCATION

	assert result.entities[1].name == 'New York City'
	assert result.entities[1].type == enums.Entity.Type.LOCATION
