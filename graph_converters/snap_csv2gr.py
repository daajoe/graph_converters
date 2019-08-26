#!/usr/bin/env python
import sys
from cStringIO import StringIO

import networkx as nx


class SymTab(object):
    symtab = {}
    last_atom = 0

    def atom_id(self, atom_name):
        if self.symtab.has_key(atom_name):
            return self.symtab[atom_name]
        else:
            self.last_atom += 1
            self.symtab[atom_name] = self.last_atom
            return self.last_atom


filename = sys.argv[1]
outputfilename = '%s.gr' % filename

graph = nx.Graph()

with open(filename) as fh:
    for line in fh.readlines():
        if line.startswith('#'):
            continue
        line = map(int, line.split(',')[:2])
        graph.add_edge(line[0], line[1])

s = SymTab()
ostream = StringIO()
for v, w in graph.edges():
    ostream.write("%s %s\n" % (s.atom_id(v), s.atom_id(w)))

with open(outputfilename, 'w') as ofh:
    ofh.write("p td %s %s\n" % (graph.number_of_nodes(), graph.number_of_edges()))
    ofh.write(ostream.getvalue())
    ofh.flush()
