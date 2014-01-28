# humanparam.py - This file contains basic variables and methods for manipulations on
# articulated human models.
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
import linecache
scene = poser.Scene()
from random import uniform,  gauss


# NOTE: due to an apparent bug in PoserPython,  Twist has to be renamed
# TwistY (this file assumes this has been done in the figure). The script sn.py
# will do it.

# the pose parameters,  as articulation angles
humanparams = [
               # height of the hip above the floor
               [["Hip",  "yTran"], [0, 1]],
               # global orientation
               [["Hip",  "yRotate"], [0, 360]],
               [["Hip",  "xRotate"], [-90, 90]],
               [["Hip",  "zRotate"], [-90, 90]],
               # torso
               [["Abdomen", "TwistY"], [-40, 40]],  # note the name
               [["Abdomen", "Bend"], [-15, 50]],
               [["Abdomen", "Side-Side"], [-20, 20]],
               [["Chest", "TwistY"], [-50, 50]],  # note the name
               [["Chest", "Bend"], [-35, 45]],
               [["Chest", "Side-Side"], [-30, 30]],
               # upper limbs
               [["Right Collar", "TwistY"], [-20, 40]],
               [["Right Collar", "Front-Back"], [-7, 7]],
               [["Right Collar", "Up-Down"], [-30, 5]],
               [["Right Shoulder", "TwistY"], [-90, 85]],
               [["Right Shoulder", "Bend"], [-30, 80]],
               [["Right Shoulder", "Front-Back"], [-30, 100]],
               [["Right Forearm", "TwistY"], [-20, 40]],
               [["Right Forearm", "Bend"], [-10, 90]],
               [["Right Hand", "TwistY"], [-15, 15]],
               [["Right Hand", "Bend"], [-10, 20]],
               [["Right Hand", "Side-Side"], [-5, 5]],
               [["Left Collar", "TwistY"], [-40, 20]],
               [["Left Collar", "Front-Back"], [-7, 7]],
               [["Left Collar", "Up-Down"], [-5, 30]],
               [["Left Shoulder", "TwistY"], [-85, 90]],
               [["Left Shoulder", "Bend"], [-80, 30]],
               [["Left Shoulder", "Front-Back"], [-100, 30]],
               [["Left Forearm", "TwistY"], [-20, 40]],
               [["Left Forearm", "Bend"], [-90, 10]],
               [["Left Hand", "TwistY"], [-15, 15]],
               [["Left Hand", "Bend"], [-20, 10]],
               [["Left Hand", "Side-Side"], [-5, 5]],
               # lower limbs
               [["lButtock", "TwistY"], [-25, 25]],
               [["lButtock", "Bend"], [-60, 60]],
               [["lButtock", "Side-Side"], [-2, 35]],
               [["Left Thigh", "TwistY"], [-90,  90]],
               [["Left Thigh", "Bend"], [-100,  60]],
               [["Left Thigh", "Side-Side"], [-20,  70]],
               [["Left Shin", "TwistY"], [-10, 10]],
               [["Left Shin", "Bend"], [-10, 130]],
               [["Left Shin", "Side-Side"], [-10, 10]],
               [["Left Foot", "Bend"], [-50, 30]],
               [["Left Foot", "TwistY"], [-15, 15]],
               [["Left Foot", "Side-Side"], [-15, 20]],
               [["rButtock", "TwistY"], [-25, 25]],
               [["rButtock", "Bend"], [-60, 60]],
               [["rButtock", "Side-Side"], [-35, 2]],
               [["Right Thigh", "TwistY"], [-90,  90]],
               [["Right Thigh", "Bend"], [-100,  60]],
               [["Right Thigh", "Side-Side"], [-70,  20]],
               [["Right Shin", "TwistY"], [-10, 10]],
               [["Right Shin", "Bend"], [-10, 130]],
               [["Right Shin", "Side-Side"], [-10, 10]],
               [["Right Foot", "TwistY"], [-15, 15]],
               [["Right Foot", "Bend"], [-30, 50]],
               [["Right Foot", "Side-Side"], [-20, 15]],
               # head
               [["Head", "Bend"], [-4, 4]],
               [["Head", "TwistY"], [-8, 8]],
               [["Head", "Side-Side"], [-4, 4]],
               [["Neck", "Bend"], [-4, 4]],
               [["Neck", "TwistY"], [-8, 8]],
               [["Neck", "Side-Side"], [-4, 4]]]

