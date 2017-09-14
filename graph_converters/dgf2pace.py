#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016
# Johannes K. Fichte, TU Wien, Austria
#
# gtfs2graphs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.  gtfs2graphs is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.  You should have received a copy of the GNU General Public
# License along with gtfs2graphs.  If not, see
# <http://www.gnu.org/licenses/>.

from optparse import OptionParser
import select
from sys import stderr, stdin, stdout
import networkx as nx

fromfile=True
if select.select([stdin,],[],[],0.0)[0]:
    inp=stdin
    fromfile=False
else:
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='filename',
                  help='Input file', metavar='FILE')
    (options, args) = parser.parse_args()
    if not options.filename:
        stderr.write('Missing filename')
        parser.print_help(stderr)
        stderr.write('\n')
        exit(1)
    inp = open(options.filename, 'r')
    fromfile=True

G = nx.Graph()

for line in inp.readlines():
    line=line.split()
    if line==[]:
        continue
    if line[0] == 'c':
        stdout.write('%s\n' %' '.join(line))
        continue
    if line[0]!='p':
        G.add_edge(int(line[1]), int(line[2]))

#print nx.number_of_nodes(G)
#
#trivial preprocessing
changed = True
while changed:
    changed = False
    for v in list(G.nodes_iter()):
        if len(G.neighbors(v))<=1:
            G.remove_node(v)
            changed = True
            continue
        if len(G.neighbors(v))==2:
            v1,v2=G.neighbors(v)
            G.add_edge(v1,v2)
            G.remove_node(v)
            #G.remove_edge(v,v1)
            #G.remove_edge(v,v2)
            changed = True
            continue

#from cStringIO import StringIO
#out = StringIO()
#nx.write_gml(G,out)
#stdout.write(out.getvalue())

G=nx.convert_node_labels_to_integers(G)

stdout.write('p tw %s %s\n' %(nx.number_of_nodes(G),nx.number_of_edges(G)))
for u,v in G.edges_iter():
    stdout.write('%s %s\n' %(u+1,v+1))

if fromfile:
    inp.close()

try:
    stdout.close()
except:
    pass

try:
    stderr.close()
except:
    pass
