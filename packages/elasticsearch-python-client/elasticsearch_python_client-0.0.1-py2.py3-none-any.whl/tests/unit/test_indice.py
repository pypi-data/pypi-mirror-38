import unittest
from .unit_test_base import ElasticPyUnitTest, MockHttp
from elasticsearchpy import ElasticSearchIndice
from elasticsearchpy import ElasticSearchDocument
from elasticsearchpy.documents import _ElasticSearchDocument
from elasticsearchpy.exceptions import DocumentAlreadyExists
from elasticsearchpy.exceptions import DocumentDoesNotExist
from elasticsearchpy.exceptions import ElasticForbidden


class TestElasticSearchIndice(ElasticPyUnitTest):

    def setUp(self):
        super().setUp()
        self.test_indice = "test-indice1"
        self.test_dict = {
            'name': 'test-indice1',
            'uuid': 'SVkn-lo3TBKOZx0FI9CI_A',
            'docs': 16,
            'deleted_docs': 3,
            'size': '434kb',
            'primary_shards': 5,
            'replicas': 1,
            'total_shards': 10,
            'status': 'open',
            'health': 'green'
        }

    def test_elasticsearch_indice_class(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertTrue(indice, ElasticSearchIndice)

    def test_deleted_docs(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.deleted_docs, 3)

    def test_docs(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.docs, 16)

    def test_health(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.health, "green")

    def test_mappings(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        mappings = indice.mappings
        print(mappings)
        self.assertTrue(isinstance(mappings, dict))
        self.assertEqual(mappings, {})

    def test_primary_shards(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.primary_shards, 5)

    def test_replicas(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.replicas, 1)

    def test_size(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.size, "434kb")

    def test_status(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.status, "open")

    def test_to_dict(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.to_dict(), self.test_dict)

    def test_total_shards(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.total_shards, 10)

    def test_uuid(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        self.assertEqual(indice.uuid, "SVkn-lo3TBKOZx0FI9CI_A")

    def test_create_doc(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)
        doc = indice.create_doc({"message": "test data"}, "testdoc")
        self.assertTrue(isinstance(doc, _ElasticSearchDocument))

        doc = indice.create_doc({"message": "test data"})
        self.assertTrue(isinstance(doc, _ElasticSearchDocument))
        self.assertEqual(doc.id, "OSnafweioaadjfewi")

        with self.assertRaises(DocumentAlreadyExists):
            doc = indice.create_doc({"message": "test data"}, "testdoc2")

        with self.assertRaises(ElasticForbidden):
            doc = indice.create_doc({"message": "test data"}, "testdoc3")

    def test_get_doc(self):
        indice = ElasticSearchIndice(self.test_indice, self.es_conn)

        doc = indice.get_doc("testdoc2")
        self.assertTrue(isinstance(doc, _ElasticSearchDocument))

        with self.assertRaises(DocumentDoesNotExist):
            doc = indice.get_doc("testdoc4")

        with self.assertRaises(ElasticForbidden):
            doc = indice.get_doc("testdoc3")
