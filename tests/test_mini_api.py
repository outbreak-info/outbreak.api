import pytest
import json

from tests.util import endpoints

def test_mini_api():
    with open('tests/mini_api/responses.json', 'r') as responses_json:
        responses = json.load(responses_json)
    for url, saved_response in responses.items():
        live_response = endpoints._get_endpoint(url, server='test.outbreak.info').json()
        assert saved_response == live_response
        


