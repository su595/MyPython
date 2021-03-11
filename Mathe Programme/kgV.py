
def kgVRechner(a, b): #kleinstesGemeinsamesVielfaches
    if a or b == 0:
        kgV = 0
    
    nA = 1
    nB = 1
    while (a*nA)%b != 0: # Ich hab hier vergessen Kommentare hinzuzufügen ^^
        nA += 1

    while (b*nB)%a != 0:
        nB += 1

    if a<0:
        nA = nA-2*nA
        print("nA negativ", nA)
    if b<0:
        nB = nB-2*nB
        print("nB negativ", nB)

    if(nA<nB):
        kgV = a*nA
    else:
        kgV = b*nB

    print("Kleinstes gemeinsames Vielfaches von a=", a, "und b=", b, "ist", kgV, "(a*", nA, "und b*", nB, ")") #ES FUNKTIONIERT!!!!!!!

    return kgV


kgVRechner(-5, 10)

