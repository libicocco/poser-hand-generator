# scenemanip.py - This file contains functions used in manipulating the Poser scene
#
# Copyright (c) 2009 Javier Romero,  Greg Shakhnarovich
#
# Author: Javier Romero <jrgn@kth.se>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License,  or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not,  write to the Free Software
# Foundation,  Inc.,  59 Temple Place,  Suite 330,  Boston,  MA 02111-1307
# USA

import poser
False = 0
True = 1
from random import uniform
from os.path import join

scene = poser.Scene()
fig_folder = 'c:/Documents and Settings/jrgn/Desktop/poserPython/Program Files/Curious Labs/Poser 5/Runtime/libraries/charachter/Clothing- Conforming/'
hair_folder = "c:/Documents and Settings/jrgn/Desktop/poserPython/Program Files/Curious Labs/Poser 5/Runtime/libraries/hair/Poser 4 Hair"


def setlight(lname):
    # set the parameters of the given light to a random values within fixed
    # bounds
    light = scene.Actor(lname)
    light.SetParameter("xRotate", uniform(-40, 40))
    light.SetParameter("yRotate", uniform(-50, 50))
    light.SetParameter("zRotate", uniform(-60, 60))
    light.SetParameter("Intensity", uniform(.70, 1))


def stereoshot(frname, disp=-.05, sil=False, stereo=True):
    # saving the image from the current camera. May also save silhouette
    # and/or a second stereo image
    if stereo:
        # produce a second shot moving the camera to the right
        cam = scene.CurrentCamera()
        currX = cam.Parameter('DollyX').Value()
        cam.SetParameter('DollyX', currX+disp)
        scene.DrawAll()
        scene.AntialiasNow()
        # JAVIER: if not added,  it doesn't update
        scene.Render()
        scene.SaveImage("png", frname+'-l.png')
        cam.SetParameter('DollyX', currX)

    scene.DrawAll()
    scene.AntialiasNow()
    #scene.SetRenderToNewWindow(0)
    # JAVIER: if not added,  it doesn't update
    scene.Render()
    #JAVIER SMALL CHANGE
    if stereo:
        scene.SaveImage("png", frname+'-r.png')
    else:
        scene.SaveImage("png", frname+'.png')

    if sil:
        # also save the silhouette
        scene.SetDisplayStyle(poser.kDisplayCodeSILHOUETTE)
        scene.DrawAll()
        # JAVIER: if not added,  it doesn't update
        scene.Render()
        silname = frname+'-fg.png'
        scene.SaveImage("png", silname)
        scene.SetDisplayStyle(poser.kDisplayCodeTEXTURESHADED)


shirts = ["P5MaleDressShirt2",
          "P5MaleTShirt",
          "P5MaleDBSuitCoat",
          "P5MaleSBSuitCoat",
          "P5MalePoloShirt",
          "P5MalePajamaTop",
          "P5MaleNehruShirt",
          "P5MaleLeatherCoat",
          "P5MaleWinterCoat",
          "P5MaleLightJacket"
          ]


def setShirt(gender='Male'):
    # change shirt (must be Figure 3)
    scene.SelectFigure(scene.Figure("Figure 3"))
    scene.DeleteCurrentFigure()
    k = int(uniform(0, len(shirts)))
    fig_path = join(fig_folder, 'Clothing- P5 '+gender, shirts[k]+".crz")
    scene.LoadLibraryFigure(fig_path)
    shirt = scene.Figure("Figure 3")
    shirt.SetConformTarget(scene.Figure("Figure 1"))

pants = ["P5MaleBathingSuit", "P5MaleJeans", "P5MaleChinos",
         "P5MaleCombatPants", "P5MaleCrocodilePants",
         "P5MaleDressSuitPants", "P5MalePajamaBottoms",
         "P5MaleSlacks", "P5ManShorts"]


def setPants(gender='Male'):
    # change pants (must be Figure 2)
    scene.SelectFigure(scene.Figure("Figure 2"))
    scene.DeleteCurrentFigure()
    k = int(uniform(0, len(pants)))
    scene.LoadLibraryFigure(join(fig_folder, "Clothing- P5 "+gender+"/"+pants[k]+".crz"))
    pant = scene.Figure("Figure 2")
    pant.SetConformTarget(scene.Figure("Figure 1"))

shoes = ["P5MaleCowBoyBoot", "P5MaleDressShoe2", "P5MaleHikingBoot",
         "P5MaleRunShoe", "P5MaleSandal", "P5MaleSock"]


def setShoes(gender='Male'):
    # change shoes. must be Figures 4 (L) and 5 (R)
    scene.SelectFigure(scene.Figure("Figure 4"))
    scene.DeleteCurrentFigure()
    k = int(uniform(0, len(shoes)))
    scene.LoadLibraryFigure(join(fig_folder, "Clothing- P5 "+gender+"/"+shoes[k]+"L.crz"))
    shoe = scene.Figure("Figure 4")
    shoe.SetConformTarget(scene.Figure("Figure 1"))

    scene.SelectFigure(scene.Figure("Figure 5"))
    scene.DeleteCurrentFigure()
    scene.LoadLibraryFigure(join(fig_folder, "Clothing- P5 "+gender+"/"+shoes[k]+"R.crz"))
    shoe = scene.Figure("Figure 5")
    shoe.SetConformTarget(scene.Figure("Figure 1"))


def setHair():
    # hair
    scene.SelectFigure(scene.Figure("Figure 1"))
    scene.SelectActor(scene.Figure("Figure 1").Actor("hair"))
    scene.DeleteCurrentProp()
    k = int(uniform(0, 4))
    scene.LoadLibraryHair(join(hair_folder, "Hair"+str(k+1)+".hr2"))
