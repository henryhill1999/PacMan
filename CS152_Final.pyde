from collections import defaultdict
from java.awt.event import KeyEvent
from java.lang.reflect import Modifier

from Ghost import Ghost
from Player import Player
from search import *
from scene import *

# These help determine which keys are pressed when
key_names = defaultdict(lambda: 'UNKNOWN')
for f in KeyEvent.getDeclaredFields():
    if Modifier.isStatic(f.getModifiers()):
        name = f.getName()
        if name.startswith("VK_"):
            key_names[f.getInt(None)] = name[3:]

# Set global constants
t = 0
    
SPEED = 0.05
keysDown = []
res = 30

x = False
p = True

ghosts = []

graphEdges = []
    
# This defines how the map will be set up
scene = [
    [x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x],
    [x,x,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,x,x],
    [x,x,p,x,x,x,p,x,x,x,x,x,p,x,x,x,p,x,x],
    [x,x,p,x,p,p,p,x,p,p,p,x,p,p,p,x,p,x,x],
    [x,x,p,x,p,x,p,x,p,x,p,x,p,x,p,x,p,x,x],
    [p,p,p,p,p,x,p,p,p,x,p,p,p,x,p,p,p,p,p],
    [x,x,p,x,x,x,p,x,x,x,x,x,p,x,x,x,p,x,x],
    [x,x,p,p,p,x,p,p,p,p,p,p,p,x,p,p,p,x,x],
    [x,x,p,x,p,x,p,x,x,x,x,x,p,x,p,x,p,x,x],
    [x,x,p,x,p,p,p,x,p,p,p,x,p,p,p,x,p,x,x],
    [x,x,p,x,p,x,p,x,p,x,p,x,p,x,p,x,p,x,x], 
    [p,p,p,p,p,x,p,p,p,x,p,p,p,x,p,p,p,p,p],
    [x,x,p,x,x,x,x,x,p,x,p,x,x,x,x,x,p,x,x],
    [x,x,p,p,p,p,p,p,p,p,p,p,p,p,p,p,p,x,x],
    [x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x]
]
    
# define canvas size and instantiate agents
def setup():
    global pman, ghosts, graphEdges
    
    size(res*(len(scene[0])-1),res*(len(scene)-1))
    
    pman = Player(2,5,SPEED,keysDown)
    
    vels = {
        'LEFT': (-1, 0),
        'RIGHT': (1, 0),
        'UP': (0, -1),
        'DOWN': (0, 1)}
        
    ghosts = [Ghost(12,5, target = pman.crd,col=(100,255,255)),
              Ghost(12,11, target = pman.crd,col=(255,200,100)),
              Ghost(2,11, target = pman.crd,col=(255,100,200))]

# main function: loops drawing of scene
def draw():
    global t, scene
    global pman, ghosts

    background(0)
    
    # draw the background 
    drawScene(scene, res)
    
    # update and draw the ghosts
    for g in ghosts:
        if (abs(pman.crd[0]-g.crd[0]) < 1 
            and abs(pman.crd[1]-g.crd[1]) < 1):
            exit()
    
        g.update(scene,keysDown,SPEED, (pman.crd[0],pman.crd[1]))
        g.render(res, t)
    # update and draw pacman
    pman.update(scene, keysDown, SPEED)
    pman.render(res, t)
    
    
    # increment the time step
    t+=1

ARROW_KEYS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
# when a key is pressed, update the global state
def keyPressed():
    global keysDown
    
    key_name = key_names[keyCode]
    
    if key == CODED and key_name in ARROW_KEYS and not key_name in keysDown:
        keysDown.append(key_name)

# when a key is released, update the global state
def keyReleased():
    global keysDown
    
    key_name = key_names[keyCode]
    
    if key == CODED and key_name in ARROW_KEYS and key_name in keysDown:
        keysDown.remove(key_name)
