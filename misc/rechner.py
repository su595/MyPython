import datetime


# x = int(input())
# y = int(input())
# print(y+x)


# date = datetime.datetime.now() #Jetziges Datum
# bdayYear = int(input("Bday year pls: "))
# bdayMonth = int(input("Bday month pls: "))

# if bdayMonth <= date.month: #Geburstag war in diesem Jahr schon
#     age = int(date.year - bdayYear)
# else: #Geburstag war noch nicht (also ist das Alter noch ein Jahr weniger)
#     age = int(date.year - bdayYear - 1)

# print("Dein Alter ist", age)

x = int(input("Zahl 1  "))
y = int(input("Zahl 2  "))
op = input("+, -, * oder /  ")

if op == "+":
    res = x+y
elif op == "-":
    res = x-y
elif op == "*":
    res = x*y
elif op == "/":
    res = x/y
else:
    res = "Du bist inkompetent"

print(res)
