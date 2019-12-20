from search import findOptimalPath

class Ghost:
    def __init__(self, pix, piy, target, col):
        self.crd =[pix, piy]
        self.drc = 'RIGHT'
        self.target = target
        self.col = col
        
    # Determine the ideal path for the ghost to follow, 
        # based on its position relative to Pacman.
        # update ghost to begin following this path
    def update(self, scene, keysDown, speed, pManPos):
        
        vels = {
            'LEFT': (-speed, 0),
            'RIGHT': (speed, 0),
            'UP': (0, -speed),
            'DOWN': (0, speed)}
    
        path = findOptimalPath(self.crd, self.target,scene)
        self.drc = path[0][1]
            
        v = vels[self.drc]
        self.crd[0] = round((self.crd[0]+v[0]) % len(scene[0]),2)
        self.crd[1] = round((self.crd[1]+v[1]) % len(scene),2)

    # draw ghost to the display
    def render(self, res, t):
        
        pushMatrix()
        
        n = res
        
        translate(n*self.crd[0],n*self.crd[1])
        
        # draw basic outline of body
        fill(*self.col)
        stroke(0,0,0,0)
        ellipse(0,0,2*n/3,n)
        rect(-n/3,0,2*n/3,n/2)
        
        # draw little triangles at the bottom
        pushMatrix()
        fill(0)
        stroke(0)
        translate(-n/3,n/3)
        triangle(0,n/6, 0,0, n/8,n/6)
        translate(n/8,0)
        triangle(0,n/6, n/8,0, n/4,n/6)
        translate(n/4,0)
        triangle(0,n/6, n/8,0, n/4,n/6)
        translate(n/4,0)
        triangle(0,n/6, n/8,0, n/8,n/6)
        popMatrix()
        
        # draw right eye
        pushMatrix()
        fill(255)
        stroke(0,0,0,0)
        translate(-n/8,-n/6)
        ellipse(0,0,n/6,n/4)
        
        if self.drc == 'RIGHT':
            translate(n/12,0)
        if self.drc == 'DOWN':
            translate(0,n/12)
        elif self.drc == 'LEFT':
            translate(-n/12,0)
        elif self.drc == 'UP':
            translate(0,-n/12)
        
        fill(0)
        ellipse(0,0,n/8,n/8)
        
        popMatrix()
        
        
        # draw left eye
        pushMatrix()
        fill(255)
        stroke(0,0,0,0)
        translate(n/8,-n/6)
        ellipse(0,0,n/6,n/4)
        
        if self.drc == 'RIGHT':
            translate(n/12,0)
        if self.drc == 'DOWN':
            translate(0,n/12)
        elif self.drc == 'LEFT':
            translate(-n/12,0)
        elif self.drc == 'UP':
            translate(0,-n/12)
        
        fill(0)
        ellipse(0,0,n/8,n/8)
        
        popMatrix()
        
        popMatrix()
