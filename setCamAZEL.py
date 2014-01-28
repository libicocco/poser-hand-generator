# setCamAZEL.py
#
# Copyright (c) 2009 Javier Romero
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
import math
import poser
import os
import scenemanip
import handmanip
import humanparam
from os.path import join

#for convenience:
XT = poser.kParmCodeXTRAN
YT = poser.kParmCodeYTRAN
ZT = poser.kParmCodeZTRAN
XR = poser.kParmCodeXROT
YR = poser.kParmCodeYROT
ZR = poser.kParmCodeZROT
FOCAL = poser.kParmCodeFOCAL
scene = poser.Scene()


def setRenderOptions(scale=2, castShadows=0, ignoreShaderTrees=1, onBlack=1,
                     rayTracing=0, textureMaps=0):
    scene.SetRenderToNewWindow(0)
    scene.SetResolutionScale(scale)
    scene.SetRenderDimAutoscale(0)
    scene.SetOutputRes(640, 480)
    scene.SetRenderIgnoreShaderTrees(ignoreShaderTrees)
    #scene.SetRenderOnBlack(onBlack)
    scene.SetRenderOnBGColor(onBlack)
    scene.SetBackgroundColor(1.0, 1.0, 1.0)
    scene.SetRenderTextureMaps(textureMaps)
    scene.SetGroundShadows(0)
    scene.SetRenderCastShadows(castShadows)
#    ibl = scene.Actor("IBL")
#    ibl.SetShadow(1)
#    ibl.SetRayTraceShadows(1)
#    fireFlyOpt = scene.CurrentFireFlyOptions()
#    fireFlyOpt.SetManual(1)
#    fireFlyOpt.SetRayTracing(rayTracing)
#    fireFlyOpt.SetShadows(rayTracing)


def setCamAZEL(az, el, ro=0, f=70, camName="RHand Camera"):
    cam = scene.Actor(camName)
    target = scene.Actor("Right Hand")
    handCenter = target.Origin()
    cam.ParameterByCode(XT).SetValue(handCenter[0])
    cam.ParameterByCode(YT).SetValue(handCenter[1])
    cam.ParameterByCode(ZT).SetValue(handCenter[2]+5)
    cam.ParameterByCode(FOCAL).SetValue(f)
    cam.PointAt(target)
    cam.ParameterByCode(XR).SetValue(-el)
    cam.ParameterByCode(YR).SetValue(az-90)
    cam.ParameterByCode(ZR).SetValue(ro)
    scene.DrawAll()


def multiViewRender(nAz, nEl, dir, fullSphere=False, f=70,
                    camName="RHand Camera"):
    azs = map(lambda x: float(x)/float(nAz-1),  range(nAz))
    els = map(lambda x: float(x)/float(nEl-1),  range(nEl))

    if fullSphere:
        azmin = 0.0
        azrange = 360.0
        elmin = -90.0
        elrange = 180.0
    else:
        azmin = -90.0
        azrange = 180.0
        elmin = -90.0
        elrange = 180.0
    azs = map(lambda x: (x*azrange)+azmin,  azs)
    els = map(lambda x: (x*elrange)+elmin,  els)
    frame = 0
    for az in azs:
        for el in els:
            setCamAZEL(az, el, f, camName)
            frname = join(dir, 'hnd_%03d_%3.1daz_%3.1del' % (frame, az, el))
            scenemanip.stereoshot(frname, sil=False, stereo=False)
            frame = frame + 1


def seqRender(basedir, az, el, dir, poseFileList, nFrames, listpath, f=70,
              camName="RHand Camera"):
    cam = scene.Actor(camName)
    scene.SetCurrentCamera(cam)
    # If range starts in 1,  first frame is not rendered
    for stage in range(len(poseFileList)-1):
        poseFileINT = join(dir, 'temporal.txt')
        handmanip.interpolatePoses(poseFileList[stage], poseFileList[stage+1],
                                   poseFileINT, nFrames)
        for frame in range(1, nFrames+1):
            frame = frame + 1
            humanparam.loadHandPose(basedir, poseFileINT, frame)
            setCamAZEL(az, el, f, camName)
            frname = join(dir, '%03d_%03d' % (stage, frame-1))
            scenemanip.stereoshot(frname, sil=False, stereo=False)
            saveInfo(az, el, frame, stage, frname, listpath)
        os.remove(poseFileINT)


