from tests.util import endpoints

# # ################################################
# # ############ Comparison Tests: v2 vs v3
# # ################################################


def test_global_prev_1():
    url = "global-prevalence"
    result = endpoints._generic_api_test(url)

    url = "v3/global-prevalence"
    result_v3 = endpoints._generic_api_test(url)

    assert endpoints._deep_compare(result, result_v3) == True


def test_global_prev_2():
    url = "global-prevalence?pangolin_lineage=BA.2"
    result = endpoints._generic_api_test(url)

    url = "v3/global-prevalence?pangolin_lineage=BA.2"
    result_v3 = endpoints._generic_api_test(url)

    assert endpoints._deep_compare(result, result_v3) == True


def test_global_prev_3():
    url = "global-prevalence?pangolin_lineage=BA.2"
    result = endpoints._generic_api_test(url)

    url = "v3/global-prevalence?pangolin_lineage=BA.2"
    result_v3 = endpoints._generic_api_test(url)

    assert endpoints._deep_compare(result, result_v3) == True


def test_global_prev_3_1():
    url = "global-prevalence?pangolin_lineage=BA.2&mutations=S:D614G"
    result = endpoints._generic_api_test(url)

    url = "v3/global-prevalence?pangolin_lineage=BA.2&mutations=S:D614G"
    result_v3 = endpoints._generic_api_test(url)

    assert endpoints._deep_compare(result, result_v3) == True


def test_global_prev_4():
    url = "global-prevalence?pangolin_lineage=BA.2&cumulative=true"
    result = endpoints._api_request(url)

    url = "v3/global-prevalence?pangolin_lineage=BA.2&cumulative=true"
    result_v3 = endpoints._api_request(url)

    assert endpoints._deep_compare(result, result_v3) == True


def test_prev_by_location_1():
    url = "prevalence-by-location"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3)


def test_prev_by_location_2():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = "prevalence-by-location?pangolin_lineage=BA.2"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/prevalence-by-location?pangolin_lineage=BA.2"
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"])


def test_prev_by_location_2_with_location_id():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = "prevalence-by-location?pangolin_lineage=BA.2&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"])


def test_prev_by_location_2_1():
    # WARNING FIXED: The result key was changed from 'BA.2' to '(BA.2)'
    # The result key value changed:
    #   from 'BA.2'
    #   to '(BA.2)'

    url = "prevalence-by-location?pangolin_lineage=BA.2&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/prevalence-by-location?pangolin_lineage=BA.2&location_id=USA"
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"])


def test_prev_by_location_2_2_with_mutations():
    url = "prevalence-by-location?pangolin_lineage=BA.2&mutations=S:D614G&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(
        result["results"]["(BA.2) AND (S:D614G)"], result_v3["results"]["(BA.2) AND (S:D614G)"]
    )


def test_prev_by_location_2_2_with_mutations_1():
    url = (
        "prevalence-by-location?pangolin_lineage=BA.2&mutations=S:D614G AND S:R21T&location_id=USA"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(
        result["results"]["(BA.2) AND (S:D614G AND S:R21T)"],
        result_v3["results"]["(BA.2) AND (S:D614G AND S:R21T)"],
    )


def test_prev_by_location_2_3():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = "prevalence-by-location?pangolin_lineage=BA.1,BA.2&min_date=2020-07-01&max_date=2020-07-02&cumulative=true"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["BA.1"], result_v3["results"]["BA.1"]) == True
    )
    assert (
        endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"]) == True
    )


def test_prev_by_location_2_4():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = (
        "prevalence-by-location?pangolin_lineage=BA.1,BA.2&min_date=2020-07-01&max_date=2020-07-02"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["BA.1"], result_v3["results"]["BA.1"]) == True
    )
    assert (
        endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"]) == True
    )


def test_prev_by_location_2_5():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = (
        "prevalence-by-location?cumulative=true&pangolin_lineage=XBB.1.16,FU.1,FU.2,FU.2.1,FU.3,FU.3.1,FU.4,FU.5,GY.1,GY.2,GY.2.1,GY.3,GY.4,GY.5,GY.6,GY.7,GY.8,HF.1,HF.1.1,HF.1.2,JF.1,JF.2,XBB.1.16.1,XBB.1.16.2,XBB.1.16.3,XBB.1.16.4,XBB.1.16.5,XBB.1.16.6,XBB.1.16.7,XBB.1.16.8,XBB.1.16.9,XBB.1.16.10,XBB.1.16.11,XBB.1.16.12,XBB.1.16.13,XBB.1.16.14,XBB.1.16.15,XBB.1.16.16,XBB.1.16.17,XBB.1.16.18,XBB.1.16.19,XBB.1.16.20,XBB.1.16.21,XBB.1.16.22,XBB.1.16.23,XBB.1.16.24"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["XBB.1.16"], result_v3["results"]["XBB.1.16"]) == True
    )
    assert (
        endpoints._deep_compare(result["results"]["FU.1"], result_v3["results"]["FU.1"]) == True
    )


def test_prev_by_location_2_4_1():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = (
        "prevalence-by-location?pangolin_lineage=BA.1,BA.2&min_date=2020-07-01&max_date=2022-07-02"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["BA.1"], result_v3["results"]["BA.1"]) == True
    )
    assert (
        endpoints._deep_compare(result["results"]["BA.2"], result_v3["results"]["BA.2"]) == True
    )


