from elasticsearchpy.bases import _ElasticBase
from elasticsearchpy.exceptions import ElasticForbidden, ElasticSearchException
from elasticsearchpy.node import _ElasticSearchNode


class _ElasticSearchCluster(_ElasticBase):
    """
    A class used to represent an ElasticSearch Cluster and the attributes
    of the cluster

    Attributes
    ----------
    active_primary_shards : int
        The number of active primary shards
    active_shards : int
        The number of active shards
    data_nodes : int
        The number of data nodes in the cluster
    delayed_unassigned_shards : int
        The number of shard that are delayed in being unassinged
    initializing_shards:
        The number of initialize shards
    name : str
        Then name of the cluster
    node_names : list(str)
        A list of the names of the hosts in the cluster
    nodes : int
        The number of nodes in the cluster
    pending_tasks : int
        The number of cluster pending tasks
    in_flight_fetch : int
        The number of fetches in flight or progress
    relocating_shards : int
        The number of shards actively relocating

    Methods
    -------
    get_node(name):
        Returns an ElasticSearchNode obj
    refresh():
        Refreshes the data about the cluster
    to_dict():
        Returns the object as a dict

    """
    _name = None
    _status = None
    _nodes = None
    _data_nodes = None
    _active_primary_shards = None
    _active_shards = None
    _relocating_shards = None
    _initializing_shards = None
    _unassigned_shards = None
    _delayed_unassigned_shards = None
    _pending_tasks = None
    _in_flight_fetch = None
    _node_names = None

    def __init__(self, es_host):
        """
        Parameters
        ----------
        es_host : ElasticSearchHost
            The object used to communciate with Elastic Search
        """
        super().__init__(es_host)

    def _get_node_names(self, all=True, master=False, exclude_master=False,
                        ingest=False, exclude_ingest=False,
                        data=False, exclude_data=False,
                        coordinating=False, search_string=None):
        self._node_names = []

        types = []

        if all:
            types.append("_all")
        elif corrdinating:
            types.append("coordinating_only:true")
        else:
            if master and not exclude_master:
                types.append("master:true")
            elif exclude_master and not master:
                types.append("master:false")
            elif master and exclude_master:
                logging.error(
                    "Unable to exclude and include master nodes in a search")

            if ingest and not exclude_ingest:
                types.append("ingest:true")
            elif exclude_ingest and not ingest:
                types.append("ingest:false")
            elif ingest and exclude_ingest:
                logging.error(
                    "Unable to exclude and include ingest nodes in a search")

            if data and not exclude_data:
                types.append("data:true")
            elif exclude_data and not data:
                types.append("data:false")
            elif data and exclude_data:
                logging.error(
                    "Unable to exclude and include data nodes in a search")

        end_point_base = "/_nodes"

        if search_string is None:
            end_point = "{}/{}".format(end_point_base, ",".join(types))
        else:
            end_point = "{}/{}".format(end_point_base, search_string)

        rest_query = self._es_host.rest_query(end_point)

        if rest_query.success:
            node_data = rest_query.data.get("nodes")
            for key in node_data.keys():
                self._node_names.append(node_data.get(key).get("name"))
        else:
            raise(ElasticSearchException.get_exception(rest_query))

    def _get_cluster_info(self):
        rest_query = self._es_host.rest_query(
            "/_cluster/health"
        )

        if rest_query.success:
            data = rest_query.data
            self._name = data.get("cluster_name")
            self._status = data.get("status")
            self._nodes = data.get("number_of_nodes")
            self._data_nodes = data.get("number_of_data_nodes")
            self._active_primary_shards = data.get("active_primary_shards")
            self._active_shards = data.get("active_shards")
            self._relocating_shards = data.get("relocating_shards")
            self._initializing_shards = data.get("initializing_shards")
            self._unassigned_shards = data.get("unassigned_shards")
            self._delayed_unassigned_shards = data.get(
                "delayed_unassigned_shards")
            self._pending_tasks = data.get("number_of_pending_tasks")
            self._in_flight_fetch = data.get("number_of_in_flight_fetch")
        else:
            raise(ElasticSearchException(rest_query))

        self._get_node_names()

    @property
    def active_primary_shards(self):
        if self._active_primary_shards is None:
            self._get_cluster_info()

        return self._active_primary_shards

    @property
    def active_shards(self):
        if self._active_shards is None:
            self._get_cluster_info()

        return self._active_shards

    @property
    def data_nodes(self):
        if self._data_nodes is None:
            self._get_cluster_info()

        return self._data_nodes

    @property
    def delayed_unassigned_shards(self):
        if self._delayed_unassigned_shards is None:
            self._get_cluster_info()

        return self._delayed_unassigned_shards

    def get_node(self, node_name):
        """
        This returns an _ElasticSearchNode used to interact with an
        ElasticSearch Node

        Parameters
        ----------
        node_name : str
            The name of the elasticsearch node

        Returns
        -------
        _ElasticSearchNode
            An ElasticSearch Node Obj
        """
        return _ElasticSearchNode(node_name, self._es_host)

    @property
    def initializing_shards(self):
        if self._initializing_shards is None:
            self._get_cluster_info()

        return self._initializing_shards

    @property
    def in_flight_fetch(self):
        if self._in_flight_fetch is None:
            self._get_cluster_info()

        return self._in_flight_fetch

    @property
    def name(self):
        if self._name is None:
            self._get_cluster_info()

        return self._name

    @property
    def nodes(self):
        if self._nodes is None:
            self._get_cluster_info()

        return self._nodes

    @property
    def node_names(self):
        if self._node_names is None:
            self._get_node_names()

        return self._node_names

    @property
    def pending_tasks(self):
        if self._pending_tasks is None:
            self._get_cluster_info()

        return self._pending_tasks

    def refresh(self):
        """
        Updates the node data
        """
        self.get_cluster_info()

    @property
    def relocating_shards(self):
        if self._relocating_shards is None:
            self._get_cluster_info()

        return self._relocating_shards

    @property
    def status(self):
        if self._status is None:
            self._get_cluster_info()

        return self._status

    def to_dict(self):
        """
        Returns a dict version of the node object

        Returns
        -------
        dict
        """
        if self._status is None:
            self._get_cluster_info()

        ret_dict = {
            "name": self._name,
            "status": self._status,
            "nodes": self._nodes,
            "data_nodes": self._data_nodes,
            "active_primary_shards": self._active_primary_shards,
            "active_shards": self._active_shards,
            "relocating_shards": self._relocating_shards,
            "initializing_shards": self._initializing_shards,
            "unassigned_shards": self._unassigned_shards,
            "delayed_unassigned_shards": self._delayed_unassigned_shards,
            "pending_tasks": self._pending_tasks,
            "in_flight_fetch": self._in_flight_fetch,
            "node_names": self._node_names
        }

        return ret_dict

    @property
    def unassigned_shards(self):
        if self._unassigned_shards is None:
            self._get_cluster_info()

        return self._unassigned_shards
