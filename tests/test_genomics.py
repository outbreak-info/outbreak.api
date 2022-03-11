import pytest
import requests
from datetime import datetime
from urllib.parse import urljoin

from time import sleep, time
from .secret import auth_token
from deepdiff import DeepDiff

def _get_endpoint(endpoint, host=None):
    dev_host = 'https://dev.outbreak.info/'
    if host is None:
        host = 'https://api.outbreak.info/'

    prefix = 'genomics/'
    url = f'{host}{prefix}{endpoint}'
    headers = {"Authorization": f"Bearer {auth_token}"}
    times = []
    # test dev against prod
    #prod_r = requests.get(url, headers=headers)
    #dev_r  = requests.get(f'{dev_host}{prefix}{endpoint}', headers=headers)
    #diff = DeepDiff(prod_r.json(), dev_r.json(), significant_digits=6)
    #if diff:
    #    raise Exception(str(diff))

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

def test_seq_counts_1():
    url = 'sequence-count'
    result = _generic_api_test(url)
    _test_date(result, url)
    _test_total_count(result, url)

def test_seq_counts_2():
    url = 'sequence-count?location_id=USA&cumulative=true&subadmin=true'
    _generic_api_test(url)

def test_seq_counts_3():
    url = 'sequence-count?location_id=USA_US-CA'
    _generic_api_test(url)

def test_global_prev_1():
    url = 'global-prevalence'
    _generic_api_test(url)

def test_global_prev_2():
    url = 'global-prevalence?pangolin_lineage=b.1.1.7'
    _generic_api_test(url)

def test_global_prev_3():
    url = 'global-prevalence?pangolin_lineage=b.1.1.7&mutations=S:E484K'
    _generic_api_test(url)

def test_global_prev_4():
    url = 'global-prevalence?pangolin_lineage=b.1.1.7&cumulative=true'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)
    cum_global_prev = res_json.get('results').get('global_prevalence')
    assert cum_global_prev is not None, "cumulative global prevalence did not return a global_prevalence"

def test_prev_by_location_1():
    url = 'prevalence-by-location'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)

def test_prev_by_location_2():
    url = 'prevalence-by-location?pangolin_lineage=b.1.1.7&location_id=USA'
    res = _get_endpoint(url)
    res_json = res.json()
    assert res_json.get('results'), f"{url} no results"
    assert len(res_json['results']), f"{url} no results"
    assert res_json['results'].get('b.1.1.7'), f"{url} no b.1.1.7"
    assert len(res_json['results']['b.1.1.7']), f"{url} no results for b.1.1.7"

def test_mutation_details():
    url = 'mutation-details?mutations=S:E484K,S:N501Y'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)
    _test_results(res_json, url)

def test_mutations_by_lineage():
    url = 'mutations-by-lineage?mutations=S:E484K&location_id=USA'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)

def test_lineage_wildcard():
    url = 'lineage?name=b.1.*'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)

def test_heavy_query():
    url = 'prevalence-by-location?pangolin_lineage=B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3,AY.4.4,AY.4.5,AY.5,AY.5.1,AY.5.2,AY.5.3,AY.5.4,AY.6,AY.7,AY.7.1,AY.7.2,AY.8,AY.9,AY.9.1,AY.9.2,AY.9.2.1,AY.10,AY.11,AY.12,AY.13,AY.14,AY.15,AY.16,AY.16.1,AY.17,AY.18,AY.19,AY.20,AY.21,AY.22,AY.23,AY.23.1,AY.24,AY.25,AY.26,AY.27,AY.28,AY.29,AY.29.1,AY.30,AY.31,AY.32,AY.33,AY.34,AY.34.1,AY.35,AY.36,AY.37,AY.38,AY.39,AY.39.1,AY.39.1.1,AY.39.2,AY.40,AY.41,AY.42,AY.43,AY.44,AY.45,AY.46,AY.46.1,AY.46.2,AY.46.3,AY.46.4,AY.46.5,AY.46.6,AY.47,AY.48,AY.49,AY.50,AY.51,AY.52,AY.53,AY.54,AY.55,AY.56,AY.57,AY.58,AY.59,AY.60,AY.61,AY.62,AY.63,AY.64,AY.65,AY.66,AY.67,AY.68,AY.69,AY.70,AY.71,AY.72,AY.73,AY.74,AY.75,AY.75.1,AY.76,AY.77,AY.78,AY.79,AY.80,AY.81,AY.82,AY.83,AY.84,AY.85,AY.86,AY.87,AY.88,AY.89,AY.90,AY.91,AY.91.1,AY.92,AY.93,AY.94,AY.95,AY.96,AY.97,AY.98,AY.98.1,AY.99,AY.99.1,AY.99.2,AY.100,AY.101,AY.102,AY.103,AY.104,AY.105,AY.106,AY.107,AY.108,AY.109,AY.110,AY.111,AY.112,AY.113,AY.114,AY.115,AY.116,AY.116.1,AY.117'
    res = _get_endpoint(url)
    res_json = res.json()
    _test_success(res_json, url)
