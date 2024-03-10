import cowsay

player = [0,0]
monsters = {}

def encounter(x,y):
    print(cowsay.cowsay(monsters[x*10+y]))

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

def addmon(x, y, hello):
    oldmon = False
    if (x*10+y) in monsters:
        oldmon = True
    monsters[x*10+y] = hello
    print(f"Added monster to ({x}, {y}) saying {hello}")
    if oldmon:
        print("Replaced the old monster")

while command := input().split():
    if len(command) == 1:
        moving(command[0])
    elif len(command) == 4:
        if command[0] == "addmon":
            if '0' <= command[1] <= '9' and '0' <= command[2] <= '9':
                addmon(int(command[1]), int(command[2]), command[3])
            else:
                print("Invalid arguments")
        else:
            print("Invalid command")
    else:
        print("Invalid command")



