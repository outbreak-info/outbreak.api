from tests.util import endpoints


def test_status():
    url = "status"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    print(res_json)
    endpoints._test_success(res_json, url)
    assert res_json["success"] == True
    assert res_json["status"] == "green"


def test_metadata():
    url = "metadata"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    print(res_json)
    assert res_json["build_date"], f"{url} no results"
    assert res_json["biothing_type"] == "dataset"
    assert res_json["src"]["genomics_muts"]["upload_date"]["genomics_data_muts"], f"{url} no results"
    assert res_json["src"]["genomics_muts"]["upload_date"]["genomics_data_mutless"], f"{url} no results"


def test_seq_counts_1():
    url = "sequence-count"
    result = endpoints._generic_api_test(url)
    endpoints._test_date(result, url)
    endpoints._test_total_count(result, url)


def test_seq_counts_2():
    url = "sequence-count?location_id=USA&cumulative=true&subadmin=true"
    endpoints._generic_api_test(url)


def test_seq_counts_3():
    url = "sequence-count?location_id=USA_US-CA"
    endpoints._generic_api_test(url)


def test_global_prev_1():
    url = "global-prevalence"
    endpoints._generic_api_test(url)


def test_global_prev_2():
    url = "global-prevalence?pangolin_lineage=BA.2"
    endpoints._generic_api_test(url)


def test_global_prev_3():
    url = "global-prevalence?pangolin_lineage=BA.2"
    endpoints._generic_api_test(url)


def test_global_prev_3_1():
    url = "global-prevalence?pangolin_lineage=BA.2&mutations=S:D614G"
    endpoints._generic_api_test(url)


def test_global_prev_4():
    url = "global-prevalence?pangolin_lineage=BA.2&cumulative=true"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)
    cum_global_prev = res_json.get("results").get("global_prevalence")
    assert (
        cum_global_prev is not None
    ), "cumulative global prevalence did not return a global_prevalence"


def test_prev_by_location_1():
    url = "prevalence-by-location"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_prev_by_location_2():
    url = "prevalence-by-location?pangolin_lineage=BA.2&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert res_json.get("results"), f"{url} no results"
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"].get("BA.2"), f"{url} no BA.2"
    assert len(res_json["results"]["BA.2"]), f"{url} no results for BA.2"


def test_prev_by_location_2_1():
    url = "prevalence-by-location?pangolin_lineage=BA.2&mutations=S:D614G&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert res_json.get("results"), f"{url} no results"
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"].get("(BA.2) AND (S:D614G)"), f"{url} no BA.2"
    assert len(res_json["results"]["(BA.2) AND (S:D614G)"]), f"{url} no results for BA.2"


def test_mutation_details():
    url = "mutation-details?mutations=ORF1a:A735A,ORF1a:P3395H"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)
    endpoints._test_results(res_json, url)


def test_mutations_by_lineage_1():
    url = "mutations-by-lineage?mutations=S:E484K&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_mutations_by_lineage_2():
    url = "mutations-by-lineage?mutations=S:E484K%20AND%20S:S477N"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_wildcard():
    url = "lineage?name=b.1.*"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_by_country():
    url = "lineage-by-country"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"][0].get(
        "key"
    ), f"{url} no results"


def test_lineage_by_country_2():
    url = "lineage-by-country?pangolin_lineage=BA.2"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"][0].get(
        "key"
    ), f"{url} no results"


def test_location():
    url = "location?name=united*"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_location_lookup():
    url = "location-lookup?id=USA_US-CA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_mutations():
    url = "mutations?name=S:E484*"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_prevalence_by_location_all_lineages():
    url = "prevalence-by-location-all-lineages?location_id=CA&other_threshold=0.03&nday_threshold=5&ndays=60&other_exclude=p.1"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineages_mutations():
    url = "lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineages_mutations_2():
    url = "lineage-mutations?pangolin_lineage=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


# ################################################
# ############ V3
# ################################################


def test_seq_counts_1_v3():
    url = "v3/sequence-count"
    result = endpoints._generic_api_test(url)
    endpoints._test_date(result, url)
    endpoints._test_total_count(result, url)


def test_seq_counts_2_v3():
    url = "v3/sequence-count?location_id=USA&cumulative=true&subadmin=true"
    endpoints._generic_api_test(url)


def test_seq_counts_3_v3():
    url = "v3/sequence-count?location_id=USA_US-CA"
    endpoints._generic_api_test(url)


def test_global_prev_1_v3():
    url = "v3/global-prevalence"
    endpoints._generic_api_test(url)


def test_global_prev_2_v3():
    url = "v3/global-prevalence?pangolin_lineage=BA.2"
    endpoints._generic_api_test(url)


def test_global_prev_3_v3():
    url = "v3/global-prevalence?pangolin_lineage=BA.2"
    endpoints._generic_api_test(url)


def test_global_prev_3_1_v3():
    url = "v3/global-prevalence?pangolin_lineage=BA.2&mutations=S:D614G"
    endpoints._generic_api_test(url)


def test_global_prev_4_v3():
    url = "v3/global-prevalence?pangolin_lineage=BA.2&cumulative=true"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)
    cum_global_prev = res_json.get("results").get("global_prevalence")
    assert (
        cum_global_prev is not None
    ), "cumulative global prevalence did not return a global_prevalence"


