import cowsay
import shlex
import io
import sys
import cmd
import socket
import multiprocessing


player = [0,0]
monsters = {}

jgsbat = cowsay.read_dot_cow(io.StringIO('''
$the_cow = <<EOC;
         $thoughts
          $thoughts
    ,_                    _,
    ) '-._  ,_    _,  _.-' (
    )  _.-'.|\\--//|.'-._  (
     )'   .'\/o\/o\/'.   `(
      ) .' . \====/ . '. (
       )  / <<    >> \  (
        '-._/``  ``\_.-'
  jgs     __\\'--'//__
         (((""`  `"")))
EOC
'''))

def encounter(x,y):
    if monsters[x*10+y][0] == "jgsbat":
        return (cowsay.cowsay(monsters[x*10+y][1], cowfile = jgsbat))
    else:
        return(cowsay.cowsay(monsters[x*10+y][1], cow = monsters[x*10+y][0]))

def moving(x, y):
    player[0] = (player[0] + x) % 10
    player[1] = (player[1] + y) % 10
    responce = (f"Moved to ({player[0]}, {player[1]})")
    if (player[0]*10 + player[1]) in monsters:
    	responce += encounter(player[0], player[1])
    return responce

def addmon(name, x, y, hello, hitpoints):
    if name not in cowsay.list_cows() and name != "jgsbat":
        print("Cannot add unknown monster")
        return
    oldmon = False
    if (x*10+y) in monsters:
        oldmon = True
    monsters[x*10+y] =[name, hello, hitpoints]
    responce = (f"Added monster {name} to ({x}, {y}) saying {hello}")
    if oldmon:
        responce += ("\nReplaced the old monster")
    return responce



def attack(name, weapon = "sword"):
    if (player[0]*10 + player[1]) not in monsters:
        print("No monster here")
        return
    else:
        mon = monsters[player[0]*10 + player[1]]
        if weapon == "sword":
            dmg = 10
        elif weapon == "spear":
            dmg = 15
        elif weapon == "axe":
            dmg = 20
        else:
            print("Unknown weapon")
            return

        if mon[0] != name:
            print(f"No {name} in here")
            return

        responce = (f"Attacked {mon[0]}, damage {dmg} hp")
        mon[2]-=dmg
        if mon[2] <= 0:
            responce += (f"\n{mon[0]} died")
            del monsters[player[0]*10 + player[1]]
        else:
            responce += (f"\n{mon[0]} now has {mon[2]}")
        return responce


def serve(conn, addr):
    with conn:
        print("Connected by", addr)
        while data := conn.recv(1024):
            com, *args = shlex.split(data.decode())
            match com:
                case "move":
                    conn.sendall(moving(int(args[0]), int(args[1])).encode())
                case "addmon":
                    conn.sendall(addmon(args[0], int(args[1]), int(args[2]), args[3], int(args[4])).encode())
                case "attack":
                    if len(args) == 1:
                        conn.sendall(attack(args[0]).encode())
                    else:
                        conn.sendall(attack(args[0], args[1]).encode())



host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
port = 1333 if len(sys.argv) < 3 else int(sys.argv[2])
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen()
    conn, addr = s.accept()
    multiprocessing.Process(target = serve, args = (conn, addr)).start()
