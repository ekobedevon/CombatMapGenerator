import string
from PIL import Image, ImageDraw
import math

def createDungeonPicture(ppi:int = 50,map_array = None):
    size_x = ppi * len(map_array)
    size_y = ppi * len(map_array[0])
    img = Image.new( 'RGB', (size_x,size_y), "black") # create a new black image
    pixels = img.load() # create the pixel map 
    for index_x, x in enumerate(map_array):
        for index_y,y in enumerate(x):
            if y==1 or y == 2:
                for x_pixel in range(ppi):
                    for y_pixel in range(ppi):
                        pixels[index_x*ppi + x_pixel,index_y*ppi +y_pixel] = (112, 112, 112) # wall grey
            if y==3:
                for x_pixel in range(ppi):
                    for y_pixel in range(ppi):
                        pixels[index_x*ppi + x_pixel,index_y*ppi +y_pixel] = (255,255,255) # white
            if y==5:
                for x_pixel in range(ppi):
                    for y_pixel in range(ppi):
                        pixels[index_x*ppi + x_pixel,index_y*ppi +y_pixel] = (107, 80, 47) # doors
    
    current_spot = ppi
    while current_spot < size_x:
        for x in range(math.floor(ppi/15)):
            for y in range(size_y):
                pixels[current_spot-x,y] = (0,0,0)
                
        current_spot += ppi
    current_spot = ppi
    while current_spot < size_y:
        for x in range(math.floor(ppi/15)):
            for y in range(size_x):
                pixels[y,current_spot-x] = (0,0,0)
        current_spot += ppi

    img.show()