import requests
from datetime import datetime

from tests.secret import auth_token

def _get_endpoint(endpoint, prefix='genomics/', host="https://test.outbreak.info/"):
    url = f'{host}{prefix}{endpoint}'
    if 'genomics' in prefix:
        headers = {"Authorization": f"Bearer {auth_token}"}
    else:
        headers = None

    r = requests.get(url, headers=headers)
    #raise Exception(f"{r.json()}")
    #
    #    raise Exception(f"{r.json()['results'][0]}")
    return r

def _test_success(res_json, url):
    assert res_json is not None, f"{url} did not return response"
    assert res_json.get('success'), f"{url} unsuccessful"
    assert res_json['success'] == True, f"{url} unsuccessful"

def _test_results(res_json, url):
    """
    tests that the api returns successfully with one or more results,
    returns the first result for convenience
    """
    assert res_json.get('results'), f"{url} no results"
    assert len(res_json['results']), f"{url} no results"
    return res_json['results'][0]

def _test_date(result, url):
    assert datetime.strptime(result['date'], '%Y-%m-%d'), f"{url} date not modified YYYY-MM-DD"

def _test_total_count(result, url):
    assert type(result['total_count']) is int, f"{url} total_count not an int"

def _generic_api_test(url):
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)
    result = _test_results(res_json, url)
    return result

