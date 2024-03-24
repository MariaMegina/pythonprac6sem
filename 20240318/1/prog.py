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

        print(f"Attacked {mon[0]}, damage {dmg} hp")
        mon[2]-=dmg
        if mon[2] <= 0:
            print(f"{mon[0]} died")
            del monsters[player[0]*10 + player[1]]
        else:
            print(f"{mon[0]} now has {mon[2]}")
