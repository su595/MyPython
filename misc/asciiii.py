from base64 import decode, encode


def printASCII(max_chars=4):
    buf="asc: "
    buf2="chr: "
    for i in range(32,128):
        
        add = str(i)
        if(len(add) != max_chars):
            add += (max_chars-len(add)) * " "
        buf += add

        add =  chr(i)
        if(len(add) != max_chars):
            add += (max_chars-len(add)) * " "
        buf2 += add


        if((i+1)%16 == 0):
            print(buf2)
            print(buf)
            buf="asc: "
            buf2="chr: "


    
printASCII()

max_chars=4
buf="asc:"
buf2="chr:"
for i in range(32,128):
    
    add = str(i)
    if(len(add) != max_chars):
        add += (max_chars-len(add)) * " "
    buf += add

    add =  chr(i)
    if(len(add) != max_chars):
        add += (max_chars-len(add)) * " "
    buf2 += add


    if((i+1)%16 == 0):
        print(buf2)
        print(buf)
        buf="asc:"
        buf2="chr:"