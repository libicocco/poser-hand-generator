# creatGraspICRA09.py - script for creating a hand poses database
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
import linecache
import os
import setCamAZEL
import setTexture
from os.path import join

scene = poser.Scene()

basedir = os.path.dirname(os.path.abspath(__file__))
dir = join(basedir, 'out')
lightdir = join(basedir, 'lights')
taxonomyDir = join(basedir, 'taxonomy')
texture = join(basedir, 'Hand Texture2.TIF')
listpath = join(basedir, 'poses', 'handjointssavinglist.txt')
#lights=["light1.lt2","light2.lt2","light3.lt2","light4.lt2"]
lights = ["light1.lt2"]
nAz = 24
nEl = 12
nRo = 9
nFrames = 6

grasps = ["largeDiameter", "smallDiameter", "mediumWrap", "adductedThumb",
          "lightTool", "prismatic4Finger", "prismatic3Finger",
          "prismatic2Finger", "palmarPinch", "powerDisk", "powerSphere",
          "precisionDisk", "precisionSphere", "tripod", "fixedHook", "lateral",
          "indexFingerExtension", "extensionType", "distalType",
          "writingTripod", "tripodVariation", "parallelExtension",
          "adductionGrip", "tipPinch", "lateralTripod", "sphere4Finger",
          "quadpod", "sphere3Finger", "stick", "palmarGrasp",
          "ringGrasp", "ventralGrasp", "inferiorPincerGrasp"]

#poser.SetNumRenderThreads(4)
#poser.SetRenderInSeparateProcess(1)

for graspIndex in range(len(grasps)):
    outdir = join(dir, '%02d' % (graspIndex+1))
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
    for lightindex in range(len(lights)):
        jointFileName0 = join(taxonomyDir, "rest.txt")
        jointFileName1 = join(taxonomyDir, grasps[graspIndex] + ".txt")
        graspCode = (graspIndex)*(len(lights)) + lightindex + 1
        # close and discard changes
        poser.CloseDocument(1)
        poser.OpenDocument(join(taxonomyDir, grasps[graspIndex] + ".pz3"))
        scene.LoadLibraryLight(lightdir+lights[lightindex])
        setTexture.setTexture(texture)
        linecache.checkcache(jointFileName0)
        linecache.checkcache(jointFileName1)
        setCamAZEL.setRenderOptions(scale=0)
        gnd = scene.Actor("GROUND")
        gnd.SetVisible(0)
        gnd.SetVisibleInRender(0)
        gnd.SetVisibleInReflections(0)
        ffly = scene.CurrentFireFlyOptions()
        ffly.SetManual(1)
        setCamAZEL.multiViewSeqRender(basedir, nAz, nEl, nRo, outdir,
                                      jointFileName0, jointFileName1,
                                      nFrames, graspCode, listpath=listpath,
                                      fullSphere=True, f=70,
                                      camName="RHand Camera")
