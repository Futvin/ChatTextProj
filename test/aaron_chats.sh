#!/bin/sh

echo "Insert Aaron's messages"
curl -X POST -H "Content-Type: application/json" -d '@./test/aaron_msg1.json' http://localhost:80/chat
curl -X POST -H "Content-Type: application/json" -d '@./test/aaron_msg2.json' http://localhost:80/chat