# need to move the hip.yRotate to 1st or last place,  to make it easier to
# find it


# the list of parameters (actor/parameter pairs) may be obtained like this:
# parampairs=map(lambda x: x[0],  humanparams)

# these additional parameters will somewhat affect the appearance,
# but are not part of the model (i.e.,  nuisance variables)

nuisance_params = [[["lThumb1", "Bend"], [-20, 10]],
                   [["rThumb1", "Bend"], [-10, 20]],
                   [["lThumb1", "TwistY"], [-10, 10]],
                   [["rThumb1", "TwistY"], [-10, 10]],
                   [["lThumb2", "Bend"], [-20, 10]],
                   [["rThumb2", "Bend"], [-10, 20]],
                   # expression
                   [["Head", "Laughter"], [-.2, .4]],
                   [["Head", "Surprise"], [-.1, .1]],
                   [["leftEye", "Side-Side"], [-30, 30]],
                   [["rightEye", "Side-Side"], [-30, 30]]
                   ]


# Joints. Although it's easier to manipulate the angles in Poser (and there
# appears,  joints are useful in
# measuring pose similarity and in fitting 3D models.
# for each joint,  we have:
# 0) its name,
# 1) the number of ends (0 meand only Origin,  1 means also the Endpoint, -1 means only the endpoint)
# 2) the parity (0 means a single part,  1 meand L/R)

humanjoints = [["SkullMale4", -1, 0],         # 1:3 (top of the head)
               ["Head", 0, 0],         # 4:6 (base of the head)
               ["Neck", 0, 0],         # 7:9
               ["Hip", 0, 0],          # 10:12
               ["lBigToe2", 1, 0],     # 13:15,  16:18
               ["rBigToe2", 1, 0],     # 19:21,  22:24
               ["Shoulder", 0, 1],     # L: 25:27,   R: 28:30
               ["Forearm", 0, 1],      # L: 31:33,   R: 34:36
               ["Hand", 0, 1],         # L: 37:39,   R: 40:42
               ["Thigh", 0, 1],        # L: 43:45,   R: 46:48
               ["Shin", 0, 1],         # L: 49:51,   R: 52:54
               ["Foot", 0, 1]         # L: 55:57,   R: 58:60
               ]
# JAVIER: Hand Joints
handjoints = [["Right Forearm", 0, 0],
              ["Right Hand", 0, 0],
              ["Right Thumb 1", 0, 0],
              ["Right Thumb 2", 0, 0],
              ["Right Thumb 3", -1, 0],
              ["Right Index 1", 0, 0],
              ["Right Index 2", 0, 0],
              ["Right Index 3", -1, 0],
              ["Right Mid 1", 0, 0],
              ["Right Mid 2", 0, 0],
              ["Right Mid 3", -1, 0],
              ["Right Ring 1", 0, 0],
              ["Right Ring 2", 0, 0],
              ["Right Ring 3", -1, 0],
              ["Right Pinky 1", 0, 0],
              ["Right Pinky 2", 0, 0],
              ["Right Pinky 3", -1, 0]
              ]


# setpar : set a given parameter for the given figure
# p[0] is [actorname, paramname]
# p[1] is the limits [min, max]
# distr is 'unif' or 'gaus'; for Gaussian,  must also provide params
def setpar(fig, p, val=None, distr='unif', distrparam=[]):
    pact = p[0][0]
    pname = p[0][1]
    if val is None:   # need to draw value at random
        if distr.lower() == 'gaus':
            newval = gauss(distrparam[0], distrparam[1])
        if distr.lower() == 'unif':
            newval = uniform(p[1][0], p[1][1])
    else:
        newval = val
    # make sure within the limits
    if newval < p[1][0]:
        newval = p[1][0]
    if newval > p[1][1]:
        newval = p[1][1]
    fig.Actor(pact).SetParameter(pname, newval)


# modify the limits for [act, par] in the list params
# returns old limits
def setlimits(params, act, par, newlimits):
    for i in range(0, len(params)):
        if act == params[i][0][0] and par == params[i][0][1]:
            oldlimits = params[i][1]
            params[i][1] = newlimits
            return oldlimits
    return [0, 0]


def writeparam(file, list, num=None, figname="Figure 1"):
    # collect and write into file the parameter (angle) values for list.
    # list contains [actor, parameter name] pairs
    if num is not None:
        file.write('%d ' % num)
    fig = scene.Figure(figname)
    for p in list:
        strVal = '%.3f ' % (fig.Actor(p[0]).Parameter(p[1]).Value())
        file.write(strVal)
    file.write('\n')


