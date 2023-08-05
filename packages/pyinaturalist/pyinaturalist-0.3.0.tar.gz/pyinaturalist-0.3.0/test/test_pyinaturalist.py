"""
Tests for `pyinaturalist` module.
"""
import json
import os

import pytest
import requests_mock
from requests import HTTPError

from pyinaturalist.rest_api import get_access_token, get_all_observation_fields, \
    get_observation_fields, update_observation
from pyinaturalist.exceptions import AuthenticationError


def _sample_data_path(filename):
    return os.path.join(os.path.dirname(__file__), 'sample_data', filename)

def _load_sample_json(filename):
    return json.loads(open(_sample_data_path(filename)).read())

PAGE_1_JSON_RESPONSE = _load_sample_json('get_observation_fields_page1.json')
PAGE_2_JSON_RESPONSE = _load_sample_json('get_observation_fields_page2.json')

class TestPyinaturalist(object):

    @classmethod
    def setup_class(cls):
        pass

    @requests_mock.Mocker(kw='mock')
    def test_get_observation_fields(self, **kwargs):
        """ get_observation_fields() work as expected (basic use)"""
        mock = kwargs['mock']

        mock.get('https://www.inaturalist.org/observation_fields.json?q=sex&page=2',
                 json=PAGE_2_JSON_RESPONSE, status_code=200)

        obs_fields = get_observation_fields(search_query="sex", page=2)
        assert  obs_fields == PAGE_2_JSON_RESPONSE


    @requests_mock.Mocker(kw='mock')
    def test_get_all_observation_fields(self, **kwargs):
        """get_all_observation_fields() is able to paginate, accepts a search query and return correct results"""
        mock = kwargs['mock']

        mock.get('https://www.inaturalist.org/observation_fields.json?q=sex&page=1',
                 json=PAGE_1_JSON_RESPONSE, status_code=200)

        mock.get('https://www.inaturalist.org/observation_fields.json?q=sex&page=2',
                 json=PAGE_2_JSON_RESPONSE, status_code=200)

        page_3_json_response = []
        mock.get('https://www.inaturalist.org/observation_fields.json?q=sex&page=3',
                 json=page_3_json_response, status_code=200)


        all_fields = get_all_observation_fields(search_query="sex")
        assert all_fields == PAGE_1_JSON_RESPONSE + PAGE_2_JSON_RESPONSE

    @requests_mock.Mocker(kw='mock')
    def test_get_all_observation_fields_noparam(self, **kwargs):
        """get_all_observation_fields() can also be called without a search query without errors"""

        mock = kwargs['mock']
        mock.get('https://www.inaturalist.org/observation_fields.json?page=1',
                 json=[], status_code=200)

        get_all_observation_fields()

    @requests_mock.Mocker(kw='mock')
    def test_get_access_token_fail(self, **kwargs):
        """ If we provide incorrect credentials to get_access_token(), an AuthenticationError is raised"""

        mock = kwargs['mock']
        rejection_json = {'error': 'invalid_client', 'error_description': 'Client authentication failed due to '
                                                                          'unknown client, no client authentication '
                                                                          'included, or unsupported authentication '
                                                                          'method.'}
        mock.post('https://www.inaturalist.org/oauth/token', json=rejection_json, status_code=401)

        with pytest.raises(AuthenticationError):
            get_access_token('username', 'password', 'app_id', 'app_secret')

    @requests_mock.Mocker(kw='mock')
    def test_get_access_token(self, **kwargs):
        """ Test a successful call to get_access_token() """

        mock = kwargs['mock']
        accepted_json = {'access_token': '604e5df329b98eecd22bb0a84f88b68a075a023ac437f2317b02f3a9ba414a08',
                         'token_type': 'Bearer', 'scope': 'write', 'created_at': 1539352135}
        mock.post('https://www.inaturalist.org/oauth/token', json=accepted_json, status_code=200)

        token = get_access_token('valid_username', 'valid_password', 'valid_app_id', 'valid_app_secret')

        assert token == '604e5df329b98eecd22bb0a84f88b68a075a023ac437f2317b02f3a9ba414a08'

    @requests_mock.Mocker(kw='mock')
    def test_update_observation(self, **kwargs):
        mock = kwargs['mock']
        mock.put('https://www.inaturalist.org/observations/17932425.json',
                 json=_load_sample_json('update_observation_result.json'),
                 status_code=200)

        p = {'ignore_photos': 1,
             'observation': {'description': 'updated description v2 !'}}
        r = update_observation(observation_id=17932425, params=p, access_token='valid token')

        # If all goes well we got a single element representing the updated observation, enclosed in a list.
        assert len(r) == 1
        assert r[0]['id'] == 17932425
        assert r[0]['description'] == 'updated description v2 !'

    @requests_mock.Mocker(kw='mock')
    def test_update_nonexistent_observation(self, **kwargs):
        """When we try to update a non-existent observation, iNat returns an error 410 with "obs does not longer exists". """
        mock = kwargs['mock']
        mock.put('https://www.inaturalist.org/observations/999999999.json',
                 json={"error":"Cette observation n’existe plus."},
                 status_code=410)

        p = {'ignore_photos': 1,
             'observation': {'description': 'updated description v2 !'}}

        with pytest.raises(HTTPError) as excinfo:
            update_observation(observation_id=999999999, params=p, access_token='valid token')
        assert excinfo.value.response.status_code == 410
        assert excinfo.value.response.json() == {"error":"Cette observation n’existe plus."}

    @requests_mock.Mocker(kw='mock')
    def test_update_observation_not_mine(self, **kwargs):
        """When we try to update the obs of another user, iNat returns an error 410 with "obs does not longer exists"."""
        mock = kwargs['mock']
        mock.put('https://www.inaturalist.org/observations/16227955.json',
                 json={"error": "Cette observation n’existe plus."},
                 status_code=410)

        p = {'ignore_photos': 1,
             'observation': {'description': 'updated description v2 !'}}

        with pytest.raises(HTTPError) as excinfo:
            update_observation(observation_id=16227955, params=p, access_token='valid token for another user')
        assert excinfo.value.response.status_code == 410
        assert excinfo.value.response.json() == {"error": "Cette observation n’existe plus."}

    @classmethod
    def teardown_class(cls):
        pass
