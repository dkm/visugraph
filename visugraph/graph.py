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

from PIL import Image
import os.path

class UnImplementedException(Exception):
    pass

class Node:

    def __init__(self, sid, x=0, y=0):
        self.neighs = []
        self.sid = sid
        self.x = x
        self.y = y

    def toSvg(self):
        raise UnImplementedException()


class ImageNode(Node):
    def __init__(self, sid, imageUrl, width, height, x=0, y=0):
        Node.__init__(self,sid, x, y)
        self.imageurl = imageUrl
        self.width = width
        self.height = height

    def toSvg(self):
        im = Image.open(self.imageurl)
        im = im.resize((self.width, self.height))
        new_url = "/home/dkm/git/visu-graph/imgcache/" + os.path.basename(self.imageurl)
        im.save(new_url)

        s = """
         <image
            y="%d"
            x="%d"
            id="%s"
            height="%d"
            width="%d"
            xlink:href="file://%s" />
            """ % (self.x, self.y, self.sid, 
                   self.height, self.width,  new_url)
        return s
