# this will allow for simple interactions with the app over a restful interface
from flask import Flask, jsonify, request, abort
from flask_cors import CORS

from ..db.map import Task, Entry
from ..db.controller import get_top_level_tasks_json

app = Flask(__name__)
CORS(app)

# GET / -> all top level tasks, as objects populated with minimal stuff
# GET /:taskid -> gets the details for a task, can be big if a top level task
# GET /entries -> gets the entries in current focus scope
# GET /entries/:entryid -> gets the metadata for the entry
# POST / -> create an entry
# POST /command -> post specifically a command
# Routes
@app.route('/', methods=['GET'])
def get_tasks():
    tasks = get_top_level_tasks_json(recurse=3)
    return jsonify({ "data": { "tasks": tasks } })

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
