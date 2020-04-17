import csv
import graphviz

# WORK IN PROGRESS

class KlassRepo:
    def __init__(self):
        self.klasses = dict()
    
    def get(self, klass_name):
        klass = None
        if len(klass_name) > 0:
            if klass_name in self.klasses:
                klass = self.klasses[klass_name]
            else:
                klass = Klass(klass_name)
                self.klasses[klass_name] = klass
        return klass
    
    def build_complete_graph(self):
        edges = set()
        g = graphviz.Graph()
        for klass_name in self.klasses.keys():
            klass = self.klasses[klass_name]
            g.node(klass.name)
            for dep in klass.strong_dependencies().union(klass.weak_dependencies()):
                edges.add(frozenset({klass, dep}))
        self._add_edges(g, edges, True)
        
        g.render('deck/dependencies2', view=True)  

    def build_graph(self):
        strong_edges = set()
        weak_edges = set()
        g = graphviz.Graph()
        for klass_name in self.klasses.keys():
            klass = self.klasses[klass_name]
            if klass.superklass is not None:
                continue
            print(klass)
            g.node(klass.name)
            for dep in klass.strong_dependencies():
                strong_edges.add(frozenset({klass, dep.root()}))
            for dep in klass.weak_dependencies():
                weak_edges.add(frozenset({klass, dep.root()}))
        self._add_edges(g, strong_edges, True)
        self._add_edges(g, weak_edges, False)
        
        g.render('deck/dependencies', view=True)  

    def _add_edges(self, g, edges, strong = True):
        for edge in edges:
            i = iter(edge)
            x = next(i)
            y = next(i, x)
            if strong:
                g.edge(x.name, y.name)
            else:
                g.edge(x.name, y.name, style = 'dashed')

# Strong dependencies: dependencies of this class
# Weak dependencies: dependencies present only in one or more subclasses
class Klass:
    def __init__(self, name):
        self.strong_deps = set()
        self.weak_deps = set()
        self.name = name
        self.superklass = None
        self.subklasses = set()

    def __str__(self):
        if self.superklass is not None:
            return f'{self.name} ({self.superklass.name})'
        else:
            return self.name

    def root(self):
        if self.superklass is None:
            return self
        else:
            return self.superklass.root()

    def add_superklass(self, klass):
        if klass is None:
            return
        self.superklass = klass
        klass.subklasses.add(self)

    def add_dependency(self, klass, strong = True):
        if klass is None:
            return
        
        if self.superklass is not None:
            self.superklass.add_dependency(klass, False)

        if strong:
            self.strong_deps.add(klass)
            klass.strong_deps.add(self)
        else:
            self.weak_deps.add(klass)
            klass.weak_deps.add(self)

    def strong_dependencies(self):
        return self.strong_deps
    
    def weak_dependencies(self):
        return self.weak_deps - self.strong_deps

if __name__ == '__main__':
    filename = 'base-classes.csv'
    repo = KlassRepo()

    with open(filename) as file:
        # Load subclass/superclass relationship
        rows = csv.DictReader(file)
        for row in rows:
            klass = repo.get(row['class'])
            klass.add_superklass(repo.get(row['hierarchy']))

    with open(filename) as file:
        rows = csv.DictReader(file)
        for row in rows:
            klass = repo.get(row['class'])
            klass.add_dependency(repo.get(row['leftClass']))
            klass.add_dependency(repo.get(row['rightClass']))
            klass.add_dependency(repo.get(row['topClass']))
            klass.add_dependency(repo.get(row['bottomClass']))
        repo.build_graph()
        repo.build_complete_graph()
        
