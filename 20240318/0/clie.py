import sys
import socket
import cmd

host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

class ClieCmd(cmd.Cmd):
    prompt = ">>"

    def do_print(self, args):
        s.sendall(args)
        print(s.recv(1024).rstrip().decode())

    def do_info(self, args):
        match args[0]:
            case "host":
                s.sendall(args[1:])
                print(s.recv(1024).rstrip().decode())
            case "port":
                s.sendall(args[1:])
                print(s.recv(1024).rstrip().decode())

if __name__ == "__main__":
    ClieCmd().cmdloop()



