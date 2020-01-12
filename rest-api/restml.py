from flask import Flask, jsonify, request, abort, make_response
import json
import os
from json.decoder import JSONDecodeError


app = Flask(__name__)




@app.route('/api/get', methods=['GET'])
def get_json():
    with open('dummy.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

@app.route('/api/post', methods=['POST'])
def post_json():
    if not request.json or not 'title' in request.json:
        abort(400)


    with open('tasks.json', "w+") as json_file:
        try:
            print("try")
            tasks = json.load(json_file)
            task_index = tasks[-1]['id'] + 1
        except:
            print("except")
            tasks = {}
            tasks['tasks'] = []
            task_index = 1

        task = {
            'id': task_index,
            'title': request.json['title'],
            'description': request.json.get('description', ""),
            'done': False
        }
        tasks['tasks'].append(task)

        json.dump(tasks, json_file)

    return jsonify({'task': task}), 201

if __name__ == '__main__':
    app.run(debug=True)

