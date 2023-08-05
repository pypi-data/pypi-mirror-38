import json


class ElasticSearchGeneralException(Exception):

    def __init__(self, es_error):
        self.type = es_error.get("error").get("type")
        self.reason = es_error.get("error").get("reason")
        self.message = "{}: {}".format(self.type, self.reason)


class ElasticSearchException:

    def get_exception(query_response):
        if query_response.status == 403:
            return ElasticForbidden(query_response.data)
        else:
            error = query_response.data.get("error")
            if error.get("type") == "resource_already_exists_exception":
                if "index" in error:
                    return IndexAlreadyExists(query_response.data)
                else:
                    return ElasticSearchGeneralException(query_response.data)
            elif error.get("type") == "index_not_found_exception":
                return IndiceNotFound(query_response.data)
            else:
                ElasticSearchGeneralException(query_response.data)


class ElasticForbidden(ElasticSearchGeneralException):
    pass


class IndexAlreadyExists(ElasticSearchGeneralException):

    def __init__(self, es_error):
        super().__init__(es_error)
        error = es_error.get("error")
        self.index = error.get("index")
        self.index_uuid = error.get("index_uuid")


class IndiceNotFound(ElasticSearchGeneralException):

    def __init__(self, es_error):
        super().__init__(es_error)
        self.index = es_error.get("error").get("index")


class DocumentAlreadyExists(Exception):

    def __init__(self, indice, document_id):
        self.reason = "Document Already Exists"
        self.indice = indice
        self.document_id = document_id
        self.message = "Document {} already exists in indice {}".format(
            document_id, indice
        )


class DocumentDoesNotExist(Exception):

    def __init__(self, indice, document_id):
        self.reason = "Document Does Not Exists"
        self.indice = indice
        self.document_id = document_id
        self.message = "Document {} does not exist in indice {}".format(
            document_id, indice
        )


class ResouceNotFound(ElasticSearchGeneralException):

    def __init__(self, es_error):
        super().__init__(es_error)
        error = es_error.get("error")
        self.resource_type = error.get("resource.type")
        self.resource = error.get("resource.id")
