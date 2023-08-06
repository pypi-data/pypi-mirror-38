import pytest

import intake_accumulo as accumulo

from .utils import verify_datasource_interface


@pytest.fixture(scope="module")
def proxy():
    from intake_accumulo.accumulo import Accumulo

    from .utils import start_proxy, stop_proxy

    name, local_port = start_proxy()

    client = Accumulo("localhost", local_port)

    table = "test"
    if not client.table_exists(table):
        client.create_table(table)

    for num in range(0, 10):
        key = b"row_%d" % num
        client.update_and_flush(table, key, family=b"cf1", qualifier=b"cq1",
                                value=b"%d" % num)
        client.update_and_flush(table, key, family=b"cf2", qualifier=b"cq2",
                                value=b"%d" % num)

    try:
        yield local_port
    finally:
        client.close()
        stop_proxy(name)


def test_open(proxy):
    src = accumulo.AccumuloSource("test", port=proxy)
    assert src.container == 'dataframe'
    assert src.description is None
    verify_datasource_interface(src)


def test_discover(proxy):
    src = accumulo.AccumuloSource("test", port=proxy)
    info = src.discover()
    assert info['shape'] == (None, 6)
    assert info['npartitions'] == 1


def test_read(proxy):
    src = accumulo.AccumuloSource("test", port=proxy)
    df = src.read()
    assert len(df) == 20


def test_close(proxy):
    src = accumulo.AccumuloSource("test", port=proxy)
    original_df = src.read()

    src.close()

    # Verify client connection is closed
    assert src._client is None

    # Can reopen after close
    df = src.read()

    assert original_df.equals(df)
