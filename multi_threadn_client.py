import socket
import sys
import select as sel

SOCKET_LIST = [sys.stdin]

host = "127.0.0.1"
port = 4444
def chat_client():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10) #timeout in 10 sec
    
    try:
        s.connect((host,port))
    except:
        print("Cannot reach {}:{} ...".format(host, port))
        sys.exit(1)
        
    while True:
        ready_read, ready_write, error = sel.select(SOCKET_LIST, [], [])
        #Block until connection is made
        
        for sock in ready_read:
            
            if sock == s:
                data = data.recv(4000).decode()
                
                if not data:
                    print("Chat Disconnected...")
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    sys.stdout.write("> ")
                    sys.stdout.flash()
            else:
                msg = sys.stdin.readline()
                s.sent(msg.encode())
                sys.stdout.write("> ")
                sys.stdout.flush()
                
if __name__ == "__main__":
    sys.exit(chat_client())
                