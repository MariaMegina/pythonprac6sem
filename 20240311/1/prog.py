import cowsay
import shlex
import io
import sys
import cmd


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
        print(cowsay.cowsay(monsters[x*10+y][1], cowfile = jgsbat))
    else:
        print(cowsay.cowsay(monsters[x*10+y][1], cow = monsters[x*10+y][0]))

def moving(c):
    rc = True
    if c == 'up':
        player[1] = (player[1] - 1) % 10
    elif c == 'down':
        player[1] = (player[1] + 1) % 10
    elif c == 'left':
        player[0] = (player[0] - 1) % 10
    elif c == 'right':
        player[0] = (player[0] + 1) % 10
    else:
        rc = False
        print("Invalid command")
    if rc:
        print(f"Moved to ({player[0]}, {player[1]})")
        if (player[0]*10 + player[1]) in monsters:
            encounter(player[0], player[1])

def addmon(name, x, y, hello, hitpoints):
    if name not in cowsay.list_cows() and name != "jgsbat":
        print("Cannot add unknown monster")
        return
    oldmon = False
    if (x*10+y) in monsters:
        oldmon = True
    monsters[x*10+y] =[name, hello, hitpoints]
    print(f"Added monster {name} to ({x}, {y}) saying {hello}")
    if oldmon:
        print("Replaced the old monster")

class GameCmd(cmd.Cmd):

    prompt = ">> "

    def __init__(self):
        print("<<< Welcome to Python-MUD 0.1 >>>")
        return super().__init__()

    
    def do_up(self, args):
        "moves up"
        moving("up")


    def do_down(self, args):
        "moves down"
        moving("down")


    def do_left(self, args):
        "moves left"
        moving("left")


    def do_right(self, args):
        "moves right"
        moving("right")


    def do_addmon(self, args):
        "add monster"
        command = shlex.split(args)
        if len(command) == 8 and "hello" in command and "hp" in command and "coords" in command:
            name = command[0]
            hello_string = command[command.index("hello")+1]
            hitpoints = command[command.index("hp")+1]
            x = command[command.index("coords")+1]
            y = command[command.index("coords")+2]
            if hitpoints.isdigit() and x.isdigit() and y.isdigit() and "0" <= x <= "9" and "0" <= y <= "9":
                hitpoints = int(hitpoints)
                x = int(x)
                y = int(y)
                addmon(name, x, y, hello_string, hitpoints)
            else:
                print("Invalid arguments")

        else:
            print("Invalid arguments")
    

if __name__ == '__main__':
    GameCmd().cmdloop()
