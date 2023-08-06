from thrift.protocol import TCompactProtocol
from thrift.transport import TSocket, TTransport

from .proxy import AccumuloProxy
from .proxy.ttypes import ColumnUpdate, TimeType


class Accumulo(object):
    def __init__(self, host="localhost", port=42424, user="root", password="secret"):
        super(Accumulo, self).__init__()
        self.transport = TTransport.TFramedTransport(TSocket.TSocket(host, port))
        self.protocol = TCompactProtocol.TCompactProtocol(self.transport)
        self.client = AccumuloProxy.Client(self.protocol)

        self.transport.open()
        self.login = self.client.login(user, {"password": password})

    def close(self):
        self.transport.close()

    def table_exists(self, table):
        return self.client.tableExists(self.login, table)

    def create_table(self, table):
        self.client.createTable(self.login, table, True, TimeType.MILLIS)

    def update_and_flush(self, table, row, family=None, qualifier=None, visibility=None, timestamp=None, value=None):
        mutation = ColumnUpdate(colFamily=family,
                                colQualifier=qualifier,
                                colVisibility=visibility,
                                timestamp=timestamp,
                                value=value)
        self.client.updateAndFlush(self.login, table, {row: [mutation]})

    def create_scanner(self, table):
        return self.client.createScanner(self.login, table, None)

    def nextk(self, scanner, batchsize=10):
        return self.client.nextK(scanner, batchsize)