#JAVIER
def readNParam(fileName, list, n):
    linecache.checkcache(fileName)
    line = linecache.getline(fileName, n)
    #print line
    vals = map(lambda x: float(x),  line.strip().split())
    param = []
    for p in range(0, len(vals)):
        param.append([list[p], vals[p]])
    return param


def readParamSkipCAM(fileName, list):
    linecache.checkcache(fileName)
    line = linecache.getline(fileName, 2)
    vals = map(lambda x: float(x),  line.strip().split())
    vals = vals[3:]
    #print vals
    param = []
    for p in range(0, len(vals)):
        param.append([list[p], vals[p]])
    return param


def readParam(file, list):
    vals = map(lambda x: float(x),  file.readline().strip().split())
    param = []
    for p in range(0, len(vals)):
        param.append([list[p], vals[p]])
    return param


def convertUnits(value, units):
    if units == 'Poser':
        return value
    elif units == 'meter':
        return value*96*.0254
    else:
        return value*96


def jointXYZ(nm, ep=0, figname="Figure 1", units='Poser'):
    # returns a string combining the joint location,  for one given body part
    # if ep is 1,  also reports the endpoint location
    if units == 'Poser':
        precision = '%.6f'
    else:
        precision = '%.4f'

    parstr = ""
    act = scene.Figure(figname).Actor(nm)
    (x, y, z) = act.WorldDisplacement()

    if ep >= 0:
        (ox, oy, oz) = act.Origin()
        parstr += precision % (convertUnits(x+ox, units))
        parstr += ' '+precision % (convertUnits(y+oy, units))
        parstr += ' '+precision % (convertUnits(z+oz, units))
    if ep != 0:
        (ex, ey, ez) = act.EndPoint()
        parstr += ' '+precision % (convertUnits(x+ex, units))
        parstr += ' '+precision % (convertUnits(y+ey, units))
        parstr += ' '+precision % (convertUnits(z+ez, units))
    return parstr


def logXYZ(logf, jointlist=None, num=None, units='Poser'):
    # save joint locations into a file
    # if num is given,  it is written before the coordinates in the file
    # units: can be 'Poser', 'meter', 'inch'
    jstr = ""
    # default joint list
    if jointlist is None:
        jointlist = humanjoints
    for j in range(0, len(jointlist)):
        nm = jointlist[j][0]
        if jointlist[j][2] == 0:
            # a non-paired joint
            jstr = jstr+' '+jointXYZ(nm, jointlist[j][1], units=units)
        else:
            jstr = jstr+' '+jointXYZ("Left "+nm, jointlist[j][1], units=units)
            jstr = jstr+' '+jointXYZ("Right "+nm, jointlist[j][1], units=units)
    if num is not None:
        logf.write('%d ' % num)
    logf.write(jstr+'\n')


# the joint reading functions don't seem to work right now
def getJoint(jointspec, vallist, ind):
    # retrieve from the list of values (with the current index given by ind)
    # the information for a joint described by jointspec
    origin = (vallist[ind], vallist[ind+1], vallist[ind+2])
    ind += 3
    if (jointspec[1] == 1):   #pack the endpoint if necessary
        endpoint = (vallist[ind], vallist[ind+1], vallist[ind+2])
        ind += 3
        pts = [origin, endpoint]
    else:
        pts = [origin]
    return pts, ind


def setJoint(jointname, origin, endpoint=None, figname="Figure 1"):
    # jointvalue is [name, origin] or [name, origin, endpoint]
    # set the locaiton of the joint
    act = scene.Figure(figname).Actor(jointname)
    act.SetWorldDisplacement(origin[0], origin[1], origin[2])
    act.SetOrigin(origin[0], origin[1], origin[2])
    if endpoint is not None:
        act.SetEndPoint(endpoint[0], endpoint[1], endpoint[2])