def test_prev_by_location_2_4_22():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    url = (
        # "prevalence-by-location?pangolin_lineage=XBB.1.16%20OR%20FU.1%20OR%20FU.2%20OR%20FU.2.1%20OR%20FU.3%20OR%20FU.3.1%20OR%20FU.4%20OR%20FU.5%20OR%20GY.1%20OR%20GY.2%20OR%20GY.2.1%20OR%20GY.3%20OR%20GY.4%20OR%20GY.5%20OR%20GY.6%20OR%20GY.7%20OR%20GY.8%20OR%20HF.1%20OR%20HF.1.1%20OR%20HF.1.2%20OR%20JF.1%20OR%20JF.2%20OR%20XBB.1.16.1%20OR%20XBB.1.16.2%20OR%20XBB.1.16.3%20OR%20XBB.1.16.4%20OR%20XBB.1.16.5%20OR%20XBB.1.16.6%20OR%20XBB.1.16.7%20OR%20XBB.1.16.8%20OR%20XBB.1.16.9%20OR%20XBB.1.16.10%20OR%20XBB.1.16.11%20OR%20XBB.1.16.12%20OR%20XBB.1.16.13%20OR%20XBB.1.16.14%20OR%20XBB.1.16.15%20OR%20XBB.1.16.16%20OR%20XBB.1.16.17%20OR%20XBB.1.16.18%20OR%20XBB.1.16.19%20OR%20XBB.1.16.20%20OR%20XBB.1.16.21%20OR%20XBB.1.16.22%20OR%20XBB.1.16.23%20OR%20XBB.1.16.24&location_id=USA_US-CA&cumulative=true"
        "prevalence-by-location?pangolin_lineage=XBB.1.16%20OR%20FU.1&location_id=USA_US-CA&cumulative=true"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["XBB.1.16 OR FU.1"], result_v3["results"]["XBB.1.16 OR FU.1"]) == True
    )


def test_prev_by_location_2_4_2():
    url = "prevalence-by-location?cumulative=true&pangolin_lineage=BA.2.86&mutations=s:n764k"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_prev_by_location_2_4_3():
    # WARNING: This is a new functionallity.
    # Now it's possible to use logic operators.
    # Ex: BA.1 OR BA.2
    url = "prevalence-by-location?pangolin_lineage=BA.1 OR BA.2&min_date=2020-07-01&max_date=2022-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()
    endpoints._test_success(result_v3, url)

    assert result_v3["results"]["BA.1 OR BA.2"] is not None


def test_prev_by_location_2_4_4():
    # WARNING: This is a new functionallity.
    # Now it's possible to use a list of logic operators.
    # Ex: BA.1 OR BA.2,AY.1 OR AY.2
    url = "prevalence-by-location?pangolin_lineage=BA.1 OR BA.2,AY.1 OR AY.2&min_date=2020-07-01&max_date=2022-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()
    endpoints._test_success(result_v3, url)

    assert result_v3["results"]["BA.1 OR BA.2"] is not None
    assert result_v3["results"]["AY.1 OR AY.2"] is not None


def test_prev_by_location_2_4_5():
    # WARNING: This is a new functionallity.
    # Now it's possible to use a list of logic operators.
    # Ex: BA.1 OR BA.2,AY.1 OR AY.2
    url = "prevalence-by-location?pangolin_lineage=BA.1 OR BA.2,AY.1 OR AY.2&mutations=s:n764k OR ORF1a:A735A&min_date=2020-07-01&max_date=2022-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()
    endpoints._test_success(result_v3, url)

    assert result_v3["results"]["(BA.1 OR BA.2) AND (s:n764k OR ORF1a:A735A)"] is not None
    assert result_v3["results"]["(AY.1 OR AY.2) AND (s:n764k OR ORF1a:A735A)"] is not None


def test_prev_by_location_q_3():
    # WARNING: This is a new functionallity.
    # Now it's possible to create logical query
    # Ex: lineages:AY.1
    url = "prevalence-by-location?pangolin_lineage=AY.1&min_date=2020-07-01&max_date=2023-07-02"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "prevalence-by-location?q=lineages:AY.1&min_date=2020-07-01&max_date=2023-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["AY.1"], result_v3["results"]["lineages:AY.1"])
        == True
    )


def test_prev_by_location_q_3_with_mutations():
    # WARNING: This is a new functionallity.
    # Now it's possible to create logical query
    # Ex: lineages:AY.1 AND mutations:S:E484K
    url = "prevalence-by-location?pangolin_lineage=AY.1&mutations=S:E484K&min_date=2020-07-01&max_date=2023-07-02"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "prevalence-by-location?q=lineages:AY.1 AND mutations:S:E484K&min_date=2020-07-01&max_date=2023-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(
            result["results"]["(AY.1) AND (S:E484K)"],
            result_v3["results"]["lineages:AY.1 AND mutations:S:E484K"],
        )
        == True
    )


