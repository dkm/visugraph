#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   airspace checker
#   Copyright (C) 2010  Marc Poulhiès
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import visugraph.graph

import StringIO
import sys

## 1 : Rank file
## 2 : listImage filr
## 3 : root node id

rankfin = open(sys.argv[1])
imgsfin = open(sys.argv[2])
pending_nodes = [int(sys.argv[3])]

# width and depth for visiting graph
depth = 3
width = 3

imgs = [x.strip() for x in imgsfin.xreadlines()]
imgsfin.close()

ranks = [x.strip() for x in rankfin.xreadlines()]
rankfin.close()

nodes = {}
neighs_nodes = {}


## set to True will use hardcoded image
debug = False

## initial pos for images
posx = 0
posy = 0

for node in pending_nodes:
    rank_line = ranks[node].split()
    node_id = int(rank_line[0])
    node_neighs = [int(x) for x in rank_line[1:width+1]]

    if depth > 0:
        pending_nodes += node_neighs
        neighs_nodes[node_id] = node_neighs
        depth -= 1
        posx += 400
    else:
        neighs_nodes[node_id] = []
        
    if debug:
        n = visugraph.graph.ImageNode(sid="node%d" % node_id, imageUrl="/home/dkm/accel.png",
                                      x=posx, y=posy)
    else:
        n = visugraph.graph.ImageNode(sid="node%d" % node_id, imageUrl=imgs[node_id],
                                      x=posx, y=posy)
    nodes[node_id] = n

for node_id, node in nodes.items():
    for neigh_node in neighs_nodes[node_id]:
        node.neighs.append(nodes[neigh_node])

sio = StringIO.StringIO()

CONNID = 1

def getConnector(node1, node2):
    global CONNID
    s="""
       <path
       style="fill:none;stroke:#000000;stroke-width:6;stroke-linecap:butt;stroke-linejoin:miter;stroke-miterlimit:4;stroke-opacity:1;stroke-dasharray:none"
       d="M -241.42854,519.50508 359.99992,-267.63779"
       id="path%d"
       inkscape:connector-type="polyline"
       inkscape:connection-start="#%s"
       inkscape:connection-end="#%s" />
       """ %(CONNID, node1.sid, node2.sid)
    CONNID += 1
    return s

sio.write("""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:xlink="http://www.w3.org/1999/xlink"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   width="744.09448819"
   height="1052.3622047"
   id="svg2"
   version="1.1"
   inkscape:version="0.47 r22583"
   sodipodi:docname="New document 1">
  <defs
     id="defs4">
    <inkscape:perspective
       sodipodi:type="inkscape:persp3d"
       inkscape:vp_x="0 : 526.18109 : 1"
       inkscape:vp_y="0 : 1000 : 0"
       inkscape:vp_z="744.09448 : 526.18109 : 1"
       inkscape:persp3d-origin="372.04724 : 350.78739 : 1"
       id="perspective10" />
    <inkscape:perspective
       id="perspective2884"
       inkscape:persp3d-origin="0.5 : 0.33333333 : 1"
       inkscape:vp_z="1 : 0.5 : 1"
       inkscape:vp_y="0 : 1000 : 0"
       inkscape:vp_x="0 : 0.5 : 1"
       sodipodi:type="inkscape:persp3d" />
    <inkscape:perspective
       id="perspective3123"
       inkscape:persp3d-origin="0.5 : 0.33333333 : 1"
       inkscape:vp_z="1 : 0.5 : 1"
       inkscape:vp_y="0 : 1000 : 0"
       inkscape:vp_x="0 : 0.5 : 1"
       sodipodi:type="inkscape:persp3d" />
  </defs>
  <sodipodi:namedview
     id="base"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageopacity="0.0"
     inkscape:pageshadow="2"
     inkscape:zoom="0.35"
     inkscape:cx="-133.57143"
     inkscape:cy="508.57143"
     inkscape:document-units="px"
     inkscape:current-layer="layer1"
     showgrid="false"
     inkscape:window-width="1280"
     inkscape:window-height="949"
     inkscape:window-x="0"
     inkscape:window-y="25"
     inkscape:window-maximized="1" />
  <metadata
     id="metadata7">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
""")

sio.write("""
 <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
""")

for node in nodes.values():
    for neigh in node.neighs:
        sio.write(getConnector(node, neigh))
    sio.write(node.toSvg())

sio.write(""" </g>
</svg>
""")

print str(sio.getvalue())
