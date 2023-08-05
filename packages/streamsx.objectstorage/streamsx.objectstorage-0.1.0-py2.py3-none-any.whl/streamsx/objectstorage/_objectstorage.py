# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2018

import datetime

import streamsx.spl.op
import streamsx.spl.types
from streamsx.topology.schema import StreamSchema
from streamsx.spl.types import rstring

SCAN_SCHEMA = StreamSchema('tuple<rstring objectname>')
"""Structured schema containing an object name.

``'tuple<rstring objectname>'``
"""

def scan(topology, bucket, pattern='.*', directory='/', endpoint='s3-api.us-geo.objectstorage.softlayer.net', credentials=None, vmArg=None, name=None):
    """Scan a directory in a bucket for object names.

    Scans an object storage directory and emits the names of new or modified objects that are found in the directory.

    Example scanning a directory ``/sample`` for objects matching the pattern::

        import streamsx.objectstorage as cos

        scans = cos.scan(topo, bucket='your-bucket-name', directory='/sample', pattern='SAMPLE_[0-9]*\\.ascii\\.text$')

    Args:
        topology(Topology): Topology to contain the returned stream.
        bucket(str): Bucket name. Bucket must have been created in your Cloud Object Storage service before using this function.
        pattern(str): Limits the object names that are listed to the names that match the specified regular expression.
        directory(str): Specifies the name of the directory to be scanned. Any subdirectories are not scanned.
        endpoint(str): Endpoint for Cloud Object Storage. When not set the endpoint ``s3-api.us-geo.objectstorage.softlayer.net`` is used.
        credentials(str): Name of the application configuration containing the credentials for Cloud Object Storage. When set to ``None`` the application configuration ``cos`` is used.
        vmArg: Arbitrary JVM arguments can be passed using vmArg.        
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        Stream: Object names stream with schema :py:const:`SCAN_SCHEMA`.
    """

    _op = ObjectStorageScan(topology, SCAN_SCHEMA, pattern=pattern, directory=directory, endpoint=endpoint, appConfigName=credentials, vmArg=vmArg, name=name)
    _op.params['objectStorageURI'] = 's3a://'+bucket
    return _op.outputs[0]


def read(stream, schema, bucket, endpoint='s3-api.us-geo.objectstorage.softlayer.net', credentials=None, vmArg=None, name=None):
    """Read an object in a bucket.

    Reads the object specified in the input stream and emits content of the object.

    Args:
        stream(Stream): Stream of tuples with object names to be read.
        schema(StreamSchema): Schema of the returned stream, for example, ``'tuple<rstring lines>'``.
        bucket(str): Bucket name. Bucket must have been created in your Cloud Object Storage service before using this function.
        endpoint(str): Endpoint for Cloud Object Storage. When not set the endpoint ``s3-api.us-geo.objectstorage.softlayer.net`` is used.
        credentials(str): Name of the application configuration containing the credentials for Cloud Object Storage. When set to ``None`` the application configuration ``cos`` is used.
        vmArg: Arbitrary JVM arguments can be passed using vmArg.        
        name(str): Sink name in the Streams context, defaults to a generated name.

    Returns:
        Stream: Object content line by line.
    """

    _op = ObjectStorageSource(stream, schema, endpoint=endpoint, appConfigName=credentials, vmArg=vmArg, name=name)
    _op.params['objectStorageURI'] = 's3a://'+bucket
    return _op.outputs[0]


def write(stream, bucket, objectName, endpoint='s3-api.us-geo.objectstorage.softlayer.net', timePerObject=10.0, credentials=None, vmArg=None, name=None):
    """Write strings to an object.

    Adds a COS-Writer where each tuple on `stream` is
    written into an object.

    Args:
        stream(Stream): Stream of tuples to be written to an object. Expects one attribute of type ``rstring`` in the input stream.
        object(str): Name of the object to be created in your bucket. For example, ``SAMPLE_%OBJECTNUM.text``
        bucket(str): Bucket name. Bucket must have been created in your Cloud Object Storage service before using this function.
        endpoint(str): Endpoint for Cloud Object Storage. When not set the endpoint ``s3-api.us-geo.objectstorage.softlayer.net`` is used.
        timePerObject: Specifies the approximate time, in seconds, after which the current output object is closed and a new object is opened for writing.
        credentials(str): Name of the application configuration containing the credentials for Cloud Object Storage. When set to ``None`` the application configuration ``cos`` is used.
        vmArg: Arbitrary JVM arguments can be passed using vmArg.
        name(str): Sink name in the Streams context, defaults to a generated name.
    """

    _op = ObjectStorageSink(stream, objectName=objectName, endpoint=endpoint, appConfigName=credentials, vmArg=vmArg, name=name)
    _op.params['storageFormat'] = 'raw'
    _op.params['objectStorageURI'] = 's3a://'+bucket
    _op.params['timePerObject'] = timePerObject


def write_parquet(stream, bucket, objectName, endpoint='s3-api.us-geo.objectstorage.softlayer.net', timePerObject=10.0, credentials=None, vmArg=None, name=None):
    """Create objects in parquet format.

    Adds a COS-Writer where each tuple on `stream` is
    written into an object in parquet format.

    Args:
        stream(Stream): Stream of tuples to be written to an object. Supports ``streamsx.topology.schema.StreamSchema`` (schema for a structured stream) as input. Attributes are mapped to parquet columns.
        object(str): Name of the object to be created in your bucket. For example, ``SAMPLE_%OBJECTNUM.parquet``
        bucket(str): Bucket name. Bucket must have been created in your Cloud Object Storage service before using this function.
        endpoint(str): Endpoint for Cloud Object Storage. When not set the endpoint ``s3-api.us-geo.objectstorage.softlayer.net`` is used.
        timePerObject: Specifies the approximate time, in seconds, after which the current output object is closed and a new object is opened for writing.
        credentials(str): Name of the application configuration containing the credentials for Cloud Object Storage. When set to ``None`` the application configuration ``cos`` is used.
        vmArg: Arbitrary JVM arguments can be passed using vmArg.
        name(str): Sink name in the Streams context, defaults to a generated name.
    """

    _op = ObjectStorageSink(stream, objectName=objectName, endpoint=endpoint, appConfigName=credentials, vmArg=vmArg, name=name)
    _op.params['storageFormat'] = 'parquet'
    _op.params['parquetCompression'] = 'SNAPPY'
    _op.params['parquetEnableDict'] = True
    _op.params['objectStorageURI'] = 's3a://'+bucket
    _op.params['timePerObject'] = timePerObject


