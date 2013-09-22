Welcome to Python Test utils documentation!
===========================================

Python test utils is a collection of different functions and classes which make
writing integration tests easier.

Installation
============

Latest stable version can be installed from PyPi using pip:

.. sourcecode:: bash

    pip install test-utils

API Documentation
=================

For API documentation, please see the :doc:`API Documentation page </api>`.

Process Runner classes
======================

ProcessRunner allows you to manage a long running process which needs to run
during your test process execution.

Process runner does this in three steps:

1. Spawn a process before running the tests
2. Wait for the process to come online
3. Run the tests
4. Stop the managed process

This long running process can be an API server, database, Twisted service or any
other long running process.

TCPProcessRunner class
----------------------

TCPProcessRunner allows you to manage a long running process which exposes a
TCP interface. It detects if a process is running by connecting to the
specified IP and port.

Example usage
~~~~~~~~~~~~~

.. literalinclude:: /examples/tcp_process_runner.py
   :language: python
   :emphasize-lines: 56-68

This example shows how :class:`TCPProcessRunner` can be used in the
``TestCommand`` in your ``setup.py`` file. It is used to start a mock
API server which runs for the whole duration of your test suite run.

Keep in mind that you need to call
:func:`test_utils.process_runners.TCPProcessRunner.setUp` function. This
function is responsible for starting the managed process and waiting for it
to come online.

For a real-life example you can have a look at `python-yubico-client`_
`setup.py file`_. In this case, ProcessRunner is used to spawn multiple
mock API servers.

.. _`python-yubico-client`: https://github.com/Kami/python-yubico-client
.. _`setup.py file`: https://github.com/Kami/python-yubico-client/blob/1786926caf86e45155d40aae7d598d409ed184a3/setup.py#L36
