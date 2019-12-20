class Edge:
    def __init__(self, adjNode, weight, drc):
        self.adjNode = adjNode
        self.weight = weight
        self.drc = drc
    
    def __hash__(self):
        return hash(self.__repr__())
    
    def __repr__(self):
        return 'To: {}, Weight: {}'.format(repr(self.adjNode),self.weight)
