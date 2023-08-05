Overview
========

Provides functions to read objects from Cloud Object Storage as a stream
and submit tuples to create objects in Cloud Object Storage.

`IBM® Cloud Object Storage <https://www.ibm.com/cloud/object-storage>`_ is a IBM Cloud service. Cloud Object Storage (COS) makes it possible to store practically limitless amounts of data, simply and cost effectively. It is commonly used for data archiving and backup, web and mobile applications, and as scalable, persistent storage for analytics.

Credentials
===========

Cloud Object Storage credentials are defined using a Streams application configuration.

By default an application configuration named `cos` is used,
a different configuration can be specified using the ``credentials``
parameter to :py:func:`write`, :py:func:`write_parquet`, :py:func:`scan` or :py:func:`read`.

The application configuration must contain the property ``cos.creds`` with a value of the raw Cloud Object Storage credentials JSON.

Sample
======

A simple hello world example of a Streams application writing string messages to
an object. Scan for created object on COS and read the content.::

    from streamsx.topology.topology import Topology
    from streamsx.topology.schema import CommonSchema
    from streamsx.topology.context import submit
    import streamsx.objectstorage as cos

    topo = Topology('ObjectStorageHelloWorld')

    to_cos = topo.source(['Hello', 'World!'])
    to_cos = to_cos.as_string()

    # Write a stream to COS using streamsx-py-sample bucket and sample_object.txt object name
    cos.write(to_cos, bucket='streamsx-py-sample', objectName='/sample/hw%OBJECTNUM.txt')

    scanned = cos.scan(topo, bucket='streamsx-py-sample', directory='/sample')

    # read text file line by line
    sch = 'tuple<rstring line>'
    r = cos.read(scanned, schema=sch, bucket='streamsx-py-sample')

    # print each line (tuple)
    r.print()

    submit('STREAMING_ANALYTICS_SERVICE', topo)

Documentation
=============

* `streamsx.objectstorage package documentation <http://streamsxobjectstorage.readthedocs.io/en/pypackage/>`_


