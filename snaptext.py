import json
import re
import redis
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, Response
from pymongo import MongoClient

## Applitation and Database Setup ##

app = Flask(__name__)

db_client = MongoClient("mongodb://mongo:27017")
chatdb = db_client.chatdb

cache = redis.Redis(host='redis', port=6379)


## Website ##

@app.route('/chat', methods = ['POST'])
def chatMessage():
    msg = ''
    try:
        msg = request.get_json()
    except:
        return jsonify(error="poorly formatted json request"), 400

    try:
        new_msg_id = cache.incr('nextchatid')
        new_msg_insert = {}
        new_msg_insert['id'] = str(new_msg_id)
        new_msg_insert['username'] = msg['username']
        new_msg_insert['text'] = msg['text']

        if 'timeout' in msg:
            new_msg_insert['expiration_date'] = datetime.now() + timedelta(seconds=float(msg['timeout']))

        chatdb.messages.insert_one(new_msg_insert)

        return jsonify(id=new_msg_id), 201
    except:
        return jsonify(error="invalid message"), 400


@app.route('/chat/<id>', methods = ['GET'])
def getChatById(id):
    msg = {}
    msg_by_id = chatdb.messages.find_one({'id': id})
    rightnow = datetime.now()

    if msg_by_id is not None:
        msg['username'] = msg_by_id['username']
        msg['text'] = msg_by_id['text']

        if 'expiration_date' in msg_by_id:
            msg['expiration_date'] = msg_by_id['expiration_date'].strftime("%Y-%m-%d %H:%M:%S")

    return Response(json.dumps(msg), mimetype='application/json')


@app.route('/chats/<username>', methods = ['GET'])
def getChatByUser(username):
    msgs_found = chatdb.messages.find({'username': username})
    msgs = []
    rightnow = datetime.now()

    for chat in msgs_found:
        if 'expiration_date' in chat and rightnow >= chat['expiration_date']:
            # This message has expired and so we ignore it.
            continue

        found_chat = {}
        found_chat['username'] = chat['username']
        found_chat['text'] = chat['text']
        msgs.append(found_chat)

    return Response(json.dumps(msgs), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
