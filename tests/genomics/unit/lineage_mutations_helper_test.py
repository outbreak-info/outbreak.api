import web.handlers.v3.genomics.helpers.lineage_mutations_helper as lineage_mutations_helper

import pytest

@pytest.mark.parametrize("lineage_param, mutation_param, expected_output", [
    ("LA", "", "pangolin_lineage: (LA)"),
    ("LA AND LB:1 AND LC:2", "", "pangolin_lineage: (LA AND LB:1 AND LC:2)"),
    ("LA OR LB OR LC", "", "pangolin_lineage: (LA OR LB OR LC)"),
    ("LA", "MA", "pangolin_lineage: (LA) AND mutations: (MA)"),
    ("LA AND LB", "MA AND MB", "pangolin_lineage: (LA AND LB) AND mutations: (MA AND MB)"),
    ("LA OR LB", "MA OR MB", "pangolin_lineage: (LA OR LB) AND mutations: (MA OR MB)"),
    ("LA AND LB", "MA OR MB", "pangolin_lineage: (LA AND LB) AND mutations: (MA OR MB)"),
])

def test_create_query_filter(lineage_param, mutation_param, expected_output):
    assert lineage_mutations_helper.create_query_filter(lineage_param, mutation_param) == expected_output

def test_parse_response():
    resp = {
        "hits": {
            "total": {
                "value": 10
            }
        },
        "aggregations": {
            "mutations": {
                "buckets": [
                    {
                        "key": "E:A123T",
                        "doc_count": 5
                    },
                    {
                        "key": "M:D456G",
                        "doc_count": 3
                    }
                ]
            }
        }
    }
    lineages = "BA.2"
    genes = ["e", "m"]
    frequency = 0.1
    result = lineage_mutations_helper.parse_response(resp=resp, frequency=frequency, lineages=lineages, genes=genes)
    expected_result = {
        "BA.2": [
            {
                "mutation": "E:A123T",
                "mutation_count": 5,
                "lineage_count": 10,
                "lineage": "BA.2",
                "gene": "E",
                "ref_aa": "A",
                "alt_aa": "T",
                "codon_num": 123,
                "codon_end": None,
                "type": "substitution",
                "prevalence": 0.5,
                "change_length_nt": None
            },
            {
                "mutation": "M:D456G",
                "mutation_count": 3,
                "lineage_count": 10,
                "lineage": "BA.2",
                "gene": "M",
                "ref_aa": "D",
                "alt_aa": "G",
                "codon_num": 456,
                "codon_end": None,
                "type": "substitution",
                "prevalence": 0.3,
                "change_length_nt": None
            }
        ]
    }
    # self.assertEqual(result, expected_result)
    assert result == expected_result
