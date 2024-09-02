# this will allow for simple interactions with the app over a restful interface
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from ..db.map import Task, Entry
from ..db import Controller

app = Flask(__name__)
CORS(app)

# GET / -> all top level tasks, as objects populated with minimal stuff
# GET /:taskid -> gets the details for a task, can be big if a top level task
# GET /entries -> gets the entries in current focus scope
# GET /entries/:entryid -> gets the metadata for the entry
# POST / -> create an entry
# POST /command -> post specifically a command
# Routes
@app.route('/', methods=['Get'])
def ping():
    return "I am here!"

@app.route('/tasks', methods=['GET'])
def get_tasks():
    with Controller() as conn:
        tasks = conn.get_focused_tasks()
        tasks_json = [task.json(recurse=3) for task in tasks]
    return jsonify({ "data": { "tasks": tasks_json } })


# @app.route('/entries', methods=['GET'])
def get_entries():
    with Controller() as conn:
        entries = conn.get_recent_entries()
        entries_json = [entry.json(recurse=1) for entry in entries]
    return entries_json

# @app.route('/entries', methods=['POST'])
def create_entry():
    data = request.get_json()
    print('received data: ', data)
    entry = data.get('entry', {})
    print('got entry: ', entry)
    if not entry:
        return jsonify({"error": "entry field is required"}), 400
    with Controller() as conn:
        entry_object = conn.create_entry(entry)
        entry_json = entry_object.json(recurse=1)
    return entry_json


@app.route('/entries', methods=['GET', 'POST'])
def route_entries():
    if request.method == "GET":
        entries = get_entries()
        return jsonify({ "data": { "entries": entries } })
    elif request.method == "POST":
        entry = create_entry()
        # return create_entry()
        return jsonify(entry)



@app.route('/latest', methods=['GET'])
def get_latest():
    with Controller() as conn: 
        latest = conn.get_latest()
    return jsonify({ "data": latest })

# @app.route('/<int:task_id>', methods=['GET'])
# def get_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     return jsonify({'id': task.id, 'title': task.title, 'description': task.description})
#
# @app.route('/entries', methods=['GET'])
# def get_entries():
#     entries = Entry.query.all()  # Replace with focus scope logic
#     return jsonify([{'id': entry.id, 'content': entry.content} for entry in entries])
#
# @app.route('/entries/<int:entry_id>', methods=['GET'])
# def get_entry(entry_id):
#     entry = Entry.query.get_or_404(entry_id)
#     return jsonify({'id': entry.id, 'metadata': entry.metadata, 'content': entry.content})
#
# @app.route('/', methods=['POST'])
# def create_entry():
#     data = request.json
#     task_id = data.get('task_id')
#     content = data.get('content')
#     if not task_id or not content:
#         abort(400, description="Task ID and content are required")
#     
#     entry = Entry(task_id=task_id, content=content)
#     db.session.add(entry)
#     db.session.commit()
#     return jsonify({'id': entry.id, 'task_id': entry.task_id, 'content': entry.content}), 201
#
# @app.route('/command', methods=['POST'])
# def post_command():
#     data = request.json
#     command = data.get('command')
#     if not command:
#         abort(400, description="Command is required")
#     
#     # Process command logic here
#     return jsonify({'status': 'command received', 'command': command}), 201
#
# # Initialize the database
# with app.app_context():
#     db.create_all()
#
# # post / allows you to create entries
