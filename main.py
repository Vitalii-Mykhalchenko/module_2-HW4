from flask import Flask, request, redirect
import socket
import json
from datetime import datetime
import threading
import os


app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/style.css')
def css():
    return app.send_static_file('style.css')


@app.route('/logo.png')
def logo():
    return app.send_static_file('logo.png')


@app.route('/message.html')
def messege():
    return app.send_static_file('message.html')


@app.errorhandler(404)
def page_not_found(error):
    return app.send_static_file('error.html'), 404


@app.route('/message', methods=['POST'])
def submit():

    if request.method == 'POST':
        form_data = request.form
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        data_dict = dict(form_data)
        dto = {}
        dto["datatime"] = current_time
        dto["data"] = data_dict
        json_data = json.dumps(dto)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        sock.connect(server_address)
        sock.sendall(json_data.encode())
        sock.close()

        return redirect('/')


def socket_server(host, port):
    with socket.socket() as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            client_thread = threading.Thread(
                target=handle_client, args=(conn,))
            client_thread.start()


def handle_client(conn):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            decoded_data = json.loads(data.decode())
            file_path = './storage/data.json'
            with open(file_path, 'r') as file:
                file_content = json.load(file)
                file_content[decoded_data["datatime"]] = decoded_data["data"]

            with open(file_path, 'w') as file:
                json.dump(file_content, file)

def check_storage_directory():
    if not os.path.exists('storage'):
        os.makedirs('storage')

def check_data_json_file():
    file_path = 'storage/data.json'
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            json.dump({}, file)

if __name__ == '__main__':
    check_storage_directory()
    check_data_json_file()
    http_thread = threading.Thread(target=app.run, kwargs={'port': 3000})
    http_thread.start()
    socket_thread = threading.Thread(
        target=socket_server, args=('localhost', 5000))
    socket_thread.start()
