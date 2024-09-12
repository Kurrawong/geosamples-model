import sys
import os
from rdflib import Graph

print(sys.argv[1])
g = Graph().parse(sys.argv[1])
# os.truncate(sys.argv[0])
open(sys.argv[1], "w").write(g.serialize(format="longturtle"))
