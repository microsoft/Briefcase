import mlbriefcase
import pytest
import os
import json
import logging
import io

@pytest.fixture
def test_subdir():
    # change to tests/ subdir so we can resolve the yaml
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

@pytest.mark.skipif(os.environ.get('myserviceprincipal2') is None,
                    reason='Environment variable myserviceprincipal2 must be set to service principals secret')
def test_clarifai_moderation(test_subdir, caplog):
	# caplog.set_level(logging.DEBUG, logger='briefcase')

	ws = mlbriefcase.Briefcase()

	client = ws['moderation'].get_client()
	
	image = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../face1.jpg'), "rb").read() 

	result = client.public_models.moderation_model.predict_by_bytes(raw_bytes=image)

	assert result['status']['code'] == 10000
	assert list(filter(lambda x: x['name'] == 'explicit', result['outputs'][0]['data']['concepts']))[0]['value'] < 0.1