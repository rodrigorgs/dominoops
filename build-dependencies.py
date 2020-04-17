import csv
import graphviz
import copy
from collections import defaultdict

class KlassRepo:
    def __init__(self):
        self.klasses = dict()
        self.dependencies = set()
    
    def get_dependency(self, klass1, klass2, inferred = False):
        dep = Dependency(klass1, klass2, inferred)
        self.dependencies.add(dep)
        return dep

    def get_klass(self, klass_name):
        klass = None
        if len(klass_name) > 0:
            if klass_name in self.klasses:
                klass = self.klasses[klass_name]
            else:
                klass = Klass(klass_name, self)
                self.klasses[klass_name] = klass
        return klass
    
    def root_classes(self):
        return set([k for k in self.klasses if k.is_root()])

    def print_degrees(self):
        degrees = defaultdict(lambda: 0, dict())
        for dep in self.dependencies:
            degrees[dep.origin.name] += 1
            degrees[dep.destination.name] += 1
        res = list(degrees.items())
        res.sort(key = lambda x: x[1])
        for x in res:
            print(str(x[1]) + " - " + x[0])

    # Solid line: explicit dependency (uses the declared attribute type)
    # Dashed line: implicit dependency (dependency between a class and
    #   the subclasses of the declared attribute types)
    def build_complete_graph(self):
        edges = set()
        g = graphviz.Digraph()
        for klass_name in self.klasses.keys():
            klass = self.klasses[klass_name]
            g.node(klass.name)
            for dep in klass.outgoing_dependencies():
                edges.add(dep)
        
        for dep in edges:
            style = 'dashed' if dep.inferred else 'solid'
            g.edge(dep.origin.name, dep.destination.name, style = style)
        
        g.render('deck/dependencies-complete', view=True)  

    # Solid line: dependency valid for class and all its subclasses
    # Dashed line: dependency valid for some subclasses only
    # Label: class name (+ number of descendants)
    def build_condensed_graph(self):
        edges = set()
        subclass_edges = set()
        g = graphviz.Digraph()
        for klass_name in self.klasses.keys():
            klass = self.klasses[klass_name]
            if klass.is_root():
                num_descendants = len(klass.descendants())
                g.node(klass.name, label = f'{klass.name} (+{num_descendants})')
            for dep in klass.outgoing_dependencies():
                dep2 = copy.copy(dep)
                dep2.origin = dep2.origin.root()
                dep2.destination = dep2.destination.root()
                dep2.inferred = False
                if dep2 in self.dependencies or dep2.dependency_with(inferred = True) in self.dependencies:
                    edges.add(dep2)
                else:
                    dep2.inferred = True
                    subclass_edges.add(dep2)
        
        for dep in edges:
            g.edge(dep.origin.name, dep.destination.name, style = 'solid')
        for dep in subclass_edges:
            g.edge(dep.origin.name, dep.destination.name, style = 'dashed')

        g.render('deck/dependencies-condensed', view=True)  

class Dependency:
    def __init__(self, origin = None, destination = None, inferred = False):
        self.origin = origin
        self.destination = destination
        self.inferred = inferred
    
    def dependency_with(self, inferred):
        dep = copy.copy(self)
        dep.inferred = inferred

    def __eq__(self, other):
        return self.origin == other.origin and self.destination == other.destination and self.inferred == other.inferred
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return 1

class Klass:
    def __init__(self, name, repo):
        self.explicit_deps = set()
        self.name = name
        self.superklass = None
        self.subklasses = set()
        self.repo = repo

    def __str__(self):
        if self.superklass is not None:
            return f'{self.name} ({self.superklass.name})'
        else:
            return self.name

    def is_root(self):
        return self.superklass is None

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
        self.explicit_deps.add(self.repo.get_dependency(self, klass, False))
        
    def descendants(self):
        res = set()
        for sub in self.subklasses:
            res.add(sub)
            res = res.union(sub.descendants())
        return res

    def outgoing_dependencies(self):
        res = set() #.union(self.explicit_deps)
        for dep in self.explicit_deps:
            res.add(dep)
            for desc in dep.destination.descendants():
                res.add(self.repo.get_dependency(self, desc, True))
        return res

if __name__ == '__main__':
    filename = 'base-classes.csv'
    repo = KlassRepo()

    with open(filename) as file:
        # Load subclass/superclass relationship
        rows = csv.DictReader(file)
        for row in rows:
            klass = repo.get_klass(row['class'])
            klass.add_superklass(repo.get_klass(row['hierarchy']))

    with open(filename) as file:
        rows = csv.DictReader(file)
        for row in rows:
            klass = repo.get_klass(row['class'])
            klass.add_dependency(repo.get_klass(row['leftClass']))
            klass.add_dependency(repo.get_klass(row['rightClass']))
            klass.add_dependency(repo.get_klass(row['topClass']))
            klass.add_dependency(repo.get_klass(row['bottomClass']))
        repo.build_condensed_graph()
        repo.build_complete_graph()
        repo.print_degrees()
        
