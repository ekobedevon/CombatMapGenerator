from multiprocessing.connection import wait
from time import sleep, time
import BlockRandomWalk as BRW
import imageGenerator as ig
import random as ran



new_map = BRW.Generate(20,5,10)
ig.createDungeonPicture(40,new_map)

new_map = BRW.makeSymetric(new_map,3)

ig.createDungeonPicture(40,new_map)

