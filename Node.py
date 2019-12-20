# Node defines an intersection in the possible paths, 
    # and may contain information about that node in a 
    # particular path (e.g. its heuristic value)
class Node:
    def __init__(self, crd):
        self.crd = crd
        self.edges = set()
        self.pruned = False
        
        self.f = None
        self.g = None
        self.h = None
        
        self.parent = None
    
    def __repr__(self):
        if self.crd[0] % 1 == 0:
            self.crd[0]=int(self.crd[0])
        
        if self.crd[1] % 1 == 0:
            self.crd[1]=int(self.crd[1])
            
        return str(self.crd)
    
    def __lt__(self,other):
        return self.f < other.f
        
    def __hash__(self):
        return hash(self.__repr__())
    
    def __eq__(self, other):
        return (self.crd[0] == other.crd[0] and 
                self.crd[1] == other.crd[1])
    
