class _ElasticBase:

    def __init__(self, es_host):
        self._es_host = es_host

    def __str__(self):
      return "{}".format(self.to_dict())

    def to_dict(self):
      return {}