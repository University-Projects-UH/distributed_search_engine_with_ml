import math
import functools

class DocVector: 
    def __init__(self, vector: dict = {}):
        self.vector = vector


    def values(self):
        return self.vector.values()

    
    def calculate_norm(self):
        self.norm = math.sqrt(functools.reduce(lambda a, b: a + (b * b), self.values(), 0))

    
    def __add__(self, other):
        new_vector = DocVector()
        
        for term in self.vector:
            try:
                new_vector[term] += self.vector[term]
            except:
                new_vector[term] = self.vector[term]

        for term in other:
            try:
                new_vector[term] += other[term]
            except:
                new_vector[term] = other[term]
        
        return new_vector

    
    # scalar multiplication
    def __mul__(self, value):
        new_vector = DocVector()
        for term in self.vector:
            new_vector[term] = self.vector[term] * value

        return new_vector 
    
    
    def __sub__(self, other):
        return self.__add__(other * -1)

    
    def __iter__(self):
        return self.vector.__iter__()

    
    def __contains__(self, value):
        return self.vector.__contains__(value)

    
    def __len__(self):
        return len(self.vector)

    
    def __getitem__(self, value):
        return self.vector[value]

    
    def __setitem__(self, key, value):
        self.vector[key] = value

