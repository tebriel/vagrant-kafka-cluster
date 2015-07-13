#!/usr/bin/env python

"""
This file simulates the Reputation API as it receives consortium data messages
It will encode the message, and send it to Kafka to be read by downstream
consumers
"""

import json
import os
import time
import io

import avro.schema
import avro.io

from kafka import SimpleProducer, KafkaClient
from kafka.common import LeaderNotAvailableError

TOPIC = b'credit_cards'


def connect(ip):
    """Create our Kafka client
    """
    return KafkaClient("%s:9092" % (ip))


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


def produce(client, messages):
    schema = avro.schema.parse(open("./schemas/sample_schema.avsc").read())
    writer = avro.io.DatumWriter(schema)
    # To wait for acknowledgements
    # ACK_AFTER_LOCAL_WRITE : server will wait till the data is written to
    #                         a local log before sending response
    # ACK_AFTER_CLUSTER_COMMIT : server will block until the message is
    #                            committed by all in sync replicas before
    #                            sending a response
    producer = SimpleProducer(client, async=False,
                              req_acks=SimpleProducer.ACK_AFTER_LOCAL_WRITE,
                              ack_timeout=2000,
                              sync_fail_on_error=False)

    message_num = 0

    # Iterate the sample data
    for datum in messages['data']:
        message = {
            'name': datum[0],
            'phone': datum[1],
            'pin': datum[2],
            'cc': datum[3],
        }

        bytes_writer = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytes_writer)
        writer.write(message, encoder)
        try:
            producer.send_messages(TOPIC, bytes_writer.getvalue())
        # Because we may not have ever set up kafka before, if our topic doesn't
        # exist, kafka will fail here, this should only fail once.
        except LeaderNotAvailableError:
            time.sleep(1)
            producer.send_messages(TOPIC, bytes_writer.getvalue())

        message_num += 1
        print("Sent message #%d" % (message_num))

if __name__ == '__main__':
    kafka_host = os.environ.get('KAFKA_HOST')
    if kafka_host is None:
        kafka_host = '192.168.33.22'
    # Read in our sample data
    with open('sample_data.json') as sample_file:
        sample_data = json.load(sample_file)

    topic_security(kafka_host)
    client = connect(kafka_host)
    produce(client, sample_data)
