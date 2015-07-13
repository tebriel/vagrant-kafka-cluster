# Kafka Cluster #

## Table of Contents ##

*  [Description](#description)
*  [Trying It Out](#trying-it-out)
*  [Kafka Manager](#kafka-manager)
*  [TODO](#todo)

## Description ##

This repo will set up 6 boxes
*  3 Zookeeper Nodes
*  3 Kafka Nodes

The IP Address Ranges will be
*  `192.168.33.1{1,2,3}` for Zookeeper
*  `192.168.33.2{1,2,3}` for Kafka

Kafka-Manager will be stood up on zookeeper1 and can be accessed via
[zookeeper1:9000](http://192.168.33.11:9000)

Each box is allocated `1GB` of RAM. Make sure your system can handle 6x1GB
Vagrants.

Kafka and Zookeeper are all started with a max heap of `512m`. This should
prevent them from knocking the box over, and should give them enough headroom
to handle most things that you throw at it.

I've locked down the versions as much as possible, check the cookbooks to see
what versions of the packages we are downloading.

## Trying It Out ##

There's a folder called `./test_scripts` which contains a producer and a
consumer. This will send messages to one kafka node and listen to another. The
consumer (`sample_consumer_stdout.py`) will listen forever, whereas the
producer (`sample_producer.py`) will push all of its messages onto Kafka and
then exit.

These scripts are hard-coded to use the `credit_cards` topic in Kafka. If it
doesn't exist, it will create it. The defaults for creating topics involve a
replication factor of 3 and a partition factor of 1. This means if the kakfa
node holding your data falls over, the other two also have it, so you have
pretty strong redundancy. Partition factor says split the data across N nodes,
right now we'll just let every node hold all of the data.

To run these scripts, first install the python requirements:

```sh
pip install -r requirements.txt
```

Then run the scripts in this order, each in its own terminal:

```sh
./sample_consumer_stdout.py
./sample_producer.py
```

The terminal with stdout will display the messages sent across Kafka once it
reads them off the queue.

As a note, these scripts are using [Avro](https://avro.apache.org/) to
serialize and deserialize the messages that are sent across Kafka. This ensures
data integrity as we will always make sure the data has been formatted
correctly before it heads down the queue. You'll have to define a new schema
(in the schemas folder) if you want to push a different type of data across the
queue.

## Kafka-Manager ##

On [zookeeper1:9000](http://192.168.33.11:9000), kafka-manager is running. On
initital startup, you'll need to configure it. You'll need to add a cluster,
with these settings:

```yaml
name: dev # doesn't really matter
zookeeper_hosts: zookeeper1:2181,zookeeper2:2181,zookeeper3:2181
Kafka_Version: 0.8.2.1
Enable_JMX: true
```

I couldn't find a PPA hosting kafka-manager's deb, so I had to bundle it here.
Building it in a RAM limited vagrant takes forever, committing 50M of debian
makes me feel dirty, but saving time was more important.

## Todo ##

*  Firewall Rules - Don't just purge ufw
*  Better Configuration - More JSON config so that this can be deployed
   somewhere
*  Some way to daemonize kafka better, there's no debian package that I found,
   so other than running it -daemon, there doesn't seeem to be a standard way
   to stand it up.