def test_prev_by_location_q_3_1():
    # WARNING: This is a new functionallity.
    # Now it's possible to create a list of logical queries
    # Ex: lineages:AY.1|lineages:AY.2
    url = (
        "prevalence-by-location?pangolin_lineage=AY.1,AY.2&min_date=2020-07-01&max_date=2023-07-02"
    )
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "prevalence-by-location?q=lineages:AY.1|lineages:AY.2&min_date=2020-07-01&max_date=2023-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["AY.1"], result_v3["results"]["lineages:AY.1"])
        == True
    )
    assert (
        endpoints._deep_compare(result["results"]["AY.2"], result_v3["results"]["lineages:AY.2"])
        == True
    )


def test_prev_by_location_q_3_1_with_mutations():
    # WARNING: This is a new functionallity.
    # Now it's possible to create a list of logical queries
    # Ex: lineages:AY.1|lineages:AY.2
    url = "prevalence-by-location?pangolin_lineage=AY.1,AY.2&mutations=S:E484K&min_date=2020-07-01&max_date=2023-07-02"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "prevalence-by-location?q=lineages:AY.1 AND mutations:S:E484K|lineages:AY.2 AND mutations:S:E484K&min_date=2020-07-01&max_date=2023-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(
            result["results"]["(AY.1) AND (S:E484K)"],
            result_v3["results"]["lineages:AY.1 AND mutations:S:E484K"],
        )
        == True
    )
    assert (
        endpoints._deep_compare(
            result["results"]["(AY.2) AND (S:E484K)"],
            result_v3["results"]["lineages:AY.2 AND mutations:S:E484K"],
        )
        == True
    )


def test_prev_by_location_q_3_2():
    # WARNING: This is a new functionallity.
    # Now it's possible to use a list of logic operators.
    # Ex: BA.1 OR BA.2,AY.1 OR AY.2
    # url = 'prevalence-by-location?q=lineages: BA.1 OR BA.2,lineages: AY.1 OR AY.2 AND mutations: s:n764k&min_date=2020-07-01&max_date=2022-07-02'
    url = "prevalence-by-location?q=lineages: AY.1 OR AY.2 AND mutations: s:n764k&min_date=2020-07-01&max_date=2020-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()
    endpoints._test_success(result_v3, url)

    assert result_v3["results"]["lineages: AY.1 OR AY.2 AND mutations: s:n764k"] is not None
    # assert result_v3['results']['(AY.1 OR AY.2) AND (s:n764k OR ORF1a:A735A)'] is not None


def test_heavy_query():
    # WARNING: The key in the result was changed adding parenthesis.
    # Ex: from 'BA.1' to '(BA.1)'
    # pangolin_lineages = 'B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3,AY.4.4,AY.4.5,AY.5,AY.5.1,AY.5.2,AY.5.3,AY.5.4,AY.6,AY.7,AY.7.1,AY.7.2,AY.8,AY.9,AY.9.1,AY.9.2,AY.9.2.1,AY.10,AY.11,AY.12,AY.13,AY.14,AY.15,AY.16,AY.16.1,AY.17,AY.18,AY.19,AY.20,AY.21,AY.22,AY.23,AY.23.1,AY.24,AY.25,AY.26,AY.27,AY.28,AY.29,AY.29.1,AY.30,AY.31,AY.32,AY.33,AY.34,AY.34.1,AY.35,AY.36,AY.37,AY.38,AY.39,AY.39.1,AY.39.1.1,AY.39.2,AY.40,AY.41,AY.42,AY.43,AY.44,AY.45,AY.46,AY.46.1,AY.46.2,AY.46.3,AY.46.4,AY.46.5,AY.46.6,AY.47,AY.48,AY.49,AY.50,AY.51,AY.52,AY.53,AY.54,AY.55,AY.56,AY.57,AY.58,AY.59,AY.60,AY.61,AY.62,AY.63,AY.64,AY.65,AY.66,AY.67,AY.68,AY.69,AY.70,AY.71,AY.72,AY.73,AY.74,AY.75,AY.75.1,AY.76,AY.77,AY.78,AY.79,AY.80,AY.81,AY.82,AY.83,AY.84,AY.85,AY.86,AY.87,AY.88,AY.89,AY.90,AY.91,AY.91.1,AY.92,AY.93,AY.94,AY.95,AY.96,AY.97,AY.98,AY.98.1,AY.99,AY.99.1,AY.99.2,AY.100,AY.101,AY.102,AY.103,AY.104,AY.105,AY.106,AY.107,AY.108,AY.109,AY.110,AY.111,AY.112,AY.113,AY.114,AY.115,AY.116,AY.116.1,AY.117'
    pangolin_lineages = "B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4"
    url = "prevalence-by-location?pangolin_lineage=" + pangolin_lineages
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    for lineage in pangolin_lineages.split(","):
        assert (
            endpoints._deep_compare(
                result["results"][lineage], result_v3["results"][lineage]
            )
            == True
        )


def test_mutation_details():
    # WARNING: v3 has two more fields in the result
    #       "id": "14749560_ORF1a:P3395H_CAC_10448",
    #       "is_synyonymous": False,
    # Remove these fields from datasource. For now it was removed
    # in the handler

    url = "mutation-details?mutations=ORF1a:A735A,ORF1a:P3395H"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutation-details?mutations=ORF1a:A735A,ORF1a:P3395H"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True

