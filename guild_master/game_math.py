import sys
FLOAT_MAX = sys.float_info.max
FLOAT_MIN = sys.float_info.min
INT_MAX = 2147483647
INT_MIN = -2147483648
#from math import pi  do I need this?

Warned = False

def is_on_course():
    global Warned
    if not Warned:
        print("Remember to set up a math function to see whether a fleet is on course!")
        Warned = True

    return True
