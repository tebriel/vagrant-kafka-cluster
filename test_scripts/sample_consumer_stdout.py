#!/usr/bin/env python

"""
This file consumes from the kafka queue and prints it out to stdout
"""

import os
import io
import avro.schema
import avro.io
from kafka import KafkaConsumer, KafkaClient

TOPIC = b'credit_cards'


def connect(ip):
    """Creates our kafka consumer"""
    return KafkaConsumer(TOPIC,
                         bootstrap_servers=["%s:9092" % (ip)])


def topic_security(ip):
    """Ensures our topic exists

    If we're the first one online it won't exist, this will not be needed once
    we configure topics in the kafka configuration

    This will open a connection, create the topic, then close the connection

    **Issues**:
        - The Port is hardcoded

    :param ip: The IP of our Kafka Box
    :type ip: str
    """
    kafka = KafkaClient("%s:9092" % (ip))
    kafka.ensure_topic_exists(TOPIC)
    kafka.close()


def consume_and_sync(consumer):
    schema = avro.schema.parse(open("./schemas/sample_schema.avsc").read())
    num_seen = 0
    # Consumer yields every time we have a new message
    for message in consumer:
        num_seen += 1
        # It's an encoded bytestring, uncode it
        bytes_reader = io.BytesIO(message.value)
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(schema)
        consumed_message = reader.read(decoder)
        print("%d -- %s" % (num_seen, consumed_message))

if __name__ == '__main__':
    kafka_host = os.environ.get('KAFKA_HOST')
    if kafka_host is None:
        kafka_host = '192.168.33.22'
    topic_security(kafka_host)
    consumer = connect(kafka_host)
    consume_and_sync(consumer)
