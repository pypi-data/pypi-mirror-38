import avro
import fastavro
import struct
import io
import avro.io
from avro import schema as avroschema
import json
import primed_avro.util


MAGIC_BYTE = 0


class AvroDecoder:
    def __init__(self, schema):
        parsed_schema = avroschema.Parse(json.dumps(schema))
        self._writer = avro.io.DatumWriter(parsed_schema)

    def decode(self, record):
        writer_schema_obj = None  # TODO: where to obtain this?
        reader_schema_obj = None  # TODO: where to obtain this?

        if message is None:
            return None

        if len(message) <= 5:
            raise SerializerError("message is too small to decode")

        avro_reader = avro.io.DatumReader(writer_schema_obj, reader_schema_obj)

        with primed_avro.util.ContextStringIO(message) as payload:
            magic, schema_id = struct.unpack(">bI", payload.read(5))
            if magic != MAGIC_BYTE:
                raise SerializerError("message does not start with magic byte")

            return avro_reader.read(avro.io.BinaryDecoder(payload))


class FastAvroDecoder:
    def __init__(self, schema):
        pass

    def decode(self, schema_id, record):
        pass


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