class ObjectStorageSink(streamsx.spl.op.Invoke):
    def __init__(self, stream, schema=None, vmArg=None, appConfigName=None, bytesPerObject=None, closeOnPunct=None, dataAttribute=None, encoding=None, endpoint=None, headerRow=None, objectName=None, objectNameAttribute=None, objectStorageURI=None, parquetBlockSize=None, parquetCompression=None, parquetDictPageSize=None, parquetEnableDict=None, parquetEnableSchemaValidation=None, parquetPageSize=None, parquetWriterVersion=None, partitionValueAttributes=None, skipPartitionAttributes=None, storageFormat=None, timeFormat=None, timePerObject=None, tuplesPerObject=None, name=None):
        topology = stream.topology
        kind="com.ibm.streamsx.objectstorage::ObjectStorageSink"
        inputs=stream
        schemas=schema
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if appConfigName is not None:
            params['appConfigName'] = appConfigName
        if bytesPerObject is not None:
            params['bytesPerObject'] = bytesPerObject
        if closeOnPunct is not None:
            params['closeOnPunct'] = closeOnPunct
        if dataAttribute is not None:
            params['dataAttribute'] = dataAttribute
        if encoding is not None:
            params['encoding'] = encoding
        if endpoint is not None:
            params['endpoint'] = endpoint
        if headerRow is not None:
            params['headerRow'] = headerRow
        if objectName is not None:
            params['objectName'] = objectName
        if objectNameAttribute is not None:
            params['objectNameAttribute'] = objectNameAttribute
        if objectStorageURI is not None:
            params['objectStorageURI'] = objectStorageURI
        if parquetBlockSize is not None:
            params['parquetBlockSize'] = parquetBlockSize
        if parquetCompression is not None:
            params['parquetCompression'] = parquetCompression
        if parquetDictPageSize is not None:
            params['parquetDictPageSize'] = parquetDictPageSize
        if parquetEnableDict is not None:
            params['parquetEnableDict'] = parquetEnableDict
        if parquetEnableSchemaValidation is not None:
            params['parquetEnableSchemaValidation'] = parquetEnableSchemaValidation
        if parquetPageSize is not None:
            params['parquetPageSize'] = parquetPageSize
        if parquetWriterVersion is not None:
            params['parquetWriterVersion'] = parquetWriterVersion
        if partitionValueAttributes is not None:
            params['partitionValueAttributes'] = partitionValueAttributes
        if skipPartitionAttributes is not None:
            params['skipPartitionAttributes'] = skipPartitionAttributes
        if storageFormat is not None:
            params['storageFormat'] = storageFormat
        if timeFormat is not None:
            params['timeFormat'] = timeFormat
        if timePerObject is not None:
            params['timePerObject'] = timePerObject
        if tuplesPerObject is not None:
            params['tuplesPerObject'] = tuplesPerObject

        super(ObjectStorageSink, self).__init__(topology,kind,inputs,schema,params,name)


class ObjectStorageScan(streamsx.spl.op.Source):
    def __init__(self, topology, schema, directory, pattern, vmArg=None, appConfigName=None, endpoint=None, objectStorageURI=None, initDelay=None, sleepTime=None, strictMode=None, name=None):
        kind="com.ibm.streamsx.objectstorage::ObjectStorageScan"
        inputs=None
        schemas=schema
        params = dict()
        params['directory'] = directory
        if vmArg is not None:
            params['vmArg'] = vmArg
        if appConfigName is not None:
            params['appConfigName'] = appConfigName
        if endpoint is not None:
            params['endpoint'] = endpoint
        if objectStorageURI is not None:
            params['objectStorageURI'] = objectStorageURI
        if initDelay is not None:
            params['initDelay'] = initDelay
        if sleepTime is not None:
            params['sleepTime'] = sleepTime
        if pattern is not None:
            params['pattern'] = pattern
        if strictMode is not None:
            params['strictMode'] = strictMode

        super(ObjectStorageScan, self).__init__(topology,kind,schemas,params,name)


class ObjectStorageSource(streamsx.spl.op.Invoke):
    
    def __init__(self, stream, schema, vmArg=None, appConfigName=None, endpoint=None, objectStorageURI=None, blockSize=None, encoding=None, initDelay=None, name=None):
        kind="com.ibm.streamsx.objectstorage::ObjectStorageSource"
        topology = stream.topology
        inputs=stream
        params = dict()
        if vmArg is not None:
            params['vmArg'] = vmArg
        if appConfigName is not None:
            params['appConfigName'] = appConfigName
        if endpoint is not None:
            params['endpoint'] = endpoint
        if objectStorageURI is not None:
            params['objectStorageURI'] = objectStorageURI
        if blockSize is not None:
            params['blockSize'] = initDelay
        if encoding is not None:
            params['encoding'] = sleepTime
        if initDelay is not None:
            params['initDelay'] = initDelay
        super(ObjectStorageSource, self).__init__(topology,kind,inputs,schema,params,name)


