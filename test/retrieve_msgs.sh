#!/bin/sh

echo "Get all chats by ID"
for id in `seq 1 10` ; do
  curl -X GET http://localhost:80/chat/$id
  echo ""
done

echo ""
echo "Get all of Aaron's Chats"
curl -X GET http://localhost:80/chats/Aaron
echo ""

echo ""
echo "Get all of Chad's Chats"
curl -X GET http://localhost:80/chats/Chad
echo ""

echo ""
echo "Get all of Bad Chats"
curl -X GET http://localhost:80/chats/Bad
echo ""