def test_prev_by_location_1_v3():
    url = "v3/prevalence-by-location"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_prev_by_location_2_v3():
    url = "v3/prevalence-by-location?pangolin_lineage=BA.2&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert res_json.get("results"), f"{url} no results"
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"].get("BA.2"), f"{url} no BA.2"
    assert len(res_json["results"]["BA.2"]), f"{url} no results for BA.2"


def test_prev_by_location_2_1_v3():
    url = "v3/prevalence-by-location?pangolin_lineage=BA.2&mutations=S:D614G&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert res_json.get("results"), f"{url} no results"
    assert len(res_json["results"]), f"{url} no results"
    assert res_json["results"].get("(BA.2) AND (S:D614G)"), f"{url} no BA.2"
    assert len(res_json["results"]["(BA.2) AND (S:D614G)"]), f"{url} no results for BA.2"


def test_mutation_details_v3():
    url = "v3/mutation-details?mutations=ORF1a:A735A OR ORF1a:P3395H"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)
    endpoints._test_results(res_json, url)


def test_mutations_by_lineage_1_v3():
    url = "v3/mutations-by-lineage?mutations=S:E484K&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_mutations_by_lineage_2_v3():
    url = "v3/mutations-by-lineage?mutations=S:E484K%20AND%20S:S477N"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_by_country_v3():
    url = "v3/lineage-by-country"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_by_country_v3_2():
    url = "v3/lineage-by-country?pangolin_lineage=BA.2"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_wildcard_v3():
    url = "v3/lineage?name=b.1.*"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineages_mutations_v3():
    # Old schema
    # url = 'lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b'
    # New schema
    url = (
        "v3/lineage-mutations?lineages=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    )
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineages_mutations_v3_2():
    # Old schema
    # url = 'lineage-mutations?pangolin_lineage=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1'
    # New schema
    url = "v3/lineage-mutations?lineages=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


URLS_TESTED = [
    "prevalence-by-location-all-lineages?location_id=USA&other_threshold=0.03&nday_threshold=5&ndays=60&other_exclude=p.1",
    "mutations?name=S:E484*",
    "location-lookup?id=USA_US-CA",
    "location?name=united*",
    "prevalence-by-location?pangolin_lineage=B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3,AY.4.4,AY.4.5,AY.5,AY.5.1,AY.5.2,AY.5.3,AY.5.4,AY.6,AY.7,AY.7.1,AY.7.2,AY.8,AY.9,AY.9.1,AY.9.2,AY.9.2.1,AY.10,AY.11,AY.12,AY.13,AY.14,AY.15,AY.16,AY.16.1,AY.17,AY.18,AY.19,AY.20,AY.21,AY.22,AY.23,AY.23.1,AY.24,AY.25,AY.26,AY.27,AY.28,AY.29,AY.29.1,AY.30,AY.31,AY.32,AY.33,AY.34,AY.34.1,AY.35,AY.36,AY.37,AY.38,AY.39,AY.39.1,AY.39.1.1,AY.39.2,AY.40,AY.41,AY.42,AY.43,AY.44,AY.45,AY.46,AY.46.1,AY.46.2,AY.46.3,AY.46.4,AY.46.5,AY.46.6,AY.47,AY.48,AY.49,AY.50,AY.51,AY.52,AY.53,AY.54,AY.55,AY.56,AY.57,AY.58,AY.59,AY.60,AY.61,AY.62,AY.63,AY.64,AY.65,AY.66,AY.67,AY.68,AY.69,AY.70,AY.71,AY.72,AY.73,AY.74,AY.75,AY.75.1,AY.76,AY.77,AY.78,AY.79,AY.80,AY.81,AY.82,AY.83,AY.84,AY.85,AY.86,AY.87,AY.88,AY.89,AY.90,AY.91,AY.91.1,AY.92,AY.93,AY.94,AY.95,AY.96,AY.97,AY.98,AY.98.1,AY.99,AY.99.1,AY.99.2,AY.100,AY.101,AY.102,AY.103,AY.104,AY.105,AY.106,AY.107,AY.108,AY.109,AY.110,AY.111,AY.112,AY.113,AY.114,AY.115,AY.116,AY.116.1,AY.117",
    "lineage?name=b.1.*",
    "mutations-by-lineage?mutations=S:E484K&location_id=USA",
    "mutation-details?mutations=S:E484K,S:N501Y",
    "prevalence-by-location?pangolin_lineage=b.1.1.7&location_id=USA",
    "prevalence-by-location",
    "global-prevalence?pangolin_lineage=b.1.1.7&cumulative=true",
    "global-prevalence?pangolin_lineage=b.1.1.7&mutations=S:E484K",
    "global-prevalence?pangolin_lineage=b.1.1.7",
    "global-prevalence",
    "sequence-count?location_id=USA_US-CA",
    "sequence-count?location_id=USA&cumulative=true&subadmin=true",
    "sequence-count",
    "mutations?name=S:E484*",
    "prevalence-by-location-all-lineages?location_id=USA&other_threshold=0.03&nday_threshold=5&ndays=60&other_exclude=p.1",
    "lineage-mutations?lineages=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b",
    "lineage-mutations?lineages=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1",
]

ENDPOINTS_TESTED = [
    "prevalence-by-location-all-lineages"
    "location-lookup"
    "location"
    "prevalence-by-location"
    "lineage"
    "mutations-by-lineage"
    "mutation-details"
    "global-prevalence"
    "sequence-count"
    "lineage-mutations"
]

ENDPOINTS_NOT_TESTED = ["get-auth-token" "lineage-by-sub-admin-most-recent"]
