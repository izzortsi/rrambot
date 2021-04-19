##
import numpy.random as npr
##
class foo:
    def __init__(self):
        self.samples = []

    def populate(self, n):
        self.L = [bar(self, i) for i in range(n)]
    
    def get_things(self):
        return self.L

    def add_sample(self, sample):
        self.samples.append(sample)

class bar:
    def __init__(self, supobj, i):
        self.index = i
        self.supobj = supobj

    def sample_and_add(self):
        self.sample = npr.randn()
        self.supobj.samples.append(self.sample)


    

##

fu = foo()
##
fu.populate(10)
##
L = fu.get_things()
##
L[-1].sample_and_add()
L[-1].sample


##
fu.samples

##
