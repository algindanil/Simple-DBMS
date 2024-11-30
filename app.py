import os
import json
import traceback
from flask import Flask, request, Response, jsonify, render_template, redirect, url_for

from core import DBManager


class CustomResponse(Response):
    @classmethod
    def force_type(cls, rv, environ=None):
        if isinstance(rv, dict):
            rv = jsonify(rv)
        return super(CustomResponse, cls).force_type(rv, environ)


def init_module():
    app = Flask(__name__)
    app.response_class = CustomResponse
    database = DBManager(os.environ.get('DB_FILE_PATH') or 'db.json')
    return app, database


app, DB = init_module()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get', methods=['GET', 'POST'])
def db_get():
    if request.method == 'POST':
        key = request.form.get('key')
        if not key:
            return render_template('index.html', error="Missing key")
        values = DB.get(key)
        return render_template('index.html', key=key, values=values)
    return render_template('index.html')


@app.route('/set', methods=['GET', 'POST'])
def db_set():
    if request.method == 'POST':
        key = request.form.get('key')
        value = request.form.get('value')
        if not key or not value:
            return render_template('index.html', error="Missing key or value")

        result = DB.set(key, value)
        message = f"Value '{value}' added to key '{key}'" if result else f"Error adding value '{value}' to key '{key}'"
        return render_template('index.html', message=message)
    return render_template('index.html')


@app.route('/remove', methods=['POST'])
def db_remove():
    key = request.form.get('key')
    value = request.form.get('value')
    if not key or not value:
        return render_template('index.html', error="Missing key or value")

    result = DB.remove_value(key, value)
    message = f"Value '{value}' removed from key '{key}'" if result else f"Error removing value '{value}' from key '{key}'"
    return render_template('index.html', message=message)


@app.route('/keys', methods=['GET'])
def db_keys():
    keys = list(DB.keys())
    return render_template('index.html', keys=keys)


@app.route('/values', methods=['GET'])
def db_values():
    values = list(DB.values())
    return render_template('index.html', values=values)


@app.route('/items', methods=['GET'])
def db_items():
    items = [list(item) for item in DB.items()]
    return render_template('index.html', items=items)


@app.route('/dumps', methods=['GET'])
def db_dumps():
    database = json.loads(DB.dumps())
    return render_template('index.html', database=database)


@app.route('/truncate-db', methods=['POST'])
def db_truncate():
    result = DB.truncate_db()
    message = "DB has been truncated successfully." if result else "Error truncating DB."
    return render_template('index.html', message=message)


if __name__ == '__main__':
    app.run(debug=True)