def test_mutation_details_2():
    # WARNING: v3 has two more fields in the result
    #       "id": "14749560_ORF1a:P3395H_CAC_10448",
    #       "is_synyonymous": False,
    # Remove these fields from datasource. For now it was removed
    # in the handler

    url = "mutation-details?mutations=ORF1a:A735A,ORF1a:P3395H"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutation-details?mutations=ORF1a:A735A OR ORF1a:P3395H"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_mutations_by_lineage_1():
    url = "mutations-by-lineage?mutations=S:E484K&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_mutations_by_lineage_2_with_and():
    # WARNING: Changed the way of mutations parameter is used
    # In the v2 version there are the rules below related to the mutation querystring param:
    # - the "," character is considered as "AND" operand
    # --- Ex: "mutation=S:E484K,S:S477N" will be used as "S:E484K AND S:S477N"
    # --- Ex: when "mutation=S:E484K AND S:S477N" will be created one ES query for each mutation"
    # - the "AND" operand is considered to split in many queries
    # In v3 version the logic was inverted when considering "," and "AND" operands.
    url = "mutations-by-lineage?mutations=S:E484K,S:S477N&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutations-by-lineage?mutations=S:E484K AND S:S477N&location_id=USA"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(
            result["results"]["S:E484K,S:S477N"], result_v3["results"]["S:E484K AND S:S477N"]
        )
        == True
    )


# def test_mutations_by_lineage_2_with_lineage():
#     # WARNING: Getting error when use "pangolin_lineage" param in the v2 version
#     url = 'mutations-by-lineage?mutations=S:E484K,S:S477N&pangolin_lineage=AY.1&location_id=USA'
#     result = endpoints._get_endpoint(url)
#     result = result.json()
#     print("### result")
#     print(result)

#     url = 'mutations-by-lineage?mutations=S:E484K AND S:S477N&pangolin_lineage=AY.1&location_id=USA'
#     url = 'v3/' + url
#     result_v3 = endpoints._get_endpoint(url)
#     result_v3 = result_v3.json()
#     print("### result_v3")
#     print(result_v3)

#     assert endpoints._deep_compare(result['results']['S:E484K,S:S477N'], result_v3['results']['S:E484K AND S:S477N']) == True


def test_mutations_by_lineage_2_with_comma():
    # WARNING: Changed the way of mutations parameter is used
    # In the v2 version there are the rules below related to the mutation querystring param:
    # - the "," character is considered as "AND" operand
    # --- Ex: "mutation=S:E484K,S:S477N" will be used as "S:E484K AND S:S477N"
    # --- Ex: when "mutation=S:E484K AND S:S477N" will be created one ES query for each mutation"
    # - the "AND" operand is considered to split in many queries
    # In v3 version the logic was inverted when considering "," and "AND" operands.
    url = "mutations-by-lineage?mutations=S:E484K AND S:S477N&location_id=USA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutations-by-lineage?mutations=S:E484K,S:S477N&location_id=USA"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["S:E484K"], result_v3["results"]["S:E484K"])
        == True
    )
    assert (
        endpoints._deep_compare(result["results"]["S:S477N"], result_v3["results"]["S:S477N"])
        == True
    )


def test_mutations_by_lineage_2_1_with_comma_lineage_and_date_filter():
    # WARNING: Changed the way of mutations parameter is used
    # In the v2 version there are the rules below related to the mutation querystring param:
    # - the "," character is considered as "AND" operand
    # --- Ex: "mutation=S:E484K,S:S477N" will be used as "S:E484K AND S:S477N"
    # --- Ex: when "mutation=S:E484K AND S:S477N" will be created one ES query for each mutation"
    # - the "AND" operand is considered to split in many queries
    # In v3 version the logic was inverted when considering "," and "AND" operands.

    url = "mutations-by-lineage?mutations=S:E484K AND S:S477N&pangolin_lineage=BA.2&min_date=2020-07-01&max_date=2020-07-02"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutations-by-lineage?mutations=S:E484K,S:S477N&pangolin_lineage=BA.2&min_date=2020-07-01&max_date=2020-07-02"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["S:E484K"], result_v3["results"]["S:E484K"])
        == True
    )
    assert (
        endpoints._deep_compare(result["results"]["S:S477N"], result_v3["results"]["S:S477N"])
        == True
    )


def test_mutations_by_lineage_2_2_with_comma_lineage_and_date_filter():
    # WARNING: Changed the way of mutations parameter is used
    # In the v2 version there are the rules below related to the mutation querystring param:
    # - the "," character is considered as "AND" operand
    # --- Ex: "mutation=S:E484K,S:S477N" will be used as "S:E484K AND S:S477N"
    # --- Ex: when "mutation=S:E484K AND S:S477N" will be created one ES query for each mutation"
    # - the "AND" operand is considered to split in many queries
    # In v3 version the logic was inverted when considering "," and "AND" operands.

    url = "mutations-by-lineage?mutations=S:E484K%20AND%20ORF1a:DEL3675/3677&frequency=0.5"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "mutations-by-lineage?mutations=S:E484K,ORF1a:DEL3675/3677&frequency=0.5"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert (
        endpoints._deep_compare(result["results"]["S:E484K"], result_v3["results"]["S:E484K"])
        == True
    )
    assert (
        endpoints._deep_compare(result["results"]["S:S477N"], result_v3["results"]["S:S477N"])
        == True
    )


