from math import floor

def secondsToTimeString(secs):
    m = floor(secs)//60
    s = floor(secs) - 60*m
    s1 = s//10
    s0 = s%10
    return f"{m}:{s1}{s0}"