#!/bin/sh

echo "Insert Chad's messages"
curl -X POST -H "Content-Type: application/json" -d '@./test/chad_msg1.json' http://localhost:80/chat
sleep 2
curl -X POST -H "Content-Type: application/json" -d '@./test/chad_msg2.json' http://localhost:80/chat
sleep 2
curl -X POST -H "Content-Type: application/json" -d '@./test/chad_msg3.json' http://localhost:80/chat
