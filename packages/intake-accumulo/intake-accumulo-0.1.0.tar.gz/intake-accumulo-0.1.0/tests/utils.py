import logging
import shlex
import subprocess
import time
import uuid

logger = logging.getLogger()


def verify_plugin_interface(plugin):
    """Assert types of plugin attributes."""
    assert isinstance(plugin.version, str)
    assert isinstance(plugin.container, str)
    assert isinstance(plugin.partition_access, bool)


def verify_datasource_interface(source):
    """Assert presence of datasource attributes."""
    for attr in ['container', 'description', 'datashape', 'dtype', 'shape',
                 'npartitions', 'metadata']:
        assert hasattr(source, attr)

    for method in ['discover', 'read', 'read_chunked', 'read_partition',
                   'to_dask', 'close']:
        assert hasattr(source, method)


def start_proxy():
    """Start an Accumulo proxy server.

    This starts a Docker container running Accumulo proxy server. Pipe the
    output of the container process to stdout, until the database is ready to
    accept connections. This container may be stopped with ``stop_proxy()``.

    Returns the container name and local proxy port.
    """
    name = uuid.uuid4().hex

    docker_run = (
        "docker run --rm --name " + name + " --publish 42424 "
        "jbcrail/accumulo-proxy:1.5.2"
        )

    cmd = shlex.split(docker_run)

    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         universal_newlines=True)

    while True:
        output = p.stdout.readline()
        logger.debug(output.rstrip())

        # If the process exited, raise exception
        if p.poll():
            raise Exception("Accumulo proxy server failed to start up properly")

        # Detect when initialization has happened, so we can stop waiting when
        # the proxy server is accepting connections.
        if "Starting Thrift proxy" in output:
            break

    time.sleep(2)

    # Return the local port to which Docker mapped Accumulo proxy server
    docker_inspect = (
        "docker inspect " + name + " --format "
        "'{{range $p, $conf := .NetworkSettings.Ports}} "
        "{{if $conf}} {{(index $conf 0).HostPort}} {{end}} "
        "{{end}}'"
        )

    cmd = shlex.split(docker_inspect)
    port = subprocess.check_output(cmd, universal_newlines=True).strip()

    return name, int(port)


def stop_proxy(name, let_fail=False):
    """Stop an Accumulo proxy server.

    This attempts to shut down the container started by ``start_proxy()``.
    Raise an exception if this operation fails, unless ``let_fail`` evaluates
    to True.
    """
    try:
        logger.debug("Stopping Accumulo proxy server...")
        subprocess.check_output("docker kill " + name, shell=True)
    except subprocess.CalledProcessError:
        if not let_fail:
            raise
