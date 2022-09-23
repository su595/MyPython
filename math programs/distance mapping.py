
from cmath import sqrt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from PIL import Image
import numpy as np

w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()


def getDistance(point1, point2):
    x1 = point1[0]
    x2 = point2[0]
    y1 = point1[1]
    y2 = point2[1]

    return sqrt((x2-x1)**2 + (y2-y1)**2).real

# copied from internet
def frange_positve(start, stop=None, step=None):
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    print("start = ", start, "stop = ", stop, "step = ", step)

    count = 0
    while True:
        temp = float(start + count * step)
        if temp >= stop:
            break
        yield temp
        count += 1

def map(x, in_min, in_max, out_min=0, out_max=255):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def convert_coordinates(point, old_width, old_height, new_width, new_heigth):
    width_ratio = point[0]/old_width
    height_ratio = point[1]/old_height

    return (int(width_ratio*new_width), int(height_ratio*new_heigth))


def getMap(points, boundaries, resolution):
    # a 2d array with a printable "map" of distance-values
    no_pixels_x = int(boundaries[0]/resolution)
    no_pixels_y = int(boundaries[1]/resolution)
    
    # convert points from coordinates to pixels
    for point in points:
        point = convert_coordinates(point, boundaries[0], boundaries[1], no_pixels_x, no_pixels_y)

    result = np.zeros((no_pixels_y, no_pixels_x), np.uint16)

    test = Image.open("/home/yannick/git-repos/MyPython/math programs/testImage.jpg")
    testarray = np.array(test)

    greatest_distance = 0
    for x in range(0, no_pixels_x):
        for y in range(0, no_pixels_y):
            current_sum_of_distance = 0
            for point in points:

                current_sum_of_distance += getDistance(point, (x,y))
            
            
            result[x, y] = current_sum_of_distance

            # at the end, greatest distance will equal the biggest current_sum_of_distance
            if current_sum_of_distance > greatest_distance:
                greatest_distance = current_sum_of_distance

    print(result)
    for x in range(0, no_pixels_x):
        for y in range(0, no_pixels_y):
            result[x,y] = map(result[x,y], 0, greatest_distance)

    print(result)        

    img = Image.fromarray(result, 'L')
    img.save('my.png')
    img.show()

    Image.fromarray(testarray, "RGB").save("/home/yannick/git-repos/MyPython/math programs/testImageNEU.jpg")

   
        



points = ((0,0), (3,0), (6,0))
getMap(points, (6,6), 1)
