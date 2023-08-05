import unittest
from .unit_test_base import ElasticPyUnitTest, MockHttp
from elasticsearchpy import ElasticSearchIndices
from elasticsearchpy.indices import _ElasticSearchIndices
from elasticsearchpy import ElasticSearchIndice
from elasticsearchpy.indices import _ElasticSearchIndice
from elasticsearchpy import ElasticSearchCluster
from elasticsearchpy.exceptions import IndexAlreadyExists
from elasticsearchpy.exceptions import ElasticForbidden
from elasticsearchpy.exceptions import IndiceNotFound


class TestElasticSearchIndices(ElasticPyUnitTest):

    def setUp(self):
        super().setUp()

    def test_elasticsearch_indices_class(self):
        indices = self.es_conn.get_indices()
        self.assertTrue(isinstance(indices, _ElasticSearchIndices))

        indices = ElasticSearchIndices(self.es_conn)
        self.assertTrue(isinstance(indices, _ElasticSearchIndices))

    def test_count(self):
        indices = ElasticSearchIndices(self.es_conn)
        self.assertEqual(indices.count, len(self.non_system_indices))

        indices = ElasticSearchIndices(self.es_conn, system_indices=True)
        self.assertEqual(indices.count, len(self.all_indices))

        indices = ElasticSearchIndices(self.es_conn, indice_prefix="another")
        self.assertEqual(indices.count, len(self.another_indices))

        indices = ElasticSearchIndices(
            self.es_conn, indice_prefix="yet", system_indices=True)
        self.assertEqual(indices.count, len(self.yet_indices))

    def test_indices(self):

        indices = ElasticSearchIndices(self.es_conn)
        self.assertEqual(indices.indices.sort(),
                         self.non_system_indices.sort())

        indices = ElasticSearchIndices(self.es_conn, system_indices=True)
        self.assertEqual(indices.indices.sort(), self.all_indices.sort())

        indices = ElasticSearchIndices(self.es_conn, indice_prefix="another")
        self.assertEqual(indices.indices.sort(), self.another_indices.sort())

        indices = ElasticSearchIndices(
            self.es_conn, indice_prefix="yet", system_indices=True)
        self.assertEqual(indices.indices.sort(), self.yet_indices.sort())

    def test_create_indice(self):
        indices = ElasticSearchIndices(self.es_conn)
        new_indice = indices.create_indice("test1")
        self.assertTrue(isinstance(new_indice, _ElasticSearchIndice))

        with self.assertRaises(IndexAlreadyExists):
            new_indice_2 = indices.create_indice("test2")

        with self.assertRaises(ElasticForbidden):
            new_indice_3 = indices.create_indice("test3")

    def test_delete_indice(self):
        indices = ElasticSearchIndices(self.es_conn)
        self.assertTrue(indices.delete_indice("test-indice1"))

        with self.assertRaises(ElasticForbidden):
            indices.delete_indice("test-indice2")

        with self.assertRaises(IndiceNotFound):
            indices.delete_indice("test-indice3")

    def test_get_indice(self):
        indices = ElasticSearchIndices(self.es_conn)
        indice = indices.get_indice("test-indice1")
        self.assertTrue(isinstance(indice, _ElasticSearchIndice))
