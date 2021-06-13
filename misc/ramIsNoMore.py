
i = 0

class evil():
    def __init__(self):

        global i 
        i += 1

        print(i)

        unlimitedObjects = evil()



start = evil()

