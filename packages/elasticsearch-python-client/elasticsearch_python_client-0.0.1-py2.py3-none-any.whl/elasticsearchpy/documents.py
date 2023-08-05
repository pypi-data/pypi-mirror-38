from elasticsearchpy.bases import _ElasticBase
from elasticsearchpy.exceptions import ElasticForbidden, ElasticSearchException


class _ElasticSearchDocument(_ElasticBase):
    _source = None
    _version = None

    def __init__(self, indice, id, es_host=None):
        super().__init__(es_host)
        self._indice = indice
        self._id = id

    def __get_document(self):
        rest_query = self._es_host.rest_query(
            "{}/_doc/{}".format(self._indice, self._id)
        )

        if rest_query.success:
            self._version = rest_query.data.get("_version")
            self._source = rest_query.data.get("_source")
        else:
            raise(ElasticSearchException.get(rest_query))

    @property
    def indice(self):
        return self._indice

    @property
    def id(self):
        return self._id

    @property
    def message(self):
        if self._version is None:
            self.__get_document()

        return "{}".format(self._source)

    @property
    def message_dict(self):
        if self._version is None:
            self.__get_document()
        return self._source

    @property
    def version(self):
        if self._version is None:
            self.__get_document()
        return self._version
