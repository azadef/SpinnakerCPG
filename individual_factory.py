import numpy as np

class Individual:
    def __init__(self, config, mutationProbability, params=None):
        self.mutationProbability = mutationProbability
        self.config = config
        self.error = -1

        if params is None:
            self.variables = {}

            for [name, min_val, max_val] in config:
                self.variables[name] = np.random.uniform(min_val, max_val)
        else:
            self.variables = params

    def get(self, name):
        return self.variables[name]
    def set(self, name, value):
        self.variables[name] = value
    def mutate(self):
        for [name, min_val, max_val] in self.config:
            if (np.random.uniform(0,1) < self.mutationProbability):
                self.variables[name] += np.random.uniform(min_val,max_val)
                if self.variables[name] > max_val:
                    self.variables[name] = max_val
                if self.variables[name] < min_val:
                    self.variables[name] = min_val
    def crossover(self, other):
        child = Individual(self.config, self.mutationProbability)
        for [name, min_val, max_val] in self.config:
            child.set(name,(self.get(name)+other.get(name))/2)
        child.mutate()
        return child
    def crossover_alt(self, other):
        child = Individual(self.config, self.mutationProbability)
        for [name, min_val, max_val] in self.config:
            if (np.random.uniform(0,1) < 0.5):
                child.set(name,self.get(name))
            else:
                child.set(name,other.get(name))
        child.mutate()
        return child
    def __repr__(self):
        return repr(self.variables)

class IndividualFactory:

    def __init__(self, mutationProbability):
        self.mutationProbability = mutationProbability
        self.variables = []
    def addVariable(self, name, min_val, max_val):
        self.variables.append([name, min_val, max_val])
    def getIndividual(self):
        return Individual(self.variables, self.mutationProbability)