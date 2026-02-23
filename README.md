# Distributed Key-Value Store with Task Queue

A backend system built using Python socket programming that supports key-value storage with TTL expiration, background job processing, and monitoring.

## Features

- SET, GET, DELETE operations
- TTL (Time-To-Live) expiration
- Background worker task queue
- Job submission and status tracking
- Persistent JSON storage
- Multithreaded socket server
- Monitoring script

## Commands

SET key value [ttl]  
GET key  
DELETE key  
SUBMIT task  
STATUS job_id  

## Run

Server:
python server.py

Client:
python client.py

Monitor:
python monitor.py

## Tech Stack

Python  
Socket Programming  
Multithreading  
Queue System  

## Author

Bharadwaj Garre 