def readXYZ(xyzf, jointlist=None):
    # read from the file xyzf the list of parameters
    # returns a list,  where each entry consists of:
    # - the joint name,
    # - the XYZ for the Origin as a triple,
    # - if relevant,  the XYZ of the Endpoint

    # get the floats from the next line in the file
    vals = map(lambda x: float(x),  xyzf.readline().strip().split())
    jvalues = []
    i = 0
    if jointlist is None:
        jointlist = humanjoints
    for j in range(0, len(jointlist)):
        nm = jointlist[j][0]
        if jointlist[j][2] == 0:  # a non-paired joint
            (pts, i) = getJoint(jointlist[j], vals, i)
            joint = [None]*(len(pts) + 1)
            joint[0] = nm
            joint[1:] = pts
            jvalues.append(joint)
        else: # a paired,  L/R,  joint
            (pts, i) = getJoint(jointlist[j], vals, i)
            joint = [None]*(len(pts)+1)
            joint[0] = "Left "+nm
            joint[1:] = pts
            jvalues.append(joint)
            (pts, i) = getJoint(jointlist[j], vals, i)
            joint = [None]*(len(pts)+1)
            joint[0] = "Right "+nm
            joint[1:] = pts
            jvalues.append(joint)
    return jvalues


def captureParam(params, figname="Figure 1"):
    fig = scene.Figure(figname)
    resparam = []
    for n in range(0, len(params)):
        # p is [actor,  name]
        p = params[n]
        resparam.append([[p[0], p[1]],
                        fig.Actor(p[0]).Parameter(p[1]).Value()])
    return resparam


def restoreParams(params, figname="Figure 1"):
    # params[i] is [[actor, parameter],  value],  as created by captureParam or by
    # readParam
    fig = scene.Figure(figname)
    for n in range(0, len(params)):
        p = params[n]
        pact = p[0][0]
        pname = p[0][1]
        fig.Actor(pact).Parameter(pname).SetValue(p[1])


def readParamList(fname):
    f = open(fname, "r")
    lines = f.readlines()
    plist = map(lambda x: x.strip().split('.'),   lines)
    f.close()
    return plist


def writeParamList(fname, plist):
    f = open(fname, "w")
    for p in range(0, len(plist)):
        print plist[p][0]
        print plist[p][1]
        f.write(plist[p][0]+"."+plist[p][1]+"\n")
    f.close()


#JAVIER: save pose; basically save paramList and params
def saveHandPose(basedir, jointFileName):
    jointFile = open(jointFileName, 'w')
    paramlist = readParamList(basedir + '/poses/handjointslist.txt')
    writeparam(jointFile, paramlist)
    jointFile.close()


#JAVIER: load pose; basically load n pose in the params
def loadHandPoseFromOutput(basedir, jointFileName):
    paramlist = readParamList(basedir + '/poses/handjointssavinglist.txt')
    pose = readParamSkipCAM(jointFileName, paramlist)
    restoreParams(pose)


def loadHandPose(basedir, jointFileName, n=1):
    paramlist = readParamList(basedir+'/poses/handjointslist.txt')
    pose = readNParam(jointFileName, paramlist, n)
    restoreParams(pose)


def mirrorPart(dict, entry, srcpart, param, tgtpart, flip):
    # if the part/param match the pattern,  add a dictionary entry
    if entry[0][0] == srcpart and entry[0][1] == param:
        dict[tgtpart, param] = flip*entry[1]


