import logging
from elasticsearchpy.exceptions import ElasticForbidden, ElasticSearchException
from elasticsearchpy.exceptions import IndexAlreadyExists, ResouceNotFound
from elasticsearchpy.exceptions import DocumentAlreadyExists, DocumentDoesNotExist
from elasticsearchpy.bases import _ElasticBase
from elasticsearchpy.documents import _ElasticSearchDocument


class _ElasticSearchIndices(_ElasticBase):
    """
    ElasticSearchIndices class is used to interact with larger indices functions, such as
    listing all or filtered indices, creating and deleting indices

    Attributes
    ----------
    count : int
        Then number of indices returned as result of the filters
    indices: list(str)
        A list of the indice names

    Methods
    -------
    create_indice(name,shards=None,replicas=None,mappings=None,Aliases=None)
        create an indice
    delete_indice(name)
        delete an existing indice
    get_indice(name)
        returns an ElasticSearchIndice object

    """
    _indices = None

    def __init__(self, es_host, indice_prefix=None, system_indices=False):
        """
        Parameters
        ----------
        es_host : ElasticSearchHost
            The ElasticSearchHost object used to communicate with elasticsearch
        indice_prefix : str, optional
            An indice name prefix filter.  This allows you to filter returned indices
        system_indices : bool
            Would you like to view system indices
        """

        self._indice_prefix = indice_prefix
        self._system_indices = system_indices
        super().__init__(es_host)

    def _get_indices(self):
        # set self._indices to a new list everytime this method is run
        self._indices = []
        query = self._es_host.rest_query("/_cat/indices")

        if query.success:
            indice_list = query.data.split("\n")

            for record in indice_list:
                s_rec = record.split()
                if len(s_rec) >= 2:
                    indice_name = s_rec[2]

                    if not self._system_indices:
                        if indice_name.startswith("."):
                            continue

                    if self._indice_prefix is not None:
                        if not indice_name.startswith(self._indice_prefix):
                            continue

                    self._indices.append(indice_name)

        else:
            print(query)

    def create_indice(self, name, shards=None, replicas=None, mappings=None, aliases=None):
        """
        Create an indice on the elasticsearch cluster

        Parameters
        ----------
        name : str
            Then name of the indice that you would like to create
        shards : int, optional
            The number of primary shards for the indice
        replicas : int, optional
            The number of replica shards for the indice
        mappings : dict, optional
            The mappings associated with the indice https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html
        aliases : dict, optional
            The alias mappings associated with the indice https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html

        Returns
        -------
        ElasticSearchIndice : obj

        Raises
        ------
        ElasticForbidden
            Raises this error if the user isn't isn't allowed to create
            the indice
        IndexAlreadyExists
            Raises this error if the indice alredy exists
        """

        if self._indices is None:
            self._get_indices()

        data = None
        if shards is not None:
            data = {
                "settings": {
                    "index": {
                        "number_of_shards": shards,
                        "number_of_replicas": 0
                    }
                }
            }

        if replicas is not None:
            if data is not None:
                data["settings"]["index"]["number_of_replicas"] = replicas
            else:
                data = {
                    "settings": {
                        "index": {
                            "number_of_shards": 1,
                            "number_of_replicas": replicas
                        }
                    }
                }

        if mappings is not None:
            if data is not None:
                data["mappings"] = mappings
            else:
                data = {"mappings": mappings}

        if aliases is not None:
            if data is not None:
                data["aliases"] = aliases
            else:
                data = {"aliases": aliases}

        rest_query = self._es_host.rest_query(
            end_point="/{}".format(name),
            method="PUT",
            body=data)

        if rest_query.success:
            self._indices.append(name)
            return _ElasticSearchIndice(name, self._es_host)

        else:
            raise(ElasticSearchException.get_exception(rest_query))

    @property
    def count(self):
        if self._indices is None:
            self._get_indices()

        return len(self._indices)

    def delete_indice(self, name):
        """
        Delete an indice from the elastic search cluster

        Parameters
        ----------
        name : str
            The name of the indice to delete

        Returns
        -------
        bool

        Raises
        ------
        ElasticForbidden
            Raises this error if the user isn't isn't allowed to delete
            the indice
        IndiceNotFound
            Raises this error if the indice does not exist
        """

        if self._indices is None:
            self._get_indices()

        rest_query = self._es_host.rest_query(
            end_point="/{}".format(name),
            method="DELETE"
        )

        if rest_query.success:
            self._indices.remove(name)
            return True
        else:
            raise(ElasticSearchException.get_exception(rest_query))

    @property
    def indices(self):
        if self._indices is None:
            self._get_indices()

        return self._indices

    def get_indice(self, name):
        if self._indices is None:
            self._get_indices()

        ret_indice = None
        if name in self._indices:
            ret_indice = _ElasticSearchIndice(name, self._es_host)

        return ret_indice


