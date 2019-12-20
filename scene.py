# draws the background, based on a list describing the 
    # layout of the game
def drawScene(scene, res):
    
    w = len(scene[0])
    h = len(scene)
    
    # takes scene matrix and draws walls
    for i in range(w*h):
        
        if int(i/w) == len(scene)-1 or i%w == len(scene[0])-1:
            continue
        
        pushMatrix()
        translate(res*(i%w), res*int(i/w))
        
        draw_four(scene[int(i/w)][i%w],
                  scene[int(i/w)][i%w+1],
                  scene[int(i/w)+1][i%w+1],
                  scene[int(i/w)+1][i%w],
                  res)
        
    
        popMatrix()
    
# helper method which generates a tile, based on four adjacent blocks
def draw_four(tl,tr,br,bl, n):
    qts = [tl,tr,br,bl]
        
    fill(0,0,0,0)
    stroke(50,180,200)
    
    pushMatrix()    
    if sum(1 for x in qts if x) == 1:
        if tr:
            rotate(HALF_PI)
            translate(0,-n)
        
        elif br:
            rotate(PI)
            translate(-n,-n)
            
        elif bl:
            rotate(-HALF_PI)
            translate(-n,0)
        
        curve(0, -3*n/2,    n/2,   0,
              0,    n/2, -3*n/2,   0)
    
    elif sum(1 for x in qts if x) == 2:
        
        if tr and tl or br and bl:
            line(0,n/2,n,n/2)
        else:
            line(n/2,0,n/2,n)
        
    elif sum(1 for x in qts if x) == 3:
        if not tr:
            rotate(HALF_PI)
            translate(0,-n)
        
        elif not br:
            rotate(PI)
            translate(-n,-n)
            
        elif not bl:
            rotate(-HALF_PI)
            translate(-n,0)
        
        curve(0, -3*n/2,    n/2,   0,
              0,    n/2, -3*n/2,   0)
        
    popMatrix()

# check if floating point coordinates provided is clear by 
# checking all adjacent blocks
def float_coord_clear(x,y, scene):

    if (not scene[floor(y)][floor(x)%len(scene[0])] or
        not scene[floor(y)][ceil(x)%len(scene[0])] or
        not scene[ceil(y)][ceil(x)%len(scene[0])] or
        not scene[ceil(y)][floor(x)%len(scene[0])]):
        return False
    
    return True
