import http.client
import json
import logging
import ssl
from elasticsearchpy.indices import _ElasticSearchIndices
from elasticsearchpy.cluster import _ElasticSearchCluster


class ElasticRestResponse:
    """
    ElasticRestResponse is a wrapper object for http requests

    Attributes
    ----------
    good_codes : list
        A list of http codes that are used to consider
        the response a success (int)
    data : dict,string
        The data returned with an HTTP response
    reason : str
        The HTTP Response Reason of a request
    status : int
        The HTTP Response Code of a request
    """
    good_codes = [200, 201]

    def __init__(self, http_response):
        """
        Parameters
        ----------
        http_response : http.client.response
            The response of a http.client request
        """
        self.status = http_response.status
        self.reason = http_response.reason

        if self.status in self.good_codes:
            self.success = True
        else:
            self.success = False

        self.data = None
        self.data = http_response.read().decode("utf-8")

        try:
            self.data = json.loads(self.data)
        except:
            logging.debug("Response is not JSON")

    def to_dict(self):
        """
        returns the object as a dict

        Returns
        -------
        dict
            The object in dict form
        """
        return {"status": self.status,
                "reason": self.reason,
                "data": self.data
                }


class _ElasticSearchHost:
    """
    ElasticSearchHost is an object used to communicate with the
    elasticseach host or cluster

    Attributes
    ----------
    address : str
        The communication address of the host
    port : int
        The TCP port of the host

    Methods
    -------
    get_cluster()
        returns an ElasticSearchCluster object
    get_indices()
        returns an ElasticSearchIndices object
    rest_query(end_point, method="Get", body=None, headers=None)
        Executes a rest query against the cluster
    """
    _headers = {"Content-Type": "application/json"}

    def __init__(self, address, port=9200, use_ssl=False, cert=None, key=None, http_conn=None):
        """
        Parameters
        ----------
        address : str
            The IP address or hostname of the ElasticSearch host to communicate with
        port : int, optional
            The TCP port used to communicate with the ElasticSearch Host
        use_ssl : bool, optional;
            Use SSL to communicate with the ElasticSearch Host
        cert : str, optional
            The path to the SSL Certificate used to authenticate with the ElasticSearch Host
        key : str, optional
            The path to the SSL Key used to authenticate with the ElasticSearch Host
        http_conn : obj
            An http object to use for communication.  It must conform to http.client methods
        """
        self._address = address
        self._port = port

        if http_conn is not None:
            self._http_conn = http_conn
        else:
            if use_ssl:
                context = ssl.SSLContext()
                context.verify_mode = ssl.CERT_NONE

                self._http_conn = http.client.HTTPSConnection(
                    host=self._address,
                    port=self._port,
                    context=context,
                    key_file=key,
                    cert_file=cert)
            else:
                self._http_conn = http.client.HTTPConnection(
                    host=self._address,
                    port=self._port
                )
    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port

    def rest_query(self, end_point, method="GET", body=None, headers=None):
        """
        Executes a rest query on the Elasticsearch host.  Documentation for ElasticSearch Rest
        can be found at https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html

        Parameters
        ----------
        end_point : str
            The rest end point to query
        method : str
            The HTTP method used when querying the end point
        body : dict
            Data to be presented to the end point.
        headers : dict
            Additional http headers

        Returns
        -------
        ElasticRestResponse
            a rest response object
        """
        if headers is None:
            headers = self._headers

        self._http_conn.request(method, end_point,
                                body=body,
                                headers=headers
                                )
        logging.debug("REST: Request {}: {}".format(method, end_point))
        resp = ElasticRestResponse(
            self._http_conn.getresponse())

        logging.debug("REST: Response {}".format(resp))
        return resp

    def get_indices(self, indice_prefix=None, system_indices=False):
        """
        Returns an ElasticSearchIndices object

        Parameters
        ----------
        indice_prefix : str, optional
            a prefix for indices that the object should contain
        system_indices : bool, optional
            should the object contain system indices (default: False)

        Returns
        -------
        ElasticSearchIndices
            an object used to interact with ElasticSearchIndices
        """
        return _ElasticSearchIndices(self, indice_prefix, system_indices)

    def get_cluster(self):
        """
        Returns and ElasticSearchCluster object

        Returns
        -------
        ElasticSearchCluster
            an object used to describe and interact with the cluster
        """
        return _ElasticSearchCluster(self)
