from cmath import log
import math
from multiprocessing.connection import wait
from time import sleep, time
from tkinter import Scale
import BlockRandomWalk as BRW
import imageGenerator as ig
import PySimpleGUI as sg
import image_viewer as iv







while(1):
    ppi = 40
    ten_factor = math.log(ppi,10)

    new_map = BRW.Generate(20,5,10)
    x_length = math.ceil(ppi * len(new_map[0]) / (2 ** ten_factor))
    y_length = math.ceil(ppi * len(new_map) / (2 ** ten_factor))

    new_img = ig.createDungeonPicture(ppi,new_map)

    preview = new_img.copy()



    preview = preview.resize((y_length,x_length))
    preview.save("preview.png")
    
    button_size = (4,1)
    
    button_layout = [[sg.Button("NEW",key="new",size=button_size)],[sg.Button("EXIT",key="exit",size=button_size)]]
    layout=[[sg.Image("preview.png",size=(y_length,x_length)),sg.Column(button_layout)]]
    window = sg.Window("Test Window",layout)

    events, values = window.read()
    window.close()
    if events == None:
        break
    if "exit" in events:
        break
    


