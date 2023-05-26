import pytest

from biothings.tests.web import BiothingsWebAppTest


class TestLineageMutationQuery(BiothingsWebAppTest):
    TEST_DATA_DIR_NAME = 'GenomicsTests'

    def test_000_basic_query(self):
        self.query(
            hits=True,
            q='BA.1.17.2'
        )

    def test_001_query_string(self):
        q = "pangolin_lineage:BA.1.17.2"
        res = self.query(
            hits=True,
            q=q
        )

        assert res['total'] == 1
        assert res['hits'][0]['pangolin_lineage'] == 'BA.1.17.2'
