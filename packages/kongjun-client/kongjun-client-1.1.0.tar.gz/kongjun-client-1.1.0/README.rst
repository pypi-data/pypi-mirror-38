.. image:: https://img.shields.io/travis/wickedasp/eureka/master.svg?style=flat-square
    :target: https://travis-ci.org/wickedasp/eureka

.. image:: https://img.shields.io/pypi/l/wasp-eureka.svg?style=flat-square
    :target: https://github.com/wickedasp/eureka/blob/master/LICENSE

.. image:: https://img.shields.io/pypi/v/wasp-eureka.svg?style=flat-square
    :target: https://pypi.python.org/pypi/wasp-eureka

.. image:: https://img.shields.io/pypi/status/wasp-eureka.svg?style=flat-square
    :target: https://pypi.python.org/pypi/wasp-eureka

.. image:: https://img.shields.io/pypi/pyversions/wasp-eureka.svg?style=flat-square
    :target: https://pypi.python.org/pypi/wasp-eureka

WASP Eureka
===========

Asynchronous Naive Eureka client for the Netflix OSS/Spring Cloud bundled eureka stack.

Installation
------------

Note: this supports Python 3.5+

.. code-block:: bash

    $ pip install wasp-eureka

If you want to just run it standalone, include those dependencies:

.. code-block:: bash

    $ pip install wasp-eureka[standalone]

Usage
-----

The surface area of this module is pretty small, effectively you just need to care about the ``wasp_eureka.EurekaClient`` class and its methods:

.. code-block:: python

    import asyncio
    
    from wasp_eureka import EurekaClient
    
    # no spaces or underscores, this needs to be url-friendly
    app_name = 'test-app'
    
    port = 8080
    # This needs to be an IP accessible by anyone that
    # may want to discover, connect and/or use your service.
    ip = '127.0.0.1'
    my_eureka_url = 'https://service-discovery.mycompany.com/eureka'
    loop = asyncio.get_event_loop()
    
    eureka = EurekaClient(app_name, port, ip, eureka_url=my_eureka_url,
                          loop=loop)
    
    async def main():
        # Presuming you want your service to be available via eureka
        result = await eureka.register()
        assert result, 'Unable to register'
        
        # You need to provide a heartbeat to renew the lease,
        # otherwise the eureka server will expel the service.
        # The default is 90s, so any time <90s is ok
        while True:
            await asyncio.sleep(67)
            await eureka.renew()
    
    loop.run_until_complete(main())

Creating a Release
------------------

Bumpversion_ provides a simplified way to manage versioning, to check the dry run before running it:

.. code-block:: bash

    $ bumpversion [patch,minor,major] --dry-run --verbose

.. code-block:: bash

    $ bumpversion patch

.. _APScheduler: https://apscheduler.readthedocs.io/en/latest/
.. _Bumpversion: https://pypi.python.org/pypi/bumpversion
