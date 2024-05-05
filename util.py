import math
import numpy as np

def string_to_seconds(str_time):
    total_seconds = 0
    if str_time != "" :
        values = str_time.split(":")
        
        for v in range(0, len(values)):
            sec = float(values[v]) * math.pow(60, (len(values) - v - 1))
            total_seconds += sec

    return(total_seconds)


def get_ranking(quartiles, value):
    rank = 0.01
    if value < quartiles[0]:
        rank = 1
    elif value < quartiles[1]:
        rank = 2
    elif value < quartiles[2]:
        rank = 3
    else:
        rank = 4
    return(rank)

