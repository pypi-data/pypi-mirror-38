import numpy as np
import rdflib

path = '/Users/mehdi/PycharmProjects/PyKEEN/data/corpora/rdf.nt'
g = rdflib.Graph()
g.parse(path, format="nt")


for s, p, o in g:
    print(str(s))
    print(type(p))
    print(o)
    print('-----------')
    exit(0)
