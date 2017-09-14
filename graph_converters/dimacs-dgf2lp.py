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

for line in inp.readlines():
    line=line.split()
    if line==[]:
        continue
    if line[0]=='e':
        stdout.write('edge({},{}).\n'.format(line[1],line[2]))

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
