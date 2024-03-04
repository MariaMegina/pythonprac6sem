import shlex

while s1 := input("ФИО: "):
    s2 = input("Место: ")
    try:
        print("register ", shlex.join(shlex.split(s1)), shlex.join(shlex.split(s2)))
    except Exception as E:
        print(E)

