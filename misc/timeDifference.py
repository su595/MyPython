#!/bin/python

# input are two timestamps (eg. Sun 10 May 2015 13:54:36 -0700)

import math
import os
import random
import re
import sys

YEAR_TO_S = 31536000
MONTH_TO_S =2628000
DAY_TO_S = 86400
HOUR_TO_S = 3600
MIN_TO_S = 60

def timeDifference(t1, t2):
    hours = int(t1[16] + t1[17])
    minutes = int(t1[19] + t1[20])
    secs = int(t1[22] + t1[23])
    
    timezone = int(t1[26] + t1[27]) * 60 # in minutes
    timezone += int(t1[28]) * 10
    timezone *= MIN_TO_S
    if(t1[25] == "-"):
        timezone *= -1
    time1 = hours * HOUR_TO_S + minutes * MIN_TO_S + secs + timezone
    
    hours = int(t2[16] + t2[17])
    minutes = int(t2[19] + t2[20])
    secs = int(t2[22] + t2[23])
    
    timezone = int(t2[26] + t2[27]) * 60 # in minutes
    timezone += int(t2[28]) * 10
    timezone *= MIN_TO_S
    if(t2[25] == "-"):
        timezone * -1
    print(timezone)

    time2 = hours * HOUR_TO_S + minutes * MIN_TO_S + secs + timezone
    
    delta = time1 - time2
    
    return delta

def dateDifference(t1, t2):
    day1 = int(t1[4] + t1[5])
    month1 = monToInt(t1[7] + t1[8] + t1[9])
    year1 = int(t1[11] + t1[12] + t1[13] + t1[14])
    day2 = int(t2[4] + t2[5])
    month2 = monToInt(t2[7] + t2[8] + t2[9])
    year2 = int(t2[11] + t2[12] + t2[13] + t2[14])
    
    delta = (day1 - day2) * DAY_TO_S
    delta += (month1- month2) * MONTH_TO_S
    delta += (year1 - year2) * YEAR_TO_S
    
    return delta
  
def monToInt(month):
    if(month == "Jan"):
        return 1
    if(month == "Feb"):
        return 2
    if(month == "Mar"):
        return 3
    if(month == "Apr"):
        return 4
    if(month == "May"):
        return 5
    if(month == "Jun"):
        return 6
    if(month == "Jul"):
        return 7
    if(month == "Aug"):
        return 8
    if(month == "Sep"):
        return 9
    if(month == "Okt"):
        return 10
    if(month == "Nov"):
        return 11
    if(month == "Dec"):
        return 12
    return 0
    
  
# Complete the time_delta function below.
def time_delta(t1, t2):
    return str(abs(timeDifference(t1, t2) + dateDifference(t1,t2)))

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(raw_input())

    for t_itr in xrange(t):
        t1 = raw_input()

        t2 = raw_input()

        delta = time_delta(t1, t2)

        fptr.write(delta + '\n')

    fptr.close()
