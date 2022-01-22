import math
import random as ran

def create_array(dimension:int = 40):
    array_base = []
    array_2d = []
    for x in range(0,dimension):
        array_base = []
        for y in range(0,dimension):
            array_base.append(0)
        array_2d.append(array_base)
    return array_2d

def addRoom(cord:list,size:list,base_map:list[list]):
    for x in range(1,size[0]-1): #for each x that is not on the edge minimum size of 3
        base_map[cord[0]+x][cord[1]] += 1 #add to the top wall
        base_map[cord[0]+x][cord[1]+size[1]-1] += 1 #add one to bottom wall
        for mid in range(cord[1]+1,cord[1]+size[1]-1): #for all spaces inbetween
            base_map[cord[0]+x][mid] = 4
        
    for y in range(size[1]): #for east and west wall, each y
        base_map[cord[0]][cord[1]+y] +=1 #add one to the west wall
        base_map[cord[0]+size[0]-1][cord[1]+y] +=1 #add one to the west wall
        
def validCheck(cord:list,size:list,base_map:list[list]):
    if(cord[0]+size[0] >= len(base_map) or cord[1]+size[1] >= len(base_map)): # if the coordinate would be out of bonds
        return -1
    
    for x in range(1,size[0]-1): #for each x that is not on the edge minimum size of 3
        if base_map[cord[0]+x][cord[1]] +1 >= 4 or base_map[cord[0]+x][cord[1]+size[1]-1] + 1 >= 4: #if greater than 3, meaning it is either a intersecting wall or a middle area
            return 0
    for y in range(size[1]): #for east and west wall, each y
        if base_map[cord[0]][cord[1]+y] +1 >= 3 or  base_map[cord[0]+size[0]-1][cord[1]+y] +1 >= 3: #same as above checking side walls now
            return 0
        
    return 1

def getCords(size:list,base_map:list[list]): #function to get cordinates for the 
    x = math.floor(len(base_map)/2)
    y = math.floor(len(base_map)/2) #starting in the middle of the grid
    directions = [[0,1],[1,0],[0,-1],[-1,0]]
    previous = ran.choice(directions)
    next_direction  = ran.choice(directions)
    valid = 0
    while(valid == 0): # while cordinates are invalid
        next_direction  = ran.choice(directions)
        while(next_direction[0] == -previous[0] & next_direction[1] == -previous[1]): #while pointed back
            next_direction  = ran.choice(directions)
        x += next_direction[0]
        y += next_direction[1]
        valid = validCheck([x,y],size,base_map) #returns if coordinates are valid or not
        if valid == -1:
            x = math.floor(len(base_map)/2)
            y = math.floor(len(base_map)/2)
            valid = 0
            
        previous = next_direction
        
    return [x,y]

def getBestFit(size:list,base_map:list[list],cords:list[list]):
    """ Given a series of valid cordinates, will return the position with the most wall shared between two rooms

    Args:
        size (list): the x and y size of the room given as [x,y]
        base_map (list[list]): the current map array
        cords (list[list]): a list of all cordinates that are valid for the room generated using random walk
        
    Returns:
        cords (list): The cords with the highest value to create the most overlap between rooms
    """
    """for x in range(1,size[0]-1): #for each x that is not on the edge minimum size of 3
        if base_map[cord[0]+x][cord[1]] +1 >= 3 or base_map[cord[0]+x][cord[1]+size[1]-1] + 1 >= 3: #if greater than 3, meaning it is either a intersecting wall or a middle area
            return 0
    for y in range(size[1]): #for east and west wall, each y
        if base_map[cord[0]][cord[1]+y] +1 >= 3 or  base_map[cord[0]+size[0]-1][cord[1]+y] +1 >= 3: #same as above checking side walls now
            return 0"""
    heaviest_cords = [0,0] #empty coords
    h_weight = -1 # weight of the current cords
    for cord_set in cords:
        weight = 0
        for x in range(1,size[0]-1): #for each x that is not the edge
            weight += base_map[cord_set[0]][cord_set[1]] + 1 # top edge
            weight += base_map[cord_set[0]+x][cord_set[1]+size[1]-1] + 1 # bottom edge
        for y in range(size[1]):
            weight += base_map[cord_set[0]][cord_set[1]+y] +1 # add left wall
            weight += base_map[cord_set[0]+size[0]-1][cord_set[1]+y] +1 #add right wall
        if weight > h_weight:
            heaviest_cords = cord_set
            h_weight = weight
    
    return heaviest_cords
    
    
        
def getBestFitCords(size:list,base_map:list[list]):
    random_cords = []
    for x in range(5):
        random_cords.append(getCords(size,base_map)) # run 5 trials of best fit, don't worry about repeat results
        
    best_cords = getBestFit(size,base_map,random_cords)
    return best_cords
        
        
def stripDown(base_array:list[list]):
    x_size = 0;
    y_size = 0;
    min_x = len(base_array)
    min_y = len(base_array)
    max_x = 0
    max_y = 0
    
    for x in range(len(base_array)):
        for y in range(len(base_array)):
            if(base_array[x][y] != 0):
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
                if x < min_x:
                    min_x = x
                    
    x_size = max_x - min_x + 1
    y_size = max_y - min_y + 1
    new_map = []
    for x in range(x_size):
        temp = []
        for y in range(y_size):
            temp.append(base_array[min_x+x][min_y+y])
        new_map.append(temp)
    
    return new_map

def makeDoors(base_array:list[list]):
    x_walls = []
    y_walls = []
    save = False
    doors = []
    
    temp_list = []
    for x in range(len(base_array)):
        for y in range(len(base_array[0])):
            if base_array[x][y] == 2: #if it is a door in this row
                temp_list.append([x,y])
            elif len(temp_list) > 2: #if the list is less than 2 than no doors, secret room
                doors.append(temp_list)
                temp_list= []
                
    return doors
                
                
    
    
    
    
def Generate(room_amount:int,min_length:int,max_length:int):
    room_data = []
    bitsMap = []

    for x in range(room_amount):
        room_data.append([ran.randint(min_length,max_length),ran.randint(min_length,max_length)]) 

    xlen = 0;
    ylen = 0;
    for room in room_data:
        xlen += room[0]
        ylen += room[1]
        
        
    if xlen > ylen: #to never be out of bounds create a new array assuming all rooms were edge to edge
        bitsMap = create_array(2*xlen)
    else:
        bitsMap = create_array(2*ylen)

    for room in room_data:
        room_cords = getBestFitCords(room,bitsMap)
        addRoom(room_cords,room,bitsMap)

    new_map = stripDown(bitsMap)
    doors = makeDoors(new_map)

    for x in doors:
        middleIndex = math.ceil((len(x) - 1)/2)
        coordinate = x[middleIndex]
        new_map[coordinate[0]][coordinate[1]] = 5

    return new_map