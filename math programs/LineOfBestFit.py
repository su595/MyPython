
LIST_OF_POINTS = [(0,0), (4,5), (2,9), (12,4), (7, 2)]
LINEAR = [(0,3.5), (1,4), (2,4.5), (3,5)]
MARGIN = 1

def getAverageM(points):
    # points is a two dimensional list

    if len(points) == 0:
        raise Exception()

    averageM = 0
    i = 0

    for firstPoint in points:
        for secondPoint in points:
            if firstPoint == secondPoint: # dont get the gradient between one point
                break

            x1 = firstPoint[0]
            x2 = secondPoint[0]
            y1 = firstPoint[1]
            y2 = secondPoint[1]

            m = (y2-y1)/(x2-x1)

            i += 1 

            averageM += m
    
    averageM = averageM/i

    return averageM

def getB(points, m):

    def averageDistanceFromLine(points, m, b):
        averageDistance = 0
        i = 0
        for point in points:
            averageDistance += abs(point[1] - (m*i+b)) # sum the difference of the real y-value and the corresponding line value f(i)
            print("-- " +str(averageDistance))
            i += 1

        return averageDistance

    b = points[0][1] # first make b the y coordinate of the first point
    averageDeviation = averageDistanceFromLine(points, m, b)
    i = 0

    while averageDeviation > MARGIN:
        newb = averageDistanceFromLine(points, m, b)

        deltab = b - newb
        b = newb + deltab *0.5
        i += 1
        if i > 100:
            break

    return b


m = getAverageM(LIST_OF_POINTS)
print(m)
print("kjahfgjk")
b = getB(LIST_OF_POINTS, m)
print("test +" +str(m))
print(f"y = {m}x+{b}")

# see the outline of algorhythm on samsung notes
