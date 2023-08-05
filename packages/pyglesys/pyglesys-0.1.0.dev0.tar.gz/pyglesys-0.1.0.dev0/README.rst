py.glesys
=========

py.glesys is a Python wrapper around the GleSYS API. 


Installing
----------

Install using `pip <https://pip.pypa.io/en/stable/>`_::

    $ pip install pyglesys


Example Usage
-------------

.. code-block:: python

    import glesys

    gs = glesys.Glesys('account_number', 'api_key')
    servers = gs.server.list()
    print(servers)

.. code-block:: console

    $ python app.py
    [Server(id_="wps1234567", hostname="example.com", datacenter="Falkenberg", platform="VMware")]
