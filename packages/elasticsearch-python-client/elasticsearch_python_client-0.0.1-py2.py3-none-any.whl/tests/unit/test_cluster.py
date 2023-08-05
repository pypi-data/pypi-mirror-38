import unittest
from .unit_test_base import ElasticPyUnitTest
from elasticsearchpy import ElasticSearchCluster
from elasticsearchpy.cluster import _ElasticSearchCluster
from elasticsearchpy.exceptions import ElasticForbidden
from elasticsearchpy import ElasticSearchConnection
from elasticsearchpy.node import _ElasticSearchNode


class ElasticSearchClusterUnitTest(ElasticPyUnitTest):

    def setUp(self):
        super().setUp()

        self.http_conn.add_url_response(
            url="/_nodes/_all",
            method="GET",
            status=200,
            reason="OK",
            response={
                "nodes": {
                    "adiaksdifasdkf": {
                        "name": "node1"
                    },
                    "9asjdfuaskfa0f": {
                        "name": "node2"
                    },
                    "iasasdflsiaowd": {
                        "name": "node3"
                    }
                }
            }
        )

        self.cluster_name = "test_cluster"
        self.cluster_status = "green"
        self.cluster_n_o_nodes = 3
        self.active_ps = 50
        self.active_shards = 150
        self.delayed_ua = 1
        self.initializing_shards = 2
        self.inflight_fetch = 23
        self.num_pending_tasks = 101
        self.reloc_shards = 5
        self.unassigned_shards = 20
        self.node_names = ["node1", "node2", "node3"]
        self.http_conn.add_url_response(
            url="/_cluster/health",
            method="GET",
            status=200,
            reason="OK",
            response={
                "cluster_name": self.cluster_name,
                "status": self.cluster_status,
                "number_of_nodes": self.cluster_n_o_nodes,
                "number_of_data_nodes": self.cluster_n_o_nodes,
                "active_primary_shards": self.active_ps,
                "active_shards": self.active_shards,
                "relocating_shards": self.reloc_shards,
                "initializing_shards": self.initializing_shards,
                "unassigned_shards": self.unassigned_shards,
                "delayed_unassigned_shards": self.delayed_ua,
                "number_of_pending_tasks": self.num_pending_tasks,
                "number_of_in_flight_fetch": self.inflight_fetch
            }

        )

    def test_ElasticSearchCluster(self):
        cluster = self.es_conn.get_cluster()
        self.assertTrue(isinstance(cluster, _ElasticSearchCluster))

        cluster = ElasticSearchCluster(self.es_conn)
        self.assertTrue(isinstance(cluster, ElasticSearchCluster))

    def test_status(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.status, self.cluster_status)

    def test_active_primary_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.active_primary_shards, self.active_ps)

    def test_active_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.active_shards, self.active_shards)

    def test_data_nodes(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.data_nodes, self.cluster_n_o_nodes)

    def test_delayed_unassigned_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.delayed_unassigned_shards, self.delayed_ua)

    def test_get_node(self):
        cluster = ElasticSearchCluster(self.es_conn)
        node = cluster.get_node("node1")
        self.assertTrue(isinstance(node, _ElasticSearchNode))

    def test_initializing_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.initializing_shards, self.initializing_shards)

    def test_in_flight_fetch(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.in_flight_fetch, self.inflight_fetch)

    def test_name(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.name, self.cluster_name)

    def test_nodes(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.nodes, self.cluster_n_o_nodes)

    def test_node_names(self):
        cluster = ElasticSearchCluster(self.es_conn)
        node_names = cluster.node_names 
        self.assertTrue(isinstance(node_names, list))
        self.assertEqual(cluster.node_names, self.node_names)

    def test_pending_tasks(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.pending_tasks, self.num_pending_tasks)

    def test_relocating_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.relocating_shards, self.reloc_shards)

    def test_status(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.status, self.cluster_status)

    def test_to_dict(self):
        cluster = ElasticSearchCluster(self.es_conn)
        verify_dict = {
            "name": self.cluster_name,
            "status": self.cluster_status,
            "nodes": self.cluster_n_o_nodes,
            "data_nodes": self.cluster_n_o_nodes,
            "active_primary_shards": self.active_ps,
            "active_shards": self.active_shards,
            "relocating_shards": self.reloc_shards,
            "initializing_shards": self.initializing_shards,
            "unassigned_shards": self.unassigned_shards,
            "delayed_unassigned_shards": self.delayed_ua,
            "pending_tasks": self.num_pending_tasks,
            "in_flight_fetch": self.inflight_fetch,
            "node_names": self.node_names
        }
        self.assertEqual(cluster.to_dict(), verify_dict)

    def test_unassigned_shards(self):
        cluster = ElasticSearchCluster(self.es_conn)
        self.assertEqual(cluster.unassigned_shards, self.unassigned_shards)

    def test_get_node_info(self):
        cluster = ElasticSearchCluster(self.es_conn)

        self.http_conn.add_url_response(
            url="/_nodes/_all",
            method="GET",
            status=403,
            reason="Forbidden",
            response={
                "error": {
                    "type": "Unauthorized",
                    "reason": "You aren't allowed to do this"
                }
            }
        )
        with self.assertRaises(ElasticForbidden):
            node_names = cluster.node_names
