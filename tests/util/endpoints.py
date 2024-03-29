import requests
from datetime import datetime

from tests.secret import auth_token

def _post_auth_token(endpoint, prefix='genomics/', host="http://localhost:8000/"):
    url = f'{host}{prefix}{endpoint}'
    r = requests.post(url)
    return r

def _get_endpoint(endpoint, prefix='genomics/', host="http://localhost:8000/"):
    url = f'{host}{prefix}{endpoint}'
    if 'genomics' in prefix:
        headers = {"Authorization": f"Bearer {auth_token}"}
    else:
        headers = None
    r = requests.get(url, headers=headers)
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

def _api_request(url):
    res = _get_endpoint(url)
    result = res.json()
    return result

def _deep_compare(dict1, dict2):
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        if set(dict1.keys()) != set(dict2.keys()):
            print("IT'S DIFFERENT 0: " + str(set(dict1.keys())) + " | " + str(set(dict2.keys())) )
            return False
        for key in dict1.keys():
            if not _deep_compare(dict1[key], dict2[key]):
                print("IT'S DIFFERENT 1: " + str(dict1[key]) + " | " + str(dict2[key]))
                return False
        return True
    elif isinstance(dict1, list) and isinstance(dict2, list):
        for item1, item2 in zip(dict1, dict2):
            if not _deep_compare(item1, item2):
                print("IT'S DIFFERENT 3: " + str(item1) + " | " + str(item2))
                return False
        return True
    else:
        if dict1 is None or dict2 is None:
            return str(dict1) == str(dict2)
        elif isinstance(dict1, (float)) and isinstance(dict2, (float)):
            n_digits = 3
            str_num1 = "{:.{n}f}".format(dict1, n=n_digits)
            str_num2 = "{:.{n}f}".format(dict2, n=n_digits)
            if str_num1 == str_num2:
                return True
        elif isinstance(dict1, (int)) or isinstance(dict2, (int)):
            if abs(dict1 - dict2) < 3000:
                return True
            else:
                return False
        return dict1 == dict2
