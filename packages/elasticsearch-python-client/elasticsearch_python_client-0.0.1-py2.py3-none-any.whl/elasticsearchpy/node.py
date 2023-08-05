from elasticsearchpy.bases import _ElasticBase


class _ElasticSearchNode(_ElasticBase):
    _master_node = False
    _data_node = False
    _ingest_node = False
    _ip = None
    _transport_address = None
    _node = None
    _version = None
    _roles = None
    _os = None

    def __init__(self, node_name, es_host):
        self.name = node_name
        super().__init__(es_host)

    def _get_info(self):
        rest_query = self._es_host.rest_query(
            "/_nodes/{}".format(self.name)
        )

        if rest_query.success:
            nodes = rest_query.data.get("nodes")
            node_id = list(nodes.keys())[0]
            node_info = nodes.get(node_id)

            self._ip = node_info.get("ip")
            self._transport_address = node_info.get("transport_address")
            self._node = node_info.get("host")
            self._version = "{} (Build: {})".format(
                node_info.get("version"),
                node_info.get("build_hash")
            )
            self._roles = node_info.get("roles")
            self._os = "{}-{} ({})".format(
                node_info.get("os").get("name"),
                node_info.get("os").get("arch"),
                node_info.get("os").get("version"),
            )

            if "master" in self._roles:
                self._master_node = True

            if "data" in self._roles:
                self._data_node = True

            if "ingest" in self._roles:
                self._ingest_node = True

            self._cluster = node_info.get(
                "settings").get("cluster").get("name")
        else:
            raise(ElasticSearchException(rest_query))

    def data_node(self):
        return self.data_node

    def ingest_node(self):
        return self.ingest_node

    def ip(self):
        if self._ip is None:
            self._get_info()

        return self._ip

        print(rest_query)

    def master_node(self):
        return self._master_node

    def node(self):
        if self._node is None:
            self._get_info()

        return self._node

    def os(self):
        if self._os is None:
            self._get_info()

        return self._os

    def roles(self):
        if self._roles is None:
            self._get_info()

        return self._roles

    def to_dict(self):
        ret_dict = {
            "name": self.name,
            "ip": self._ip,
            "transport_address": self._transport_address,
            "node": self._node,
            "version": self._version,
            "roles": self._roles,
            "os": self._os
        }

        return ret_dict

    def transport_address(self):
        if self._transport_address is None:
            self._get_info()

        return self._transport_address

    def version(self):
        if self._version is None:
            self._get_info()

        return self._version
