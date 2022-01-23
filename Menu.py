import math
import os
import BlockRandomWalk as BRW
import imageGenerator as ig
import PySimpleGUI as sg
from random import randint
sg.theme("Dark Amber")

def GenerateUniqueName(file_name: str,file_set: set,file_extension: str = ""):
    while len({file_name + file_extension}.intersection(file_set)):
        file_name += hex(randint(0,15)).removeprefix("0x")#keeps adding hex values to file name unitl it is unique
    return file_name + file_extension




room_amount  = 10
min_length = 5
max_length = 10
ppi = 40
sym = 0
sym_h = False
sym_v = False
sym_value = 0




while(1):
    ten_factor = math.log(ppi,10)

    new_map = BRW.Generate(room_amount,min_length,max_length)
    if sym_v and sym_h :
        sym_value = 3
    elif(sym_h):
        sym_value = 2
    elif sym_v :
        sym_value = 1
    else:
        sym_value = 0
        
    new_map = BRW.makeSymetric(new_map,sym_value)
        
    
    
    x_length = math.ceil(ppi * len(new_map[0]) / (2 ** ten_factor))
    y_length = math.ceil(ppi * len(new_map) / (2 ** ten_factor))

    new_img = ig.createDungeonPicture(ppi,new_map)

    preview = new_img.copy()
    preview = preview.resize((y_length,x_length))
    preview.save("preview.png")
    
    


    button_size = (4,1)
    slider_layout = [[sg.Text("Room Amount: ")],[sg.Slider((1,100),room_amount,orientation='h',key="Room Amount")],
                     [sg.Text("Minimum Room Length: ")],[sg.Slider((5,20),min_length,orientation='h',key="Min_length")],
                     [sg.Text("Max Room Length: ")],[sg.Slider((5,20),max_length,orientation='h',key="Max_length")],
                     [sg.Text("Pixels Per Inch: ")],[sg.Slider((10,100),ppi,orientation='h',key="PPI",resolution=10)]]
    slider_layout = [[sg.Frame("Slider",slider_layout)]]
    
    button_layout = [[sg.Button("NEW",key="new",size=button_size),
                      sg.Button("SAVE",key="save",size = button_size),
                      sg.Button("EXIT",key="exit",size=button_size)]]
    check_layout = [[sg.CB("Horizontal",default=sym_h,key="sym_h")],[sg.CB("Vertical",default=sym_v,key="sym_v")]]
    check_layout = [[sg.Frame("Symmetry",check_layout)]]
    
    
    column_layout = [[sg.Column(slider_layout)],[sg.Column(check_layout)],[sg.Column(button_layout)]]
    layout=[[sg.Frame("Map Preview, 50% actual size",layout=[[sg.Image("preview.png",size=(y_length,x_length))]]),sg.Column(column_layout)]]
    window = sg.Window("Combat Map Generator",layout)

    events, values = window.read()    
    
    window.close()
    if events == None:
        break
    elif "exit" in events:
        break
    elif "save" in events:
        file_name = ""
        for x in range(5):
            file_name += hex(randint(0,15)).removeprefix("0x")#keeps adding hex values to file name unitl it is unique
        file_name = GenerateUniqueName(file_name,os.listdir(),".png")
        new_img.save(file_name)
        
    
    room_amount = int(values["Room Amount"])
    min_length = int(values["Min_length"])
    max_length = int(values["Max_length"])
    ppi = int(values["PPI"])
    sym_h = values["sym_h"]
    sym_v = values["sym_v"]
    
    if max_length <= min_length:
        min_length = max_length-1
        
        

os.remove("preview.png")