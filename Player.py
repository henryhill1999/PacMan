from scene import float_coord_clear

# Player class - i.e. Pacman
class Player:
    def __init__(self, pix, piy, speed, keysDown):
        self.crd = [pix, piy]
        self.drc = 'RIGHT'
        
    # Check for keys being pressed, turn and move if necessary
    def update(self, scene, keysDown, speed):
        
        vels = {
            'LEFT': (-speed, 0),
            'RIGHT': (speed, 0),
            'UP': (0, -speed),
            'DOWN': (0, speed)}
        
        if len(keysDown):
            self.attemptTurn(*vels[keysDown[-1]], 
                             drc = keysDown[-1], scene=scene)
        
        self.attemptMoveForward(*vels[self.drc], scene=scene)
    
    # If the way is clear, move forward
    def attemptMoveForward(self, vx, vy, scene):
        if float_coord_clear(self.crd[0]+vx, self.crd[1]+vy, scene):
            self.crd[0] += vx
            self.crd[1] += vy    
            
        self.crd[0] = round(self.crd[0] % len(scene[0]),2)
        self.crd[1] = round(self.crd[1] % len(scene),2)
    
    # Turn only if the key with precedence leads to a path
    def attemptTurn(self, vx, vy, drc, scene): 
        if float_coord_clear(self.crd[0]+vx, self.crd[1]+vy, scene):
            self.drc = drc

    # Draw pacman
    def render(self, res, t):
        
        pushMatrix()
        
        n = res
        
        translate(n*self.crd[0],n*self.crd[1])
        
        fill(255,255,0)
        stroke(0,0,0,0)
        ellipse(0,0,n,n)
        
        if self.drc == 'DOWN':
            rotate(HALF_PI)
        elif self.drc == 'LEFT':
            rotate(PI)
        elif self.drc == 'UP':
            rotate(-HALF_PI)
        
        fill(0)
        triangle(  0,    0, 
                 n/2, -(t%50-25)/25.0 * (n/2),
                 n/2,  (t%50-25)/25.0 * (n/2))
        
        popMatrix()