def test_mutations_by_lineage_q():
    url = "mutations-by-lineage?mutations=S:E484K AND S:S477N&pangolin_lineage=BA.2"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    url = "mutations-by-lineage?q=mutations:(S:E484K AND S:S477N) AND pangolin_lineage:BA.2"
    url = "v3/" + url
    result_v3_q = endpoints._get_endpoint(url)
    result_v3_q = result_v3_q.json()

    assert (
        endpoints._deep_compare(result_v3["results"]["S:E484K AND S:S477N"], result_v3_q["results"]["mutations:(S:E484K AND S:S477N) AND pangolin_lineage:BA.2"])
        == True
    )


def test_mutations_by_lineage_q_with_location():
    url = "mutations-by-lineage?mutations=S:E484K AND S:S477N&pangolin_lineage=BA.2&location_id=USA"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    url = "mutations-by-lineage?q=mutations:(S:E484K AND S:S477N) AND pangolin_lineage:BA.2&location_id=USA"
    url = "v3/" + url
    result_v3_q = endpoints._get_endpoint(url)
    result_v3_q = result_v3_q.json()

    assert (
        endpoints._deep_compare(result_v3["results"]["S:E484K AND S:S477N"], result_v3_q["results"]["mutations:(S:E484K AND S:S477N) AND pangolin_lineage:BA.2"])
        == True
    )


def test_lineage_wildcard():
    url = "lineage?name=b.1.*"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_lineage_by_country():
    url = "lineage-by-country"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    data_result = result["aggregations"]["prevalence"]["country"]["buckets"]
    data_result_v3 = result_v3["results"]
    assert endpoints._deep_compare(data_result, data_result_v3) == True


def test_lineage_by_country_2():
    url = "lineage-by-country?pangolin_lineage=BA.2"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    data_result = result["aggregations"]["prevalence"]["country"]["buckets"]
    data_result_v3 = result_v3["results"]
    assert endpoints._deep_compare(data_result, data_result_v3) == True


def test_mutations():
    url = "mutations?name=S:E484*"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_lineage_mutations_a():
    # WARNING: LITTLE DIFFERENCE!
    # Changed from string "None" to None
    url = "lineage-mutations?pangolin_lineage=BA.2"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?pangolin_lineage=BA.2"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    url = "lineage-mutations?lineages=BA.2"
    url = "v3/" + url
    result_v3_new = endpoints._get_endpoint(url)
    result_v3_new = result_v3_new.json()

    mutation = next(
        (d for d in result["results"]["BA.2"] if d.get("mutation") == "orf6:d61l"), None
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["BA.2"] if d.get("mutation") == "orf6:d61l"), None
    )
    mutation_v3_new = next(
        (d for d in result_v3_new["results"]["BA.2"] if d.get("mutation") == "orf6:d61l"), None
    )
    assert endpoints._deep_compare(mutation, mutation_v3) == True
    assert endpoints._deep_compare(mutation, mutation_v3_new) == True


def test_lineage_mutations_1():
    # WARNING: LITTLE DIFFERENCE!
    # Changed from string "None" to None
    url = "lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?lineages=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    mutation = next(
        (d for d in result["results"]["BA.2"] if d.get("mutation") == "orf6:d61l"), None
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["BA.2"] if d.get("mutation") == "orf6:d61l"), None
    )
    assert endpoints._deep_compare(mutation, mutation_v3) == True


def test_lineage_mutations_2():
    url = "lineage-mutations?pangolin_lineage=B.1.427%20OR%20B.1.429&frequency=1"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?lineages=B.1.427%20OR%20B.1.429&frequency=1"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    mutation = next(
        (d for d in result["results"]["B.1.427 OR B.1.429"] if d.get("mutation") == "orf6:d61l"),
        None,
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["B.1.427 OR B.1.429"] if d.get("mutation") == "orf6:d61l"),
        None,
    )
    assert endpoints._deep_compare(mutation, mutation_v3) == True


def test_lineage_mutations_with_q():
    url = "lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?q=lineages:BA.2 AND mutations:S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    mutation = next(
        (d for d in result["results"]["BA.2"] if d.get("mutation") == "s:l24s"),
        None,
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["lineages:BA.2 AND mutations:S:D614G"] if d.get("mutation") == "s:l24s"),
        None,
    )
    mutation_v3["lineage"] = "BA.2"

    assert mutation != None
    assert mutation_v3 != None
    assert endpoints._deep_compare(mutation, mutation_v3) == True


def test_lineage_mutations_with_q_1():
    # WARNING: LITTLE DIFFERENCE!
    # Changed from string "None" to None
    url = "lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?q=lineages:BA.2 AND mutations:S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    mutation = next(
        (d for d in result["results"]["BA.2"] if d.get("mutation") == "s:l24s"),
        None,
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["lineages:BA.2 AND mutations:S:D614G"] if d.get("mutation") == "s:l24s"),
        None,
    )
    mutation_v3["lineage"] = "BA.2"

    assert mutation != None
    assert mutation_v3 != None
    assert endpoints._deep_compare(mutation, mutation_v3) == True


