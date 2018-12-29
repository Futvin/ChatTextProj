#!/bin/sh

echo "Insert bad messages"
curl -X POST -H "Content-Type: application/json" -d '@./test/bad_msg1.json' http://localhost:80/chat
curl -X POST -H "Content-Type: application/json" -d '@./test/bad_msg2.json' http://localhost:80/chat
