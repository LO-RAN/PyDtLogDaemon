# PyDtLogDaemon
Python implementation of a log monitoring tool, used to send events to Dynatrace when specific patterns are detected in new log entries

## prerequisites
- python 3.6
- pip3 

## install
Get the following files and copy them to a target folder in the system hosting the log to monitor:
- LogDaemon.py
- config.properties
- requirements.txt

Specify parameter values in config.properties

In the target folder, execute the following command once to load required dependencies:

>    pip3 install -r requirements.txt

## usage
In the target folder, execute the following command to start monitoring:

>    python3 LogDaemon.py

