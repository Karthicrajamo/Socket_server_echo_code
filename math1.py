import socket
from subprocess import Popen, PIPE, STDOUT
from threading import Thread

def start_new_math_Thread(conn, addr):
    t = MathServerCommunicationThread(conn, addr)
    t.start()
    
class ProcessOutputThread(Thread):
    def __init__(self, proc, conn):
        Thread.__init__(self)
        self.proc = proc
        self.conn = conn
        
    def run(self):
        while not self.proc.stdout.closed and not self.conn._closed:
            try:
                self.conn.sendall("> ".encode())
                self.conn.sendall(self.proc.stdout.readline())
                self.conn.sendall("\n<<".encode())
            except:
                pass                
    
    
class MathServerCommunicationThread(Thread):
    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        
    def run(self):
        print("{} is connected to the port {}...".format(self.addr[0], self.addr[1]))
        self.conn.sendall("Now your are entered into Math Server. You can ask any type of Mathematical Calculations:".encode())
        
        #APPLICATION LAYER
        p = Popen(['bc'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
        h = ProcessOutputThread(p, self.conn)
        h.start()
        
        while not p.stdout.closed and not self.conn._closed:
            #PRESENTATION LAYER
            try:
                data = self.conn.recv(2000)
                if not data:
                    break
                else:
                    try:
                        data = data.decode()
                        query = data.strip()
                        # print("Welcome")
                        if query == "quit" or query == "exit":
                            p.communicate(query.encode(), timeout = 1)
                            print("exit")
                            if p.poll() is not None:
                                break
                        self.conn.sendall("--> ".encode())
                        query = query + "\n"
                        p.stdin.write(query.encode())
                        p.stdin.flush()
                    except:
                        pass              
            except:
                pass
        self.conn.close()
    
host = ''
port = 3334


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen()

while True:
    conn, addr = s.accept()
    start_new_math_Thread(conn, addr)
s.close()