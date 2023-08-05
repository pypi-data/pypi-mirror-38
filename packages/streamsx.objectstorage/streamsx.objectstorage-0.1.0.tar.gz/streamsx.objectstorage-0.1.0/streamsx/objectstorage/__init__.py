# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

"""
Overview
++++++++

`IBM® Cloud Object Storage <https://www.ibm.com/cloud/object-storage>`_ is a IBM Cloud service. Cloud Object Storage (COS) makes it possible to store practically limitless amounts of data, simply and cost effectively. It is commonly used for data archiving and backup, web and mobile applications, and as scalable, persistent storage for analytics.

This module allows a Streams application to create objects in parquet format :py:func:`write_parquet <write_parquet>` or
to write string messages with :py:func:`write <write>` from a stream
of tuples.
Objects can be listed with :py:func:`scan <scan>` and read with :py:func:`read <read>`.

Credentials
+++++++++++

Cloud Object Storage credentials are defined using a Streams application configuration.

By default an application configuration named `cos` is used,
a different configuration can be specified using the ``credentials``
parameter to :py:func:`write`, :py:func:`write_parquet`, :py:func:`scan` or :py:func:`read`.

The application configuration must contain the property ``cos.creds`` with a value of the raw Cloud Object Storage credentials JSON.

Sample
++++++

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

"""

__all__ = ['write_parquet', 'scan', 'read', 'write']
from streamsx.objectstorage._objectstorage import write_parquet, scan, read, write
