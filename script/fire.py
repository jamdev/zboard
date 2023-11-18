import time, random
from galactic import GalacticUnicorn

graphics = None
palette = None
colourscheme = "red"

# setup heat value buffer and fire parameters
width = GalacticUnicorn.WIDTH + 2
height = GalacticUnicorn.HEIGHT + 4
heat = [[0.0 for y in range(height)] for x in range(width)]
fire_spawns = 5
damping_factor = 0.97

def init():
    # a palette of five firey colours (white, yellow, orange, red, smoke)
    #todo - optimise different colours
    #todo - replace black with background colour
    global palette
    
    palette = {"brightred":[
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 20,  20,  20),
        graphics.create_pen(180,  30,   0),
        graphics.create_pen(220, 160,   0),
        graphics.create_pen(255, 255, 180)
    ],
    "red":[
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 5,  5,  5),
        graphics.create_pen(45,  8,   0),
        graphics.create_pen(55, 40,   0),
        graphics.create_pen(64, 64, 45)
    ],
    "green":[
        graphics.create_pen(  0,   0,   0),
        graphics.create_pen( 5,  5,  5),
        graphics.create_pen( 26, 51,   0),
        graphics.create_pen(0, 77,   26),
        graphics.create_pen(64, 64, 45)
    ]}

# returns the palette entry for a given heat value
@micropython.native  # noqa: F821
def pen_from_value(value):
    global colourscheme
    if value < 0.15:
        return palette[colourscheme][0]
    elif value < 0.25:
        return palette[colourscheme][1]
    elif value < 0.35:
        return palette[colourscheme][2]
    elif value < 0.45:
        return palette[colourscheme][3]
    return palette[colourscheme][4]

@micropython.native  # noqa: F821
def draw(cl): 
    global colourscheme 
    colourscheme = cl      
    # clear the the rows off the bottom of the display
    for x in range(width):
        heat[x][height - 1] = 0.0
        heat[x][height - 2] = 0.0
        
    # add new fire spawns
    for c in range(fire_spawns):
        x = random.randint(0, width - 4) + 2
        heat[x + 0][height - 1] = 1.0
        heat[x + 1][height - 1] = 1.0
        heat[x - 1][height - 1] = 1.0
        heat[x + 0][height - 2] = 1.0
        heat[x + 1][height - 2] = 1.0
        heat[x - 1][height - 2] = 1.0

    # average and damp out each value to create rising flame effect
    for y in range(0, height - 2):
        for x in range(1, width - 1):
            # update this pixel by averaging the below pixels
            average = (
                heat[x][y] + heat[x][y + 1] + heat[x][y + 2] + heat[x - 1][y + 1] + heat[x + 1][y + 1]
            ) / 5.0

            # damping factor to ensure flame tapers out towards the top of the displays
            average *= damping_factor

            # update the heat map with our newly averaged value
            heat[x][y] = average
           
    # render the heat values to the graphics buffer
    for y in range(GalacticUnicorn.HEIGHT):
        for x in range(GalacticUnicorn.WIDTH):
            graphics.set_pen(pen_from_value(heat[x + 1][y]))
            graphics.pixel(x, y)
