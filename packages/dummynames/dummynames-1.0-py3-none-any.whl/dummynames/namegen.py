import random
import os

_path = os.path.dirname(__file__)

f = open(os.path.join(_path, "names"), "r")
names = f.readlines()
f.close()
names = list(map(lambda x: x[:-1], names))

f = open(os.path.join(_path, "adjs"), "r")
adjs = f.readlines()
f.close()
adjs = list(map(lambda x: x[:-1], adjs))

def generate_fullname():
    return random.choice(adjs) + " " + random.choice(names)

def generate_firstname():
    return random.choice(names)

def generate_lastname():
    return random.choice(adjs)
