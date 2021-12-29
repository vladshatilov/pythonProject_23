import os
import itertools as it
from flask import Flask, request, jsonify

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
print(DATA_DIR)


class MyOwlException(Exception):
    pass


def lines(path):
    with open(path, 'r') as file:
        for line in file:
            yield line


def fetch_list(command, value, arr):
    if command == 'filter':
        return filter(lambda x: value in x, arr)
    elif command == 'map':
        return map(lambda x: x.split(' ')[int(value)], arr)
    elif command == 'unique':
        return set(x for x in arr)
    elif command == 'sort':
        return sorted(arr, key=lambda x: x, reverse=False if value == 'asc' else True)
    elif command == 'limit':
        return it.islice(arr, 0, int(value))
    else:
        return 1


@app.route("/perform_query", methods=['GET', 'POST'])
def perform_query():
    if request.method == 'POST':
        details = request.json
        path = f"{DATA_DIR}\\{details.get('file_name')}"
        try:
            temp = fetch_list(details.get('cmd1'), details.get('value1'), lines(path))
            temp = fetch_list(details.get('cmd2'), details.get('value2'), temp)
            return jsonify(list(temp))
        except FileNotFoundError as e:
            # raise MyOwlException(str(e))
            return jsonify({"error": "invalid payload"}), 400
    return app.response_class('', content_type="text/plain")
