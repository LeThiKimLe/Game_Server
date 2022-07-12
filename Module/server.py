from msilib.schema import Error
import socket
import os
from _thread import *
import sys
import Module.data_process as exe
import tkinter as tk

ServerSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

hostname = socket.gethostname()
host=socket.gethostbyname(hostname)
port = 1233
ThreadCount = 0

REQUEST={'GET_DATA':1, 'LOGIN':2, 'REGIS':3, 'SAVE':4, 'RANK':5}
user=exe.User_Data()
game=exe.Game_Data()

class Buffer:
    def __init__(self,s):
        '''Buffer a pre-created socket.
        '''
        self.sock = s
        self.buffer = b''

    def get_bytes(self,n):
        '''Read exactly n bytes from the buffered socket.
           Return remaining buffer if <n bytes remain and socket closes.
        '''
        while len(self.buffer) < n:
            data = self.sock.recv(1024)
            if not data:
                data = self.buffer
                self.buffer = b''
                return data
            self.buffer += data
        # split off the message bytes from the buffer.
        data,self.buffer = self.buffer[:n],self.buffer[n:]
        return data

    def put_bytes(self,data):
        self.sock.sendall(data)

    def get_utf8(self):
        '''Read a null-terminated UTF8 data string and decode it.
           Return an empty string if the socket closes before receiving a null.
        '''
        while b'\x00' not in self.buffer:
            data = self.sock.recv(1024)
            if not data:
                return ''
            self.buffer += data
        # split off the string from the buffer.
        data,_,self.buffer = self.buffer.partition(b'\x00')
        return data.decode()

    def put_utf8(self,s):
        if '\x00' in s:
            raise ValueError('string contains delimiter(null)')
        self.sock.sendall(s.encode() + b'\x00')


def threaded_client(connection):

    def send_gamedata(conn, files_to_send):
        with conn:
            sbuf = Buffer(conn)
            hash_type = 'abc'

            for file_name in files_to_send:
                print(file_name)
                sbuf.put_utf8(hash_type)
                sbuf.put_utf8(file_name)

                file_size = os.path.getsize(file_name)
                sbuf.put_utf8(str(file_size))

                with open(file_name, 'rb') as f:
                    sbuf.put_bytes(f.read())
                print('File Sent')

        return 'F'

                
    def request_process(data):
        data=data.split(',')
        req=data[0]
        if 5>REQUEST[req]>=2:
            infor=','.join(data[1:])
            if REQUEST[req]==2:
                rep=str(user.check_user(infor))
            elif REQUEST[req]==3:
                rep=str(user.add_user(infor))
            else:
                rep=user.update_user_dataplay(infor)

        elif REQUEST[req]==1:
            list_filedata=game.game_data()
            rep=send_gamedata(connection, list_filedata)
        return rep
            
    while True:
        data = connection.recv(2048)
        data=data.decode('utf-8')
        if data=='OK':
            break
        rep=request_process(data)
        if rep=='F':
            break
        connection.sendall(str.encode(rep))
    connection.close()

def Start_Server():
    global ThreadCount
    try:
        ServerSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Waitiing for a Connection..')
    ServerSocket.listen(5)

    while True:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSocket.close()

class Redirect():
    
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert('end', text)
        self.widget.see('end') # autoscroll

def Begin():
    root = tk.Tk()

    text = tk.Text(root)
    text.pack()

    old_stdout = sys.stdout    
    sys.stdout = Redirect(text)

    root.mainloop()

    sys.stdout = old_stdout

