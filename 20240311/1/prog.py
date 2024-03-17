import cowsay
import shlex
import io
import sys

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


print("<<< Welcome to Python-MUD 0.1 >>>")

while command := shlex.split(sys.stdin.readline()):
    if len(command) == 1:
        moving(command[0])
    elif len(command) == 9 and command[0] == "addmon":
        if "hello" in command and "hp" in command and "coords" in command:
            name = command[1]
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
    else:
        print("Invalid command")
