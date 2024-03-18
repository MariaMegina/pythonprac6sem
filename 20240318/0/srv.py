import socket
import sys
import shlex

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while data := conn.recv(1024):
            com = shlex.split(data.decode())
            match com[0:2]:
                case ["print", _]:
                    conn.sendall(" ".join(com[1:]).encode() + b"\n")
                case ["info", "host"]:
                    conn.sendall(addr[0].encode())
                case ["info", "port"]:
                    conn.sendall(str(addr[1]).encode())
