from flask import Flask, request
import json
from dockerapi.DockerCon import DockerCon

app = Flask(__name__)

dockerAPI = DockerCon("tcp://127.0.0.1:2375")


@app.route('/sync', methods=['POST'])
def syncWithAppwrite():
    """
    Post data expected:

    1. Refreshes current sessions
    JSON {
        "start" : ["session_id", ...],
        "end" : ["session_id", ...]
    }
    2. Starting new session
    :return: json {
    "started_containers" : [ {"session_id" : "id", "container_id" : "id", "server_url" : "url"}, ...],
    "absent_containers" : ["session_id", ...]}
    """
    print(json.loads(request.get_data()))
    absent_containers = dockerAPI.updateList()
    return "None"



@app.route('/appwrite/event/start')
def appwrite_start_server():
    print("Got request")
    print(str(request))
    return "Got request"


@app.route('/list/containers')
def list_containers():
    return dockerAPI.list_container()


@app.route('/list/ports')
def list_ports():
    return dockerAPI.list_ports()


@app.route('/list/sessions')
def list_sessions():
    return dockerAPI.list_sessions()


@app.route('/start')
def start_session():
    if dockerAPI.start_session():
        return 'Started new session'
    else:
        return 'Failed to start new session, no more ports available'


@app.route('/stop/all')
def end_all_sessions():
    dockerAPI.stop_all_sessions()
    return 'Stopped all'


if __name__ == '__main__':
    app.run(host="0.0.0.0")
