from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json

app = Flask(__name__)

pusher = Pusher(
    app_id='1067908',
    key='e93dc138050cd12bd114',
    secret='a97768fa2e83ecbd6e34',
    cluster='us3',
    ssl=True
)


@app.route('/')
def index():
    return render_template('index.html')


# endpoint for storing todo item
@app.route('/add-todo', methods=['POST'])
def addTodo():
    data = json.loads(request.data)  # load JSON data from request
    pusher.trigger('todo', 'item-added', data)  # trigger `item-added` event on `todo` channel
    return jsonify(data)


# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
    data = {'id': item_id}
    pusher.trigger('todo', 'item-removed', data)
    return jsonify(data)


# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods=['POST'])
def updateTodo(item_id):
    data = {
        'id': item_id,
        'completed': json.loads(request.data).get('completed', 0)
    }
    pusher.trigger('todo', 'item-updated', data)
    return jsonify(data)


# run Flask app in debug mode
app.run(debug=True)
