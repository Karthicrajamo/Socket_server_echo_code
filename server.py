import socket

host = ''
port = 3333

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# print("Echoing IPV4 line : {}".format(s))
s.bind((host,port))
s.listen(10)
conn, addr = s.accept()
print("{} is connected with backport {}".format(addr[0],addr[1]))

while True:
    data = conn.recv(1024)
    if not data:
        print("breaking...")
        break
    else:
        data = data.decode()
        # print("echo > {}".format(data))
        if(data == "quit"):
            break
        else:
            conn.send(data.encode())
s.close()