def mirrorPose(params):
    # "flip" left/right in the pose. Params is a list of entries
    # [[actor, param],  value] such as build by captureParam or by
    # readParam
    # returns the mirror pose.

    mirror = {}
    for p in params:
        mirrorPart(mirror, p, "Hip", "yRotate", "Hip", -1)
        mirrorPart(mirror, p, "Hip", "xRotate", "Hip", -1)
        mirrorPart(mirror, p, "Hip", "zRotate", "Hip", -1)
        mirrorPart(mirror, p, "Abdomen", "TwistY", "Abdomen", -1)
        mirrorPart(mirror, p, "Abdomen", "Side-Side", "Abdomen", -1)
        mirrorPart(mirror, p, "Chest", "TwistY", "Chest", -1)
        mirrorPart(mirror, p, "Chest", "Side-Side", "Chest", -1)
        mirrorPart(mirror, p, "Left Collar", "TwistY", "Right Collar", 1)
        mirrorPart(mirror, p, "Left Collar", "Front-Back", "Right Collar", -1)
        mirrorPart(mirror, p, "Left Collar", "Up-Down", "Right Collar", -1)
        mirrorPart(mirror, p, "Right Collar", "TwistY", "Left Collar", 1)
        mirrorPart(mirror, p, "Right Collar", "Front-Back", "Left Collar", -1)
        mirrorPart(mirror, p, "Right Collar", "Up-Down", "Left Collar", -1)
        mirrorPart(mirror, p, "Right Shoulder", "TwistY", "Left Shoulder", 1)
        mirrorPart(mirror, p, "Right Shoulder", "Front-Back", "Left Shoulder", -1)
        mirrorPart(mirror, p, "Right Shoulder", "Bend", "Left Shoulder", -1)
        mirrorPart(mirror, p, "Left Shoulder", "TwistY", "Right Shoulder", 1)
        mirrorPart(mirror, p, "Left Shoulder", "Front-Back", "Right Shoulder", -1)
        mirrorPart(mirror, p, "Left Shoulder", "Bend", "Right Shoulder", -1)
        mirrorPart(mirror, p, "Left Forearm", "TwistY", "Right Forearm", 1)
        mirrorPart(mirror, p, "Left Forearm", "Bend", "Right Forearm", -1)
        mirrorPart(mirror, p, "Right Forearm", "TwistY", "Left Forearm", 1)
        mirrorPart(mirror, p, "Right Forearm", "Bend", "Left Forearm", -1)
        mirrorPart(mirror, p, "Left Hand", "TwistY", "Right Hand", 1)
        mirrorPart(mirror, p, "Left Hand", "Bend", "Right Hand", -1)
        mirrorPart(mirror, p, "Left Hand", "Side-Side", "Right Hand", -1)
        mirrorPart(mirror, p, "Right Hand", "TwistY", "Left Hand", 1)
        mirrorPart(mirror, p, "Right Hand", "Side-Side", "Left Hand", -1)
        mirrorPart(mirror, p, "Right Hand", "Bend", "Left Hand", -1)
        mirrorPart(mirror, p, "lButtock", "TwistY", "rButtock", -1)
        mirrorPart(mirror, p, "lButtock", "Side-Side", "rButtock", -1)
        mirrorPart(mirror, p, "lButtock", "Bend", "rButtock", 1)
        mirrorPart(mirror, p, "rButtock", "TwistY", "lButtock", -1)
        mirrorPart(mirror, p, "rButtock", "Side-Side", "lButtock", -1)
        mirrorPart(mirror, p, "rButtock", "Bend", "lButtock", 1)
        mirrorPart(mirror, p, "Right Thigh", "TwistY", "Left Thigh", -1)
        mirrorPart(mirror, p, "Left Thigh", "TwistY", "Right Thigh", -1)
        mirrorPart(mirror, p, "Right Thigh", "Side-Side", "Left Thigh", -1)
        mirrorPart(mirror, p, "Left Thigh", "Side-Side", "Right Thigh", -1)
        mirrorPart(mirror, p, "Right Thigh", "Bend", "Left Thigh", 1)
        mirrorPart(mirror, p, "Left Thigh", "Bend", "Right Thigh", 1)
        mirrorPart(mirror, p, "Right Shin", "TwistY", "Left Shin", -1)
        mirrorPart(mirror, p, "Left Shin", "TwistY", "Right Shin", -1)
        mirrorPart(mirror, p, "Right Shin", "Side-Side", "Left Shin", -1)
        mirrorPart(mirror, p, "Left Shin", "Side-Side", "Right Shin", -1)
        mirrorPart(mirror, p, "Right Shin", "Bend", "Left Shin", 1)
        mirrorPart(mirror, p, "Left Shin", "Bend", "Right Shin", 1)
        mirrorPart(mirror, p, "Left Foot", "TwistY", "Right Foot", -1)
        mirrorPart(mirror, p, "Right Foot", "TwistY", "Left Foot", -1)
        mirrorPart(mirror, p, "Left Foot", "Side-Side", "Right Foot", -1)
        mirrorPart(mirror, p, "Right Foot", "Side-Side", "Left Foot", -1)
        mirrorPart(mirror, p, "Left Foot", "Bend", "Right Foot", 1)
        mirrorPart(mirror, p, "Right Foot", "Bend", "Left Foot", 1)
        mirrorPart(mirror, p, "Neck", "TwistY", "Neck", -1)
        mirrorPart(mirror, p, "Neck", "Side-Side", "Neck", -1)
        mirrorPart(mirror, p, "Head", "TwistY", "Head", -1)
        mirrorPart(mirror, p, "Head", "Side-Side", "Head", -1)
        if (p[0][0], p[0][1]) not in mirror.keys():
            mirror[p[0][0], p[0][1]] = p[1]

    mirrorparams = []
    for p in params:
        mirrorparams.append([p[0], mirror[p[0][0], p[0][1]]])
    return mirrorparams
