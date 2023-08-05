from elasticsearchpy.cluster import _ElasticSearchCluster
from elasticsearchpy.documents import _ElasticSearchDocument
from elasticsearchpy.host import _ElasticSearchHost
from elasticsearchpy.indices import _ElasticSearchIndices
from elasticsearchpy.indices import _ElasticSearchIndice
from elasticsearchpy.node import _ElasticSearchNode


class ElasticSearchConnection(_ElasticSearchHost):
    pass


class ElasticSearchCluster(_ElasticSearchCluster):
    pass


class ElasticSearchDocument(_ElasticSearchDocument):
    pass


class ElasticSearchIndices(_ElasticSearchIndices):
    pass


class ElasticSearchIndice(_ElasticSearchIndice):
    pass


class ElasticSearchNode(_ElasticSearchNode):
    pass