def test_lineage_mutations_with_q_2():
    url = "lineage-mutations?pangolin_lineage=B.1.427%20OR%20B.1.429"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "lineage-mutations?q=lineages:(B.1.427 OR B.1.429)"
    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    mutation = next(
        (d for d in result["results"]["B.1.427 OR B.1.429"] if d.get("mutation") == "s:d614g"),
        None,
    )
    mutation_v3 = next(
        (d for d in result_v3["results"]["lineages:(B.1.427 OR B.1.429)"] if d.get("mutation") == "s:d614g"),
        None,
    )
    mutation_v3["lineage"] = "B.1.427 OR B.1.429"

    assert mutation != None
    assert mutation_v3 != None
    assert endpoints._deep_compare(mutation, mutation_v3) == True


def test_seq_counts_1():
    url = "sequence-count"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_seq_counts_2_1():
    url = "sequence-count?location_id=USA&cumulative=true&subadmin=true"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_seq_counts_2_2():
    url = "sequence-count?location_id=USA_US-CA"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_seq_counts_2_3():
    url = "sequence-count?cumulative=true"
    result = endpoints._get_endpoint(url)
    result = result.json()

    url = "v3/" + url
    result_v3 = endpoints._get_endpoint(url)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v3) == True


def test_cumulative_prevalence_by_location_1():
    url = "lineage-by-sub-admin-most-recent?pangolin_lineage=XBB.1.16%20OR%20FU.1%20OR%20FU.2%20OR%20FU.2.1%20OR%20FU.3%20OR%20FU.3.1%20OR%20FU.4%20OR%20FU.5%20OR%20GY.1%20OR%20GY.2%20OR%20GY.2.1%20OR%20GY.3%20OR%20GY.4%20OR%20GY.5%20OR%20GY.6%20OR%20GY.7%20OR%20GY.8%20OR%20HF.1%20OR%20HF.1.1%20OR%20HF.1.2%20OR%20JF.1%20OR%20JF.2%20OR%20XBB.1.16.1%20OR%20XBB.1.16.2%20OR%20XBB.1.16.3%20OR%20XBB.1.16.4%20OR%20XBB.1.16.5%20OR%20XBB.1.16.6%20OR%20XBB.1.16.7%20OR%20XBB.1.16.8%20OR%20XBB.1.16.9%20OR%20XBB.1.16.10%20OR%20XBB.1.16.11%20OR%20XBB.1.16.12%20OR%20XBB.1.16.13%20OR%20XBB.1.16.14%20OR%20XBB.1.16.15%20OR%20XBB.1.16.16%20OR%20XBB.1.16.17%20OR%20XBB.1.16.18%20OR%20XBB.1.16.19%20OR%20XBB.1.16.20%20OR%20XBB.1.16.21%20OR%20XBB.1.16.22%20OR%20XBB.1.16.23%20OR%20XBB.1.16.24&detected=true"
    # url = "lineage-by-sub-admin-most-recent?pangolin_lineage=XBB.1.16%20OR%20FU.1&detected=true"

    result = endpoints._get_endpoint(url)
    result = result.json()

    url_v2 = "v2/" + url
    result_v2 = endpoints._get_endpoint(url_v2)
    result_v2 = result_v2.json()

    url_v3 = "v3/" + url
    result_v3 = endpoints._get_endpoint(url_v3)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v2) == True
    assert endpoints._deep_compare(result, result_v3) == True


def test_cumulative_prevalence_by_location_2():
    url = "lineage-by-sub-admin-most-recent?pangolin_lineage=XBB.1.16%20OR%20FU.1%20OR%20FU.2%20OR%20FU.2.1%20OR%20FU.3%20OR%20FU.3.1%20OR%20FU.4%20OR%20FU.5%20OR%20GY.1%20OR%20GY.2%20OR%20GY.2.1%20OR%20GY.3%20OR%20GY.4%20OR%20GY.5%20OR%20GY.6%20OR%20GY.7%20OR%20GY.8%20OR%20HF.1%20OR%20HF.1.1%20OR%20HF.1.2%20OR%20JF.1%20OR%20JF.2%20OR%20XBB.1.16.1%20OR%20XBB.1.16.2%20OR%20XBB.1.16.3%20OR%20XBB.1.16.4%20OR%20XBB.1.16.5%20OR%20XBB.1.16.6%20OR%20XBB.1.16.7%20OR%20XBB.1.16.8%20OR%20XBB.1.16.9%20OR%20XBB.1.16.10%20OR%20XBB.1.16.11%20OR%20XBB.1.16.12%20OR%20XBB.1.16.13%20OR%20XBB.1.16.14%20OR%20XBB.1.16.15%20OR%20XBB.1.16.16%20OR%20XBB.1.16.17%20OR%20XBB.1.16.18%20OR%20XBB.1.16.19%20OR%20XBB.1.16.20%20OR%20XBB.1.16.21%20OR%20XBB.1.16.22%20OR%20XBB.1.16.23%20OR%20XBB.1.16.24&detected=true&location_id=USA"

    result = endpoints._get_endpoint(url)
    result = result.json()

    url_v2 = "v2/" + url
    result_v2 = endpoints._get_endpoint(url_v2)
    result_v2 = result_v2.json()

    url_v3 = "v3/" + url
    result_v3 = endpoints._get_endpoint(url_v3)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v2) == True
    assert endpoints._deep_compare(result, result_v3) == True