#included Rolling of the camera (introduced in UNIKARL)
#UPDATE:uniform sphere: 90 el: 1 az; and number increasing...
#NOW WORKS FOR HALF SPHERE AND STARTING AT EL 90
def multiViewSeqRender(basedir, nAz, nEl, nRo, dir, poseFile0, poseFile1,
                       nFrames, graspCode, listpath, fullSphere=False, f=70,
                       camName="RHand Camera"):
    cam = scene.Actor(camName)
    scene.SetCurrentCamera(cam)
    if fullSphere:
        azmin = 0.0
        # Defined later depending on nActualAz
        #azrange = 360.0*(1.0-(1.0/nAz))
        elmin = -90.0
        elrange = 180.0
    else:
        azmin = -90.0
        azrange = 180.0
        elmin = 0.0
        elrange = 90.0
    #romin   = -90
    #rorange = 180
    romin = 0
    rorange = 360.0*(1.0-(1.0/nRo))
    poseFileINT = join(dir, 'temporal.txt')
    handmanip.interpolatePoses(poseFile0, poseFile1, poseFileINT, nFrames)
    # If range starts in 1,  first frame is not rendered
    view = 0
    for frame in range(1, nFrames):
        frame = frame + 1
        humanparam.loadHandPose(basedir, poseFileINT, frame)
        for ind_el in range(0, nEl):
            if(ind_el < (nEl-1.0)/2.0):
                el = (1 - math.sin((float(ind_el)/((nEl-1.0)/2.0))*(math.pi/2)))*90
            else:
                el = (1 - math.sin((float(ind_el)/((nEl-1.0)/2.0))*(math.pi/2)))*-90
            #nActualAz = 2*(nEl-ind_el-1)+1 # this works if el starts in 0,  and is just half a sphere
            if(math.cos(math.radians(el)) < (1.0/nAz)):
                nActualAz = 1
            else:
                nActualAz = int(round(math.cos(math.radians(el))*nAz))
            for ind_az in range(0, nActualAz):
                azrange = 360.0*(1.0-(1.0/nActualAz))
                if nActualAz == 1:
                    azstep = 0
                else:
                    azstep = azrange/(nActualAz-1)
                az = azmin + ind_az*azstep
                for ind_ro in range(0, nRo):
                    print "%d, %d, %d, %d, %d" % (graspCode, frame,
                                                  ind_el, ind_az, ind_ro)
                    if nRo == 1:
                        rostep = 0
                    else:
                        rostep = rorange/(nRo-1)
                    ro = romin + ind_ro*rostep
                    setCamAZEL(az, el, ro, f, camName)
                    # Starting in frame 2 directly
                    #frname=dir+'/%03d_%04d' % (graspCode, (frame-2)*nAz*nEl*nRo+view)
                    frname = join(dir, '%03d_%04d' % (graspCode, view))
                    scenemanip.stereoshot(frname, sil=False, stereo=False)
                    scene.SaveImage("png", frname+'.png')

                    saveInfo(az, el, ro, frame, graspCode, frname, listpath)
                    view = view + 1
    os.remove(poseFileINT)


# next commented function is the valid one without ro!
def saveInfo(az, el, ro, frame, graspCode, frname, listpath):
    savingList = humanparam.readParamList(listpath)
    file = open(frname+".info", "w")
    file.write("# camera orientation (az, el)\n")
    file.write('%03.1f %03.1f %03.1f\n' % (az, el, ro))
    file.write("# hand joints (forearm{bend, side, twist} {index, mid, ring, pinky, thumb}{1[bend, side, twist] 2bend 3bend})\n")
    humanparam.writeparam(file, savingList)
    file.write("# grasp phase (frame within sequence)\n")
    file.write('%02d\n' % frame)
    file.write("# grasp code\n")
    file.write('%02d\n' % graspCode)
    file.write("# hand parts location ( forearm,  hand,  {thumb, index, mid, ring, pinky}{1, 2, 3})\n")
    humanparam.logXYZ(file, jointlist=humanparam.handjoints, units='Poser')
    file.close()
