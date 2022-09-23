import numpy as np
from PIL import Image
from math import sin, cos, sqrt, atan2
import requests
import json

DREISAM_UL = (48.154658, 7.615669)
DREISAM_LR = (47.861023, 8.055387)
UL_FUJI = (35.49495, 138.56429) # test coordinates
LR_FUJI = (35.24691, 138.88908)
SCALE_TEST = 1000 # meters per pixel
PATH = "/home/yannick/Pictures/"
MAX_API_CALLS = 1000000 # too large
POINTS_PER_ITERATION = 800

# upper_left_corner and lower_right_corner are real-world points forming the boundaries of the rectangular heightmap (latitude, longitude)
# scale is meters per pixel (limited by source data)
def make_heightmap(ul_corner,lr_corner, scale):

    distance_x = get_distance_between_coords(ul_corner, (ul_corner[0], lr_corner[1]))
    distance_y = get_distance_between_coords(ul_corner, (lr_corner[0], ul_corner[1]))
    print(distance_x)
    print(distance_y)
    pixels_x = distance_x//scale # integer division, fractions will be truncated
    pixels_y = distance_y//scale

    lat_steps = (ul_corner[0] - lr_corner[0]) / pixels_y # change in lat and lon per pixel
    lon_steps = abs((ul_corner[1] - lr_corner[1]) / pixels_x) # abs doesn't mess anything up if ul and lr are correct
    
    print(lat_steps)
    print(lon_steps)

    # safety stop
    if (pixels_y*pixels_x) > MAX_API_CALLS:
        # this doesn't prevent naturally large maps with reasonable scale, but only maps with unreasonable scale
        print("Scale is too small, this would have resulted in {0} individual pixels! (more than 1'000'000) ".format(pixels_x*pixels_y))
        return

    confirm = input("This will produce an image of {0}*{1} pixels with a total of {2} pixels, are you sure? (y/N) ".format(pixels_x, pixels_y, pixels_x*pixels_y))
    if confirm.upper() != "Y":
        return

    point_list = []
    for i_y in range(pixels_y):
        for i_x in range(pixels_x):
            point_list.append((ul_corner[0] - (lat_steps*i_y), ul_corner[1] + (lon_steps*i_x)))

    elevation = post_elevations(point_list)
    min_elevation = min(elevation)
    max_elevation = max(elevation)
    
    map_array = np.full((pixels_y,pixels_x), 0, dtype=np.uint8)
    main_i = 0
    for i_y in range(pixels_y):
        for i_x in range(pixels_x):
            # map values to a uint8 in order for Image.fromarray to work properly
            map_array[i_y, i_x] = map_range(elevation[main_i], min_elevation, max_elevation, 0, 255)

            main_i += 1

    heightmap = Image.fromarray(map_array, 'L')
    heightmap.show()
    
    heightmap.save("/home/yannick/Pictures/heightmaps/{0},{1},{2}.png".format(ul_corner[0], ul_corner[1], scale), format="PNG")

def post_elevations(point_list):
    iterations = ((len(point_list) - len(point_list)%POINTS_PER_ITERATION)//POINTS_PER_ITERATION) + 1
    all_temp_elevations = []
    point_i = 0
    for iteration_no in range(iterations):
        print(".", end="")
        temp_elevations = []
        data = {"locations": []}
        
        while point_i < (iteration_no+1) * POINTS_PER_ITERATION:
            if point_i >= len(point_list):
                break
            data["locations"].append({"latitude": point_list[point_i][0], "longitude": point_list[point_i][1]})
            point_i += 1

        json_data = json.dumps(data, indent=4)

        newHeaders = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.post("https://api.open-elevation.com/api/v1/lookup", data=json_data, headers=newHeaders)

        for result in response.json()["results"]:
            temp_elevations.append((result["elevation"]))
        
        all_temp_elevations.append(temp_elevations)
    
    elevations = []
    for temp_elevations in all_temp_elevations:
        for elevation in temp_elevations:
            elevations.append(elevation)
            
    return elevations

def map_range(val, in_min,in_max, out_min, out_max): # map val proportionally to new range
    return (val - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
    
def get_distance_between_coords(coord1, coord2): 
    # everything to 4 sf
    # source: https://www.movable-type.co.uk/scripts/latlong.html
    lat1 = coord1[0]
    lon1 = coord1[1]
    lat2 = coord2[0]
    lon2 = coord2[1]
    R = 6371000 # radius of the earth in metres
    PI = 3.142

    φ1 = lat1 * PI/180 # convert to radians  φ, λ in radians
    φ2 = lat2 * PI/180
    Δφ = (lat2-lat1) * PI/180
    Δλ = (lon2-lon1) * PI/180

    a = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a)) # angular distance 

    return int(round(R * c, 0)) # in whole metres


# For germany, a scale less than 100 meters doesn't give additional detail
make_heightmap(DREISAM_UL,DREISAM_LR, 100)