def test_cumulative_prevalence_by_location_3():
    url = "lineage-by-sub-admin-most-recent?pangolin_lineage=XBB.1.16%20OR%20FU.1%20OR%20FU.2%20OR%20FU.2.1%20OR%20FU.3%20OR%20FU.3.1%20OR%20FU.4%20OR%20FU.5%20OR%20GY.1%20OR%20GY.2%20OR%20GY.2.1%20OR%20GY.3%20OR%20GY.4%20OR%20GY.5%20OR%20GY.6%20OR%20GY.7%20OR%20GY.8%20OR%20HF.1%20OR%20HF.1.1%20OR%20HF.1.2%20OR%20JF.1%20OR%20JF.2%20OR%20XBB.1.16.1%20OR%20XBB.1.16.2%20OR%20XBB.1.16.3%20OR%20XBB.1.16.4%20OR%20XBB.1.16.5%20OR%20XBB.1.16.6%20OR%20XBB.1.16.7%20OR%20XBB.1.16.8%20OR%20XBB.1.16.9%20OR%20XBB.1.16.10%20OR%20XBB.1.16.11%20OR%20XBB.1.16.12%20OR%20XBB.1.16.13%20OR%20XBB.1.16.14%20OR%20XBB.1.16.15%20OR%20XBB.1.16.16%20OR%20XBB.1.16.17%20OR%20XBB.1.16.18%20OR%20XBB.1.16.19%20OR%20XBB.1.16.20%20OR%20XBB.1.16.21%20OR%20XBB.1.16.22%20OR%20XBB.1.16.23%20OR%20XBB.1.16.24&ndays=60"

    result = endpoints._get_endpoint(url)
    result = result.json()

    url_v2 = "v2/" + url
    result_v2 = endpoints._get_endpoint(url_v2)
    result_v2 = result_v2.json()

    url_v3 = "v3/" + url
    result_v3 = endpoints._get_endpoint(url_v3)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v2) == True
    assert endpoints._deep_compare(result, result_v3) == True


def test_cumulative_prevalence_by_location_4():
    url = "lineage-by-sub-admin-most-recent?location_id=DEU&pangolin_lineage=EG.5.1&mutations=s:l24s&ndays=60"

    result = endpoints._get_endpoint(url)
    result = result.json()

    url_v2 = "v2/" + url
    result_v2 = endpoints._get_endpoint(url_v2)
    result_v2 = result_v2.json()

    url_v3 = "v3/" + url
    result_v3 = endpoints._get_endpoint(url_v3)
    result_v3 = result_v3.json()

    assert endpoints._deep_compare(result, result_v2) == True
    assert endpoints._deep_compare(result, result_v3) == True


# # ################################################
# # ############ v3 Tests
# # ################################################


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
    # assert res_json['results'].get('(BA.2) AND (USA)'), f"{url} no BA.2"
    # assert len(res_json['results']['(BA.2) AND (USA)']), f"{url} no results for BA.2"
    assert res_json["results"].get("BA.2"), f"{url} no BA.2"
    assert len(res_json["results"]["BA.2"]), f"{url} no results for BA.2"


def test_prev_by_location_2_1_v3():
    url = "v3/prevalence-by-location?pangolin_lineage=BA.2&mutations=S:D614G&location_id=USA"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    assert res_json.get("results"), f"{url} no results"
    assert len(res_json["results"]), f"{url} no results"
    # assert res_json['results'].get('(BA.2) AND (S:D614G) AND (USA)'), f"{url} no BA.2"
    # assert len(res_json['results']['(BA.2) AND (S:D614G) AND (USA)']), f"{url} no results for BA.2"
    assert res_json["results"].get("(BA.2) AND (S:D614G)"), f"{url} no BA.2"
    assert len(res_json["results"]["(BA.2) AND (S:D614G)"]), f"{url} no results for BA.2"


def test_heavy_query_v3():
    # url = 'v3/prevalence-by-location?pangolin_lineage=B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3,AY.4.4,AY.4.5,AY.5,AY.5.1,AY.5.2,AY.5.3,AY.5.4,AY.6,AY.7,AY.7.1,AY.7.2,AY.8,AY.9,AY.9.1,AY.9.2,AY.9.2.1,AY.10,AY.11,AY.12,AY.13,AY.14,AY.15,AY.16,AY.16.1,AY.17,AY.18,AY.19,AY.20,AY.21,AY.22,AY.23,AY.23.1,AY.24,AY.25,AY.26,AY.27,AY.28,AY.29,AY.29.1,AY.30,AY.31,AY.32,AY.33,AY.34,AY.34.1,AY.35,AY.36,AY.37,AY.38,AY.39,AY.39.1,AY.39.1.1,AY.39.2,AY.40,AY.41,AY.42,AY.43,AY.44,AY.45,AY.46,AY.46.1,AY.46.2,AY.46.3,AY.46.4,AY.46.5,AY.46.6,AY.47,AY.48,AY.49,AY.50,AY.51,AY.52,AY.53,AY.54,AY.55,AY.56,AY.57,AY.58,AY.59,AY.60,AY.61,AY.62,AY.63,AY.64,AY.65,AY.66,AY.67,AY.68,AY.69,AY.70,AY.71,AY.72,AY.73,AY.74,AY.75,AY.75.1,AY.76,AY.77,AY.78,AY.79,AY.80,AY.81,AY.82,AY.83,AY.84,AY.85,AY.86,AY.87,AY.88,AY.89,AY.90,AY.91,AY.91.1,AY.92,AY.93,AY.94,AY.95,AY.96,AY.97,AY.98,AY.98.1,AY.99,AY.99.1,AY.99.2,AY.100,AY.101,AY.102,AY.103,AY.104,AY.105,AY.106,AY.107,AY.108,AY.109,AY.110,AY.111,AY.112,AY.113,AY.114,AY.115,AY.116,AY.116.1,AY.117'
    url = "v3/prevalence-by-location?pangolin_lineage=B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


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


