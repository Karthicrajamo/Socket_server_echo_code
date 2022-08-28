import socket as s
import select as sel
import sys

host = ''
port = 4444
SOCKET_LIST = []
 
def chat_server():
    server_socket = s.socket(s.AF_INET,s.SOCK_STREAM)
    server_socket.setsockopt(s.SOL_SOCKET, s. SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    SOCKET_LIST.append(server_socket)
    
    print("Server is ready to listen port : "+str(port))
    
    while True:
        #Blocking the flow for new coming connection...
        ready_read, ready_write, error = sel.select(SOCKET_LIST, [], [])
        
        for sock in ready_read:
            
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                # print("client_socket at line 25 : {}".format(client_socket))
                print("client {} from port {}".format(addr[0],addr[1]))
                SOCKET_LIST.append(client_socket)
                # Entering into chat room
                print("hello")
                broadcast(server_socket, client_socket, "{} entered in our chat room : In the port {}...".format(addr[0],addr[1]))
                
            else:
                try:
                    data = sock.recv(1000)
                    data = data.encode()
                    
                    if data:
                        print("---------------\nserver_socket is holding the value : {}".format(server_socket))
                        broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(),data))
                    
                    else:
                        #socket must have been broken, remove it from the list, and broadcast a message
                        broadcast(server_socket, sock, "[{}] Client is Offline".format(sock.getpeername()))
                        
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)
                            
                except:
                    broadcast(server_socket, sock, "[{}] {}".format(sock.getpeername(),"Client is Out"))
                    continue
                
def broadcast(server_socket, client_socket, message):
    print("broadcasting.....")
    
    for socket in SOCKET_LIST:
        
        if socket != server_socket and socket != client_socket:
            try:
                # print("hiii")
                socket.sent(message.encode())
            except:
                
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
                    
if __name__ == "__main__":
    sys.exit(chat_server())                    
                        