import socket

s = socket.socket()
s.connect(("127.0.0.1",5000))

print("Connected to server")

while True:
    cmd = input(">> ")
    if cmd.lower()=="exit":
        break

    s.send((cmd+"\n").encode())
    print(s.recv(1024).decode())

s.close()
