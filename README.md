# Network Engineering 2
For the NE2 course we we're given the assignment to build a Network Intrusion Detection System (IDS) from scratch in Python.
## Setup
* Create database
```mariadb
CREATE DATABASE 'ne2-nids';
```
* Create table
```mariadb
CREATE TABLE `ne2-nids`.`sniffer` (
  `id` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp(),
  `src_mac` varchar(17) NOT NULL,
  `dest_mac` varchar(17) NOT NULL,
  `protocol` int(11) NOT NULL,
  `version` int(11) NOT NULL,
  `header_length` int(11) NOT NULL,
  `ttl` int(11) NOT NULL,
  `ip_protocol` int(11) NOT NULL,
  `src_ip` varchar(15) NOT NULL,
  `dest_ip` varchar(15) NOT NULL,
  `udp_src_port` int(11) NOT NULL,
  `udp_dest_port` int(11) NOT NULL,
  `udp_length` int(11) NOT NULL,
  `data` mediumtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
ALTER TABLE `sniffer`
ADD PRIMARY KEY (`id`);
ALTER TABLE `sniffer`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
``` 
* Edit configuration in db.py accordingly
```python
host="localhost"
user="root"
passwd="appelflap"
database="ne2-nids"
```
   
## Requirements
### Detector running on Windows, Mac, Linux or Rpi:

* That captures network packets from a WIFI-network or a ethernet-network (it is
capable of capturing from both type of networks!).
* Only UDP and TCP packets are recorded; non IP packets are dropped.
* For each connection (identified by one signature as described below), it records the
number of data and packages in either direction.
* The signature is defined by a five tuple (src-ip-addr, src-ip-port, dst-ip-addr,
dst-ip-port and protocol UDP / TCP).
For example: 127.0.0.1:5723:127.0.0.1:22:TCP (an ssh connection)
* The detector captures in time-intervals. Each interval, all counters are reset and at
the end of the interval the information for that interval is send to a collector-process
as a JSON-structure. Besides the measurements, this JSON-structure contains the
start and the end of the interval as well as an ID of the Detector. Timestamps are
UTC based and the time offset is also in the JSON-structure. An example JSON text
is shown below.
* The communication between the Detector and Collector is REST-based and
secured.
* The program has command-line arguments to specify the network-interface, the
interval time (typically 1-5 minutes) and the address of the collector.
* The detector runs as a deamon.
* On a TERM-signal it stops capturing and sends the last measurement to the
collector.
* If the connection the the Collector couldn’t be made the measurement is discarded
and the next interval is started.
* If capturing continues during the transmission to the Collector, this is considered as
a plus, but isn’t required.
* It must be possible to run two Detectors on the same machine, one detecting the
WIFI-network, another one the ethernet-network.

### Collector:

* The collector can receive traffic-information from several Detectors.
* The information is stored persistently (file of database) and can be queried.
* Queries consists of the following parameters
    * Selection
        * Interval, the returned information must have overlap with this interval
        * Signature, “<src-addr>:<src-port>:<dst-addr>:<dest-port>:<proto>”
        if one of the fields is empty, there is no filter on that field. A signature
        of “” is considered as no filtering at all
        * DetectorId, a comma-separated list of DetectorIds. Only traffic
        information from those Detectors is returned.

    * Aggregation
        * Interval, the measurements are collapsed in intervals of given size.
        This size is greater than the measurement interval.
        * src-addr, dst-addr, src-port, dst-port, proto. If any is present the
        measurements are aggregated with respect of those fields. So if only
        “src-addr” and “proto” are given the total traffic (packets and bytes) are
        given of each ip-addr and protocol.
#### This could be the result of a query:
* Selection:
    * Interval: 09:30 .. 17:30
    * Signature “:22::22:TCP”
    * DectectorId: “”
* Aggregation:
    * Interval: 3600 (secs)
    * Fields: src-addr,proto
    
### Dashboard
* The dashboard is a web-based GUI
* The dashboard offers insight in the traffic information.
* It queries the collector and display the information, preferable with numbers and
graphics.
* It gives an interface to the Selection and Aggregate options of the Collector query.
* It must be possible to display information of several Detectors over a larger time
interval.
