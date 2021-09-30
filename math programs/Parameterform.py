# Man merkt dass ich das programmiert habe bevor ich Klassen kannte

def Parameterform (tA, tB, tC): #Es werden drei Tuples mit jeweils 3 Werten, nämlich x1, x2 und x3 übergeben.
    x1A = tA[0]
    x2A = tA[1]
    x3A = tA[2]

    x1B = tB[0]
    x2B = tB[1]
    x3B = tB[2]

    x1C = tC[0]
    x2C = tC[1]
    x3C = tC[2]

    if ((x1A*x1B) == (x2A*x2B)) and ((x1A*x1B) == (x3A*x3B)): #Wenn das Produkt aller Koordinaten gleich ist, dann sind die Punkte linear abhänig. 
        linearAbhängig = True                                 #Beim Produkt anstelle des Quotienten gibt es keine Problemem beim Teilen durch 0.

    elif ((x1A*x1C) == (x2A*x2C)) and ((x1A*x1C) == (x3A*x3C)):
        linearAbhängig = True
    
    else:
        linearAbhängig = False
        OA = tA
        AB = ((x1B - x1A), (x2B - x2A), (x3B - x3A))
        AC = ((x1C - x1A), (x2C - x2A), (x3C - x3A))


    if linearAbhängig: #Wenn die Vektoren linear abhänig sind
        print("Vektoren sind linear abhängig, es gibt nicht genug Punkte, um die Ebene zu definieren.")
    else: 
        print("Die Parameterform ist:", OA, "+ r *", AB, "+ r *", AC)


tA = (4, 0, 3.5) #Punkte A, B und C
tB = (0, 4, 4.5)
tC = (0, 6, 2.5)

Parameterform(tA, tB, tC)
