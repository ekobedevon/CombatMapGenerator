from multiprocessing.connection import wait
from time import sleep, time
import BlockRandomWalk as BRW
import imageGenerator as ig
import random as ran



new_map = BRW.Generate(20,5,10)

print(len(new_map))
print(len(new_map[0]))
ig.createDungeonPicture(40,new_map)

