import os

def nowpath(path=None):
    if path:
        currentpath = os.path.abspath(path)
    else:

        currentpath = os.path.abspath(__file__)
    print(currentpath)

def printout():
    print("hellloworld,changhao")




