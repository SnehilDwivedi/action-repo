from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client.github_webhooks
events_collection = db.events

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('Content-Type') != 'application/json':
        return jsonify({'error': 'Invalid content type'}), 400

    payload = request.json
    event_type = request.headers.get('X-GitHub-Event')

    # Process different event types
    if event_type == 'push':
        process_push_event(payload)
    elif event_type == 'pull_request':
        process_pull_request_event(payload)
    elif event_type == 'merge':
        process_merge_event(payload)
    else:
        return jsonify({'error': 'Unsupported event type'}), 400

    return jsonify({'status': 'success'}), 200

def process_push_event(payload):
    event = {
        'request_id': payload['after'],
        'author': payload['pusher']['name'],
        'action': 'PUSH',
        'from_branch': None,  # Push events don't have a from_branch
        'to_branch': payload['ref'].split('/')[-1],
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    events_collection.insert_one(event)

def process_pull_request_event(payload):
    pr_action = payload['action']
    if pr_action not in ['opened', 'reopened']:
        return
        
    event = {
        'request_id': str(payload['pull_request']['id']),
        'author': payload['pull_request']['user']['login'],
        'action': 'PULL_REQUEST',
        'from_branch': payload['pull_request']['head']['ref'],
        'to_branch': payload['pull_request']['base']['ref'],
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    events_collection.insert_one(event)

def process_merge_event(payload):
    if payload.get('merged') and payload['pull_request']['merged']:
        event = {
            'request_id': str(payload['pull_request']['id']),
            'author': payload['pull_request']['merged_by']['login'],
            'action': 'MERGE',
            'from_branch': payload['pull_request']['head']['ref'],
            'to_branch': payload['pull_request']['base']['ref'],
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        events_collection.insert_one(event)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/events')
def get_events():
    events = list(events_collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(50))
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)