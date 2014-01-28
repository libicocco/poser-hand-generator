# setTexture.py
#
# Copyright (c) 2009 Javier Romero
#
# Author: Javier Romero <jrgn@kth.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA
import poser


def setTexture(texture):
    scene = poser.Scene()
    fig = scene.Figure("Figure 1")
    materials = fig.Materials()
    for material in materials:
        #material.SetTextureMapFileName(texture)
        #print material.TextureMapFileName()
        name = material.Name()
        #print material.Name()
        if name == "skin":
            material.SetTextureMapFileName(texture)
        #    print "skin!!!"
        #else:
        #    print "no skin!!!"
    #skin = fig.FindMaterialByName("skin")
    #skin.SetTextureMapFileName("texture")
