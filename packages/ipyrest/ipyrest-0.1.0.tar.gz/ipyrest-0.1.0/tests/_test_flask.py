"""
Ipyrest tests running on a local server implementing sample API endpoints.

To be executed with pytest:

    pytest -s -v test_flask.py
"""

import time
from threading import Thread

from flask import Flask
import pytest
import requests


app = Flask(__name__)

@app.route('/')
def main():
    return 'foo'

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from contextlib import closing

def find_free_port():
    with closing(socket(AF_INET, SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        return s.getsockname()[1]

def run_flask_app(app, kwargs):
    "Run a flask server inside a thread."

    t = Thread(target=app.run, kwargs=kwargs)
    t.daemon = True
    t.start()
    time.sleep(1)


# from api_server import find_free_port, run_flask_app
port = find_free_port()
kwargs = dict(host='0.0.0.0', port=port, debug=False)
run_flask_app(app, kwargs)

server = f'http://localhost:{port}'
try:
    requests.get(f'{server}/')
    SERVER_NOT_FOUND = False
except requests.exceptions.ConnectionError:
    SERVER_NOT_FOUND = True


@pytest.mark.skipif(SERVER_NOT_FOUND, reason="API server not found.")
def test():
    "Test..."

    server = f'http://localhost:{port}'
    requests.get(f'{server}/').text
