from flask import Flask, render_template, request
from wakeonlan import send_magic_packet
import paramiko
import socket

app = Flask(__name__)

def is_server_online(hostname):
    hostname = '10.10.20.1'
    port = 22
    timeout = 3
    try:
        socket.setdefaulttimeout(timeout)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((hostname, port))
        sock.close()
        return True
    except socket.error as e:
        return False

@app.route('/')
def index():
    hostname = '10.10.20.1'
    if is_server_online(hostname):
        status = "Proxmox Server is online"
    else:
        status = "Proxmox Server is offline"
    return status
    
@app.route('/start', methods=['GET'])
def start():
    try:
        mac_address = '3c:ec:ef:89:c4:3c'
        send_magic_packet(mac_address)
        return "Server started"
    except Exception as e:
        print (f"Error during shutdown: {e}")
        return "Server already online"

@app.route('/stop', methods=['GET'])
def stop():
    hostname = '10.10.20.1'
    port = 22
    username = 'root'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(hostname, port=port, username=username)
        ssh.exec_command('shutdown now')
        ssh.close()
        return "Server stopped"
    except Exception as e:
        ssh.close()
        print (f"Error during shutdown: {e}")
        return "Server already offline"

if __name__ == '__main__':
    app.run(host='10.10.20.5', port=80)