import socket            
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)        
port = 3333               
 
s.connect(('127.0.0.1', port))
while True: 
        msg = input("> ")
        if not msg:
            print("No Data")
        else:
            s.sendall(msg.encode())
            print (s.recv(1024).decode())
    # close the connection
s.close()  