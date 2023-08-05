import json
import unittest
from elasticsearchpy import ElasticSearchConnection

class ElasticPyUnitTest(unittest.TestCase):

    def setUp(self):
        self.http_conn = MockHttp()
        self.address = "1.1.1.1"
        self.port = 9300

        self.es_conn = ElasticSearchConnection(self.address, self.port,
                                         http_conn=self.http_conn)

        self.another_indices = [
            "another-test-indice", "another-test-indice2"
        ]

        self.test_indices = [
            "test-indice1", "test-indice2"
        ]

        self.yet_indices = ["yet-another-indice"]

        self.system_indices = [
            ".watcher-history-7-2018.09.19",
            ".watcher-history-7-2018.07.22"
        ]

        self.non_system_indices = self.another_indices + \
            self.test_indices + self.yet_indices
        self.all_indices = self.non_system_indices + self.system_indices

        indice_response = [
            "green open test-indice1                  SVkn-lo3TBKOZx0FI9CI_A 5 1      16     3    434kb   217kb",
            "green open .watcher-history-7-2018.09.19 R1yAnmoCSXea-nT6dp1iPg 1 1    8777     0   19.5mb   9.8mb",
            "green open test-indice2                  qG2rboxxSEqZLxDu0vZYHA 5 1       3     0   95.9kb  47.9kb",
            "green open .watcher-history-7-2018.07.22 7lMA2O9JRieOvlg-xACnZQ 1 1    8762     0   19.6mb   9.9mb",
            "green open another-test-indice           7UWO-yl9SlyrwbwyuoEU7g 5 1     570     0    1.1mb 606.9kb",
            "green open another-test-indice2          hf9yHkVqTn2dfH1RrMtE8w 5 1      29     0  973.1kb 486.5kb",
            "green open yet-another-indice            WFG9Hxx7TTm_wOs1eS-X1g 5 1    4454     0    3.9mb   1.9mb"
        ]

        self.http_conn.add_url_response(
            url="/_cat/indices",
            method="GET",
            status=200,
            reason="OK",
            response="\n".join(indice_response)
        )

        self.http_conn.add_url_response(
            url="/_cat/indices/test-indice1",
            method="GET",
            status=200,
            reason="OK",
            response="green open test-indice1                  SVkn-lo3TBKOZx0FI9CI_A 5 1      16     3    434kb   217kb"
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc",
            method="POST",
            status=200,
            reason="OK",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"0BGl1GYBx0qP_ThW_o2h",
                "_version":1,
                "result":"created"
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc",
            method="PUT",
            status=200,
            reason="OK",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"testdoc",
                "_version":1,
                "result":"created"
            }
        )



        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc",
            method="GET",
            status=404,
            reason="Not Found",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"testdoc",
                "found":False
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc2",
            method="GET",
            status=200,
            reason="OK",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"testdoc2",
                "_version":1,
                "found":True,
                "_source":{"Message":"Testing Data"}
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc3",
            method="PUT",
            status=403,
            reason="Forbidden",
            response={
                "error":{
                    "type":"security_exception",
                    "reason":"action [indices:data/write/index] is unauthorized for user [test user]"
                }
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc3",
            method="GET",
            status=403,
            reason="Forbidden",
            response={
                "error":{
                    "type":"security_exception",
                    "reason":"action [indices:data/read/get] is unauthorized for user [test user]"
                }
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc/testdoc4",
            method="GET",
            status=404,
            reason="Not Found",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"testdoc",
                "found":False
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_doc",
            method="POST",
            status=200,
            reason="OK",
            response={
                "_index":"test-indice1",
                "_type":"_doc",
                "_id":"OSnafweioaadjfewi",
                "_version":1,
                "result":"created"
            }
        )

        # This will return a successful create index
        self.http_conn.add_url_response(
            url="/test1",
            method="PUT",
            status=200,
            reason="OK",
            response={"acknowledged": True,
                      "shards_acknowledged": True, "index": "test1"}
        )

        # this will cause a failure due to template already existing
        self.http_conn.add_url_response(
            url="/test2",
            method="PUT",
            status=400,
            reason="Bad Request",
            response={
                "error": {
                    "type": "resource_already_exists_exception",
                    "reason": "index [test2/jhK0HBcOSiW2mjvUhr12wQ] already exists",
                    "index_uuid": "jhK0HBcOSiW2mjvUhr12wQ",
                    "index": "test2"
                }
            }
        )

        # this will cause a failure do to lack of permission to create an index
        self.http_conn.add_url_response(
            url="/test3",
            method="PUT",
            status=403,
            reason="Forbidden",
            response={
                "error": {
                    "type": "security_exception",
                    "reason": "action [indices:admin/create] is unauthorized for user [test_user]"
                }
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1",
            method="GET",
            status=200,
            reason="OK",
            response={
                "test-indice1":{
                    "aliases":{},
                    "mappings":{},
                    "settings":{
                        "index":{
                            "creation_date":"1540932108133",
                            "number_of_shards":"5",
                            "number_of_replicas":"1",
                            "uuid":"SVkn-lo3TBKOZx0FI9CI_A",
                            "version":{"created":"6020499"},
                            "provided_name":"test-indice1"
                        }
                    }
                }
            }
        )

        self.http_conn.add_url_response(
            url="/test-indice1/_mapping",
            method="GET",
            status=200,
            reason="OK",
            response={"test-indice1":{"mappings":{}}}
        )

        self.http_conn.add_url_response(
            url="/test-indice1",
            method="DELETE",
            status=200,
            reason="OK",
            response={"acknowledged": True}
        )


        self.http_conn.add_url_response(
            url="/test-indice2",
            method="DELETE",
            status=403,
            reason="Forbidden",
            response={
                "error": {
                    "type": "security_exception",
                    "reason": "action [indices:admin/delete] is unauthorized for user [test_user]"
                }
            }
        )


        self.http_conn.add_url_response(
            url="/test-indice3",
            method="DELETE",
            status=400,
            reason="Bad Request",
            response={
                "error": {
                    "type": "index_not_found_exception",
                    "reason": "no such index",
                    "resource.type": "index_or_alias",
                    "resource.id": "test-indice3",
                }
            }
        )


class MocHttpResponse:

    def __init__(self, status, reason, data):
        self.status = status
        self.reason = reason
        self._data = data

    def read(self):
        if isinstance(self._data,dict):
          return json.dumps(self._data).encode("utf-8")
        elif isinstance(self._data,str):
          return self._data.encode("utf-8")
        else:
          return self._data

class MockHttp:
    _urls = {}

    def request(self, method, url, body=None, headers=None):
        self._active_url = url
        self._active_method = method

    def add_url_response(self, url, method, status, reason, response):

        _method = {
            "status": int(status),
            "reason": reason,
            "response": response
        }

        if not url in self._urls:
          self._urls[url] = {}

        self._urls[url][method] = _method
        
    def list_urls(self):
      return self._urls

    def getresponse(self):
      bad_response = MocHttpResponse(404,"Not Found","None")
      if self._active_url in self._urls.keys():
        if self._active_method in self._urls.get(self._active_url).keys():
          url = self._urls.get(self._active_url).get(self._active_method)
          return MocHttpResponse(
              url.get("status"),
              url.get("reason"),
              url.get("response")
            )
        else:
          return bad_response
      else:
        return bad_response