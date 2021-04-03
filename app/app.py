from flask import Flask

from dockerapi.DockerCon import DockerCon

app = Flask(__name__)

dockerAPI = DockerCon("tcp://127.0.0.1:2375")


@app.route('/')
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
    app.run()
