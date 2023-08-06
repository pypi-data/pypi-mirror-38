import avro
import fastavro
import struct
import io
import avro.io
from avro import schema as avroschema
import json
import primed_avro.util


MAGIC_BYTE = 0


class SerializerError(Exception):
    pass


class AvroDecoder:
    def __init__(self, schema):
        parsed_schema = avroschema.Parse(json.dumps(schema))
        self._writer = avro.io.DatumWriter(parsed_schema)

    def decode(self, record):
        writer_schema_obj = None  # TODO: where to obtain this?
        reader_schema_obj = None  # TODO: where to obtain this?

        if record is None:
            return None

        if len(record) <= 5:
            raise SerializerError("record is too small to decode")

        avro_reader = avro.io.DatumReader(writer_schema_obj, reader_schema_obj)

        with primed_avro.util.ContextStringIO(record) as payload:
            magic, schema_id = struct.unpack(">bI", payload.read(5))
            if magic != MAGIC_BYTE:
                raise SerializerError("record does not start with magic byte")

            return avro_reader.read(avro.io.BinaryDecoder(payload))


class FastAvroDecoder:
    def __init__(self, schema, schemaless=True):
        self.parsed_schema = fastavro.parse_schema(schema)
        self._decoder = fastavro.schemaless_reader if schemaless else fastavro.reader

    def decode(self, schema_id, record):

        with primed_avro.util.ContextStringIO(record[5:]) as buf:
            # magic, schema_id = struct.unpack(">bI", buf.read(5))
            # if magic != MAGIC_BYTE:
            #     raise SerializerError("record does not start with magic byte")

            return self._decoder(buf, self.parsed_schema)


class Decoder:
    """
    Allows the user to dynamically specify whether to use the
    FastAvro or regular Avro implementations
    """

    _classmap = {"fastavro": FastAvroDecoder, "avro": AvroDecoder}

    def __init__(self, schema, classname="fastavro"):
        # TODO: decoders not implemented yet
        raise NotImplemented
        return _classmap[classname](schema)
