# PyDtLogDaemon
Python implementation of a log monitoring tool, used to send events to Dynatrace when specific patterns are detected in new log entries

## prerequisites
- python 2.7

## install
Get the following files and copy them to a target folder in the system hosting the log to monitor:
- LogDaemon.py
- config.properties
- requirements.txt

Specify parameter values in config.properties

## usage
In the target folder, execute the following command to start monitoring:

>    python LogDaemon.py

