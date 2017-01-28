import pygame, sys
from pygame.locals import *

import time

from random import randint

# Mark constants to describe map
DIRT = 0
GRASS = 1
MAC = 2

# Manual tilemap
tilemap = [
    [GRASS,DIRT, DIRT, DIRT, GRASS,DIRT, GRASS],
    [GRASS,DIRT, DIRT, GRASS,DIRT, DIRT, DIRT ],
    [DIRT, DIRT, DIRT, DIRT, DIRT, GRASS,DIRT ],
    [GRASS,GRASS,DIRT, MAC,  DIRT, DIRT, GRASS],
    [DIRT, DIRT, DIRT, DIRT, DIRT, DIRT, DIRT ],
    [DIRT, DIRT, GRASS,DIRT, DIRT, GRASS,GRASS],
    [GRASS,GRASS,GRASS,GRASS,GRASS,GRASS,GRASS]
    ]

# Tilemap generator

# Initialize all as dirt based on map size
MAPSIZE = 15
tilemap = [[DIRT]*MAPSIZE for x in range(MAPSIZE)]

# Disperse proportion of grass
grass_percentage = 0.25 # 10% grass coverage

for grass_loop in range(int(round((len(tilemap)*len(tilemap[0]))*grass_percentage))):
    tilemap[randint(0,len(tilemap)-1)][randint(0,len(tilemap[0])-1)] = GRASS

# Add Mac
tilemap[randint(0,len(tilemap)-1)][randint(0,len(tilemap[0])-1)] = MAC

# Tilemap colours RGB
BROWN = (153,76,0)
GREEN = (0,255,0)
GRAY = (128,128,128)

# Dictionary linking tilemap colors to tiles
colours = {
    DIRT  : BROWN,
    GRASS : GREEN,
    MAC   : GRAY
    }

# Game dimensions
TILESIZE = 40
MAPWIDTH = len(tilemap)
MAPHEIGHT = len(tilemap[0])

# Set up game display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

# Import eating sound
pygame.mixer.music.load("Bite.wav")
crunch = False

while True:

    # Get user events
    for event in pygame.event.get():
        # For quitting
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Draw the map based on tiles

    # For each row
    for row_loop in range(MAPHEIGHT):

        # For each column
        for column_loop in range(MAPWIDTH):

            # Draw the resources specified
            pygame.draw.rect(DISPLAYSURF, colours[tilemap[row_loop][column_loop]], (column_loop*TILESIZE,row_loop*TILESIZE,TILESIZE,TILESIZE))

    # Update display after re-mapping
    pygame.display.update()

    # Crunch if Mac ate grass
    if (crunch == True):
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

    # Slow graphic update for animated movement
    time.sleep(0.1)

    dirt_list = []
    # Move to closest City-block distance space
    # Step 1: Check for all dirt locations
    for row_loop in range(len(tilemap)):
        for column_loop in range(len(tilemap[0])):
            if tilemap[row_loop][column_loop]==1:
                dirt_list.append([row_loop,column_loop])
            if tilemap[row_loop][column_loop]==2:
                mac_position = [row_loop,column_loop]
        
        # Step 2 calculate closest point from list
        
    closest_location = [0,0]
    closest_distance = -1
        
    for dirt_distance_loop in range(len(dirt_list)):
        city_block_distance = abs(dirt_list[dirt_distance_loop][0]-mac_position[0])+abs(dirt_list[dirt_distance_loop][1]-mac_position[1])
        if (city_block_distance<closest_distance) or (closest_distance==-1):
            closest_distance = city_block_distance
            closest_location = dirt_list[dirt_distance_loop]

    # Auto-close if no more grass to eat
    if (closest_distance == -1):
        #input("Hungry Mac ate all the grass! Press Enter to quit...")
        time.sleep(1)
        pygame.quit()
        sys.exit()
        
    # Determine next movement based on closest point
    crunch = False
    if (closest_location[0]<mac_position[0]):
        tilemap[mac_position[0]][mac_position[1]] = DIRT
        if (tilemap[mac_position[0]-1][mac_position[1]]==GRASS):
            crunch = True
        tilemap[mac_position[0]-1][mac_position[1]] = MAC
    elif(closest_location[0]>mac_position[0]):
        tilemap[mac_position[0]][mac_position[1]] = DIRT
        if (tilemap[mac_position[0]+1][mac_position[1]]==GRASS):
            crunch = True
        tilemap[mac_position[0]+1][mac_position[1]] = MAC
    elif(closest_location[1]<mac_position[1]):
        tilemap[mac_position[0]][mac_position[1]] = DIRT
        if (tilemap[mac_position[0]][mac_position[1]-1]==GRASS):
            crunch = True
        tilemap[mac_position[0]][mac_position[1]-1] = MAC
    else:
        tilemap[mac_position[0]][mac_position[1]] = DIRT
        if (tilemap[mac_position[0]][mac_position[1]+1]==GRASS):
            crunch = True
        tilemap[mac_position[0]][mac_position[1]+1] = MAC
