import unittest
from .unit_test_base import ElasticPyUnitTest
from elasticsearchpy import ElasticSearchConnection
from elasticsearchpy import ElasticSearchIndices
from elasticsearchpy.indices import _ElasticSearchIndices
from elasticsearchpy import ElasticSearchCluster
from elasticsearchpy.host import  ElasticRestResponse
from elasticsearchpy.cluster import _ElasticSearchCluster


class ElastiSearchHostUnitTest(ElasticPyUnitTest):

    def setUp(self):
        super().setUp()
        self.http_conn.add_url_response(
            url="testpoint",
            method="GET",
            status=200,
            reason="OK",
            response="{\"Good\":\"Data\"}"
        )

    def test_ElasticSearchConnection(self):
        host = ElasticSearchConnection(self.address, self.port,
                                http_conn=self.http_conn)
        self.assertTrue(isinstance(host, ElasticSearchConnection))

    def test_rest_query(self):
        host = ElasticSearchConnection(self.address, self.port,
                                http_conn=self.http_conn)
        response = host.rest_query("testpoint")
        self.assertTrue(isinstance(response, ElasticRestResponse))
        self.assertTrue(response.success)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.reason, "OK")
        self.assertTrue(isinstance(response.data, dict))
        self.assertEqual(response.data.get("Good"), "Data")

    def test_get_indices(self):
        host = ElasticSearchConnection(self.address, self.port,
                                http_conn=self.http_conn)

        indices = host.get_indices()
        self.assertTrue(isinstance(indices, _ElasticSearchIndices))

    def test_get_cluster(self):
        host = ElasticSearchConnection(self.address, self.port,
                                http_conn=self.http_conn)

        cluster = host.get_cluster()
        self.assertTrue(isinstance(cluster, _ElasticSearchCluster))
