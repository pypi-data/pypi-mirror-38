from collections import namedtuple, OrderedDict

from . import __version__
from intake.source import base

dtypes = [('row', 'str'),
          ('column_family', 'str'),
          ('column_qualifier', 'str'),
          ('column_visibility', 'str'),
          ('time', 'datetime64[ns]'),
          ('value', 'object')]

KeyValue = namedtuple('KeyValue', [dtype[0] for dtype in dtypes])


class AccumuloSource(base.DataSource):
    """Read data from Accumulo table.

    Parameters
    ----------
    table : str
        The database table that will act as source
    host : str
        The server hostname for the given table
    port : int
        The server port for the given table
    username : str
        The username used to connect to the Accumulo cluster
    password : str
        The password used to connect to the Accumulo cluster
    """
    name = 'accumulo'
    container = 'dataframe'
    version = __version__
    partition_access = False

    def __init__(self, table, host="localhost", port=42424, username="root",
                 password="secret", metadata=None):
        self._table = table
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._client = None

        super(AccumuloSource, self).__init__(metadata=metadata)

    def _get_schema(self):
        return base.Schema(datashape=None,
                           dtype=dtypes,
                           shape=(None, len(dtypes)),
                           npartitions=1,
                           extra_metadata={})

    def _get_partition(self, i):
        import pandas as pd
        if self._client is None:
            from .accumulo import Accumulo
            self._client = Accumulo(self._host,
                                    self._port,
                                    self._username,
                                    self._password)

        data = []
        scanner = self._client.create_scanner(self._table)

        while True:
            chunk = self._client.nextk(scanner)
            for entry in chunk.results:
                kv = KeyValue(entry.key.row,
                              entry.key.colFamily,
                              entry.key.colQualifier,
                              entry.key.colVisibility,
                              entry.key.timestamp,
                              entry.value)
                data.append(kv)
            if not chunk.more:
                break

        df = pd.DataFrame(data, columns=KeyValue._fields)
        return df.astype(dtype=OrderedDict(dtypes))

    def _close(self):
        self._client = None