def test_lineage_mutations_v3():
    # Old schema
    # url = 'lineage-mutations?pangolin_lineage=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b'
    # New schema
    url = (
        "v3/lineage-mutations?lineages=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b"
    )
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


def test_lineage_mutations_v3_2():
    # Old schema
    # url = 'lineage-mutations?pangolin_lineage=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1'
    # New schema
    url = "v3/lineage-mutations?lineages=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1"
    res = endpoints._get_endpoint(url)
    res_json = res.json()
    endpoints._test_success(res_json, url)


URLS_TESTED = [
    # 'prevalence-by-location-all-lineages?location_id=USA&other_threshold=0.03&nday_threshold=5&ndays=60&other_exclude=p.1',
    "mutations?name=S:E484*",
    # 'location-lookup?id=USA_US-CA',
    "location?name=united*",
    "lineage?name=b.1.*",
    "mutations-by-lineage?mutations=S:E484K&location_id=USA",
    "mutation-details?mutations=S:E484K,S:N501Y",
    "prevalence-by-location?pangolin_lineage=B.1.617.2,AY.1,AY.2,AY.3,AY.3.1,AY.4,AY.4.1,AY.4.2,AY.4.3,AY.4.4,AY.4.5,AY.5,AY.5.1,AY.5.2,AY.5.3,AY.5.4,AY.6,AY.7,AY.7.1,AY.7.2,AY.8,AY.9,AY.9.1,AY.9.2,AY.9.2.1,AY.10,AY.11,AY.12,AY.13,AY.14,AY.15,AY.16,AY.16.1,AY.17,AY.18,AY.19,AY.20,AY.21,AY.22,AY.23,AY.23.1,AY.24,AY.25,AY.26,AY.27,AY.28,AY.29,AY.29.1,AY.30,AY.31,AY.32,AY.33,AY.34,AY.34.1,AY.35,AY.36,AY.37,AY.38,AY.39,AY.39.1,AY.39.1.1,AY.39.2,AY.40,AY.41,AY.42,AY.43,AY.44,AY.45,AY.46,AY.46.1,AY.46.2,AY.46.3,AY.46.4,AY.46.5,AY.46.6,AY.47,AY.48,AY.49,AY.50,AY.51,AY.52,AY.53,AY.54,AY.55,AY.56,AY.57,AY.58,AY.59,AY.60,AY.61,AY.62,AY.63,AY.64,AY.65,AY.66,AY.67,AY.68,AY.69,AY.70,AY.71,AY.72,AY.73,AY.74,AY.75,AY.75.1,AY.76,AY.77,AY.78,AY.79,AY.80,AY.81,AY.82,AY.83,AY.84,AY.85,AY.86,AY.87,AY.88,AY.89,AY.90,AY.91,AY.91.1,AY.92,AY.93,AY.94,AY.95,AY.96,AY.97,AY.98,AY.98.1,AY.99,AY.99.1,AY.99.2,AY.100,AY.101,AY.102,AY.103,AY.104,AY.105,AY.106,AY.107,AY.108,AY.109,AY.110,AY.111,AY.112,AY.113,AY.114,AY.115,AY.116,AY.116.1,AY.117",
    "prevalence-by-location?pangolin_lineage=b.1.1.7&location_id=USA",
    "prevalence-by-location",
    "global-prevalence?pangolin_lineage=b.1.1.7&cumulative=true",
    "global-prevalence?pangolin_lineage=b.1.1.7&mutations=S:E484K",
    "global-prevalence?pangolin_lineage=b.1.1.7",
    "global-prevalence",
    # 'sequence-count?location_id=USA_US-CA',
    # 'sequence-count?location_id=USA&cumulative=true&subadmin=true',
    # 'sequence-count',
    "mutations?name=S:E484*",
    "lineage-mutations?lineages=BA.2&mutations=S:D614G&frequency=0&gene=ORF1a,ORF1b,S,ORF7b",
    "lineage-mutations?lineages=BA.2%20OR%20BA.4.1%20OR%20BA.5.1&frequency=1",
]

ENDPOINTS_TESTED = [
    # 'prevalence-by-location-all-lineages'
    # 'location-lookup'
    # 'location'
    "prevalence-by-location"
    "lineage"
    "mutations-by-lineage"
    "mutation-details"
    "global-prevalence"
    'sequence-count'
    "lineage-mutations"
]

ENDPOINTS_NOT_TESTED = ["get-auth-token" "lineage-by-sub-admin-most-recent" "metadata" "status"]
