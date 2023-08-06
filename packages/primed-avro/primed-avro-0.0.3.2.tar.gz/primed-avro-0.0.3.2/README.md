primed-avro
===============================

version number: 0.0.1
author: Matthijs van der Kroon

Overview
--------

A python package that provides Avro serialisation and deserialisation compatible with the Confluent Schema Registry.

WARNING: python2.7 not supported

Installation / Usage
--------------------

To install use pip:

    $ pip install primed_avro


Or clone the repo:

    $ git clone https://gitlab.com/primedio/primed-avro
    $ python setup.py install
    
Contributing
------------

TBD

Example
-------

	from primed_avro.writer import Writer
	from primed_avro.registry import ConfluentSchemaRegistryClient


	csr = ConfluentSchemaRegistryClient(url="http://localhost:8081")
	schemaMeta = csr.get_schema(subject=topic)
	writer = Writer(schema=schemaMeta.schema)