class _ElasticSearchIndice(_ElasticBase):
    """
    ElasticSearchIndice is a class used to get status and interact with 
    an Elastic Search Indice directly

    Attributes
    ----------
    deleted_docs : int
        The number of documents that have been deleted from the indice
    docs : int
        The number of documents on the indice
    health : str
        The health designator for the Indice (green, yellow, red)
    primary_shards : int
        The number of primary shards
    replicas : int
        The number of replicas per primary shards
    size : str
        The disk size of the indice
    status : str
        The status of the indice (open, close, etc....)
    total_shards : int
        The number of total shards
    uuid : str
        The UUID of the indice

    Methods
    -------
    refresh()
        Updates the data of the object
    to_dict()
        The dict version of the object
    """
    _docs = None
    _deleted_docs = None
    _size = None
    _total_shards = None
    _primary_shards = None
    _replicas = None
    _status = None
    _health = None
    _uuid = None
    _mappings = None

    def __init__(self, name, es_host):
        """
        Parameters
        ----------
        name : str
            The Name of the indice
        es_host : ElasticSearchHost
            The ElasticSearchHost Object used to communicate with elasticsearch
        """
        self.name = name
        super().__init__(es_host)

    def _get_stats(self):
        stats = self._es_host.rest_query(
            "/_cat/indices/{}".format(self.name)
        )

        if stats.success:
            data = stats.data.split()

            self._docs = int(data[6])
            self._deleted_docs = int(data[7])
            self._size = data[8]
            self._primary_shards = int(data[4])
            self._replicas = int(data[5])
            self._status = data[1]
            self._health = data[0]
            self._uuid = data[3]
            self._total_shards = self._primary_shards * (self._replicas + 1)
        else:
            logging.error("Unable to get indice statistics: {}:{}".format(
                stats.status, stats.reason))
            logging.debug("REST ERROR: {}".format(stats.data))

    def _get_mappings(self):
        rest_query = self._es_host.rest_query(
            "/{}/_mapping".format(self.name)
        )

        if rest_query.success:
            self._mappings = rest_query.data.get(self.name).get("mappings")
        else:
            if rest_query.status == 404:
                return None
            else:
                raise(ElasticSearchException(rest_query))

    def to_dict(self):
        """
        Returns
        -------
        dict
            A dict form of this object
        """
        if self._docs is None:
            self._get_stats()

        ret_dict = {
            "name": self.name,
            "uuid": self._uuid,
            "docs": self._docs,
            "deleted_docs": self._deleted_docs,
            "size": self._size,
            "primary_shards": self._primary_shards,
            "replicas": self._replicas,
            "total_shards": self._total_shards,
            "status": self._status,
            "health": self._health
        }

        return ret_dict

    def _doc_exists(self, name):
        rest_query = self._es_host.rest_query(
            "/{}/_doc/{}".format(self.name, name)
        )

        if rest_query.success:
            if rest_query.data.get("found"):
                return True
            else:
                return False
        else:
            if rest_query.status == 404:
                return False
            else:
                raise(ElasticSearchException.get_exception(rest_query))

    def create_doc(self, data, name=None):
        if not isinstance(data, dict):
            raise(TypeError("Expecting dict but received {}".format(
                type(data))))

        end_point = "/{}/_doc".format(self.name)
        method = "POST"

        if name is not None:
            if self._doc_exists(name):
                raise(DocumentAlreadyExists(
                    self.name, name
                ))
            end_point += "/{}".format(name)
            method = "PUT"

        rest_query = self._es_host.rest_query(
            end_point, method, data
        )

        if rest_query.success:
            return _ElasticSearchDocument(self.name,
                                         rest_query.data.get("_id"),
                                         self._es_host)
        else:
            raise(ElasticSearchException.get_exception(rest_query))

    @property
    def deleted_docs(self):
        if self._deleted_docs is None:
            self._get_stats()

        return self._deleted_docs

    @property
    def docs(self):
        if self._docs is None:
            self._get_stats()

        return self._docs

    def get_doc(self, name):
        if self._doc_exists(name):
            return _ElasticSearchDocument(self.name, name,
                                         self._es_host)
        else:
            raise(DocumentDoesNotExist(self.name, name))

    @property
    def health(self):
        if self._health is None:
            self._get_stats()

        return self._health

    @property
    def mappings(self):
        if self._mappings is None:
            self._get_mappings()

        return self._mappings

    @property
    def primary_shards(self):
        if self._primary_shards is None:
            self._get_stats()

        return self._primary_shards

    def refresh(self):
        self._get_stats()
        return self

    @property
    def replicas(self):
        if self._replicas is None:
            self._get_stats()

        return self._replicas

    @property
    def size(self):
        if self._size is None:
            self._get_stats()

        return self._size

    @property
    def status(self):
        if self._status is None:
            self._get_stats()

        return self._status

    @property
    def total_shards(self):
        if self._total_shards is None:
            self._get_stats()

        return self._total_shards

    @property
    def uuid(self):
        if self._uuid is None:
            self._get_stats()

        return self._uuid
