.. image:: https://travis-ci.org/enyx-opensource/yassh.svg?branch=master
   :target: https://travis-ci.org/enyx-opensource/yassh
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/enyx-opensource/yassh/badge.svg?branch=master
   :target: https://coveralls.io/github/enyx-opensource/yassh?branch=master
   :alt: Coverage Status

.. image:: https://codeclimate.com/github/enyx-opensource/yassh/badges/gpa.svg
   :target: https://codeclimate.com/github/enyx-opensource/yassh
   :alt: Code Climate

.. image:: https://codeclimate.com/github/enyx-opensource/yassh/badges/issue_count.svg
   :target: https://codeclimate.com/github/enyx-opensource/yassh
   :alt: Issue Count

.. image:: https://readthedocs.org/projects/yassh/badge/?version=latest
   :target: http://yassh.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

yassh
=====

Yassh is a python library used to run
asynchronous, dependent remote and local tasks.

Usage
-----

.. code-block:: python

    import logging
    from yassh import Reactor, RemoteRun, RemoteConfiguration, LocalRun

    logging.basicConfig(level=logging.DEBUG)

    # Create a remote ; only host parameter is mandatory
    remote = RemoteConfiguration(host='localhost', username='user')

    # ssh_config(5) options can be set in RemoteConfiguration object
    remote.set('Compression', 'yes')
    remote.set('CompressionLevel', '9')

    r = Reactor()
    c1 = RemoteRun(r, remote, 'sleep 5')
    c2 = LocalRun(r, 'echo ok')
    c3 = RemoteRun(r, remote, 'echo "finished" && sleep 1')


    def start_c2(run):
        # Start cmd2 when cmd1 complete successfully
        if run.result == 0:
            c2.start()
    c1.register_exit_monitor(start_c2)


    def start_c3(run):
        # Start cmd3 when cmd2 complete
        c3.start()
    c2.register_monitor(u'ok', start_c3)


    def on_c3_finished(run):
        # Print dummy message when c3 is near terminaison
        print('c3 almost finished')
    c3.register_monitor(u'finished', on_c3_finished)


    # Start first task
    c1.start()


    # Infinite
    timeout = -1
    while r.run(timeout) > 0:
            pass

Installation
------------

To install latest release::

    pip install yassh

To install latest code::

    pip install git+https://github.com/enyx-opensource/yassh.git

Testing
-------

Run from project root::

    behave

License
-------
MIT License (see LICENSE)

