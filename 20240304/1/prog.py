import cowsay
import io

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

def addmon(name, x, y, hello):
    if name not in cowsay.list_cows() and name != "jgsbat":
        print("Cannot add unknown monster")
        return
    oldmon = False
    if (x*10+y) in monsters:
        oldmon = True
    monsters[x*10+y] =[name, hello]
    print(f"Added monster {name} to ({x}, {y}) saying {hello}")
    if oldmon:
        print("Replaced the old monster")

print("<<< Welcome to Python-MUD 0.1 >>>")

while command := input().split():
    if len(command) == 1:
        moving(command[0])
    elif len(command) == 5:
        if command[0] == "addmon":
            if '0' <= command[2] <= '9' and '0' <= command[3] <= '9':
                addmon(command[1],int(command[2]), int(command[3]), command[4])
            else:
                print("Invalid arguments")
        else:
            print("Invalid command")
    else:
        print("Invalid command")
