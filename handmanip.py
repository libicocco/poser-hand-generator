# creatGraspICRA10.py -
#
# Copyright (c) 2009 Javier Romero, Greg Shakhnarovich
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
import random
import os
import linecache
import humanparam
import scenemanip

# Auxiliary stuff

unirnd = random.uniform

__finger_names = ['Index', 'Mid', 'Ring', 'Pinky']

#__cam_names = map(lambda x: x+' Camera',  ['Front', 'Main', 'Aux', 'Top', 'Left', 'Bottom'])
__cam_names = map(lambda x: x+' Camera',  ['Dolly', 'Main', 'Aux'])

scene = poser.Scene()


def all_set_lim(which, actor, valm, ValM):
    actor.Parameter(which).SetMinValue(valm)
    actor.Parameter(which).SetMaxValue(ValM)
    for c in actor.Children():
        all_set_lim(which, c, valm, ValM)


def all_set_scale(which,  actor,  val):
    # recursively set the corresp. scale (x, y, z) to actor and its descendants
    actor.SetParameter(which+'Scale',  val)
    for c in actor.Children():
        all_set_scale(which, c, val)


def phalangs(name):
    return [
        scene.Figure("Figure 1").Actor(name + '1'),
        scene.Figure("Figure 1").Actor(name + '2'),
        scene.Figure("Figure 1").Actor(name + '3')]


def draw_and_save(fname, fmt, logf, rend=1):
    scene.SetRenderAntiAliased(1)
    scene.SetRenderToNewWindow(0)
    logged = 0
    for cam in __cam_names:
        let = cam[0]
        scene.SetCurrentCamera(scene.Actor(cam))
        if rend:
            scene.Render()
        else:
            scene.DrawAll()
        scene.AntialiasNow()
        scene.SaveImage(fmt, fname+'_'+let)
        vals = {}
        vals['file'] = fname+'_'+let+'.'+fmt
        if not logged:
            hp = poserio.HandParam(0, vals)
            hp.write(logf)
            logged = 1
    logged = 0


# functions for hand perturbation
# JAVIER: bend individual fingers
def bend_finger_lim(limlow, limhigh, name, bnd=None):
    # val is in persentage of bending - positive
    ph = phalangs(name)
    # default - a random value
    if bnd is None:
        bnd = unirnd(0, 1)
    # define limits of bending
    # (t1t, t1b, t2b, t3b)
    limrange = map(lambda x, y: x-y,  limhigh, limlow)

    #compute actual bend values
    vals = map(lambda x, y: x*y,  [(bnd)]*len(limlow),  limrange)
    vals = map(lambda x, y: x+y,  vals,  limlow)
    # compute the needed deformation
    map(lambda x, y: x.Parameter('Bend').SetValue(y),  ph, vals[2:])
    #r = map(lambda x, y: x.Name()+'.Parameter(Bend).SetValue('+str(y)+')',  ph, vals[1:])
    ph[0].Parameter('Twist').SetValue(vals[0])
    ph[0].Parameter('Side-Side').SetValue(vals[1])


def interpolatePoses(jointFileName0, jointFileName1, jointFileNameOut, nFrames):
    line0 = linecache.getline(jointFileName0, 1)
    line1 = linecache.getline(jointFileName1, 1)
    vals0 = map(lambda x: float(x),  line0.strip().split())
    vals1 = map(lambda x: float(x),  line1.strip().split())
    range = map(lambda x, y: x-y,  vals1,  vals0)
    frame = 0.0
    jointFileOut = open(jointFileNameOut, 'w')
    while frame < nFrames:
        vals = map(lambda x, y: x*y,  [(frame/(nFrames-1))]*len(vals0),  range)
        vals = map(lambda x, y: x+y,  vals,  vals0)
        for val in vals:
            jointFileOut.write('%.3f ' % val)
        jointFileOut.write('\n')
        frame = frame + 1
    jointFileOut.close()


def renderInterpolatedPoses(basedir, jointFileName0, jointFileName1, outdir, nFrames):
    from os.path import join
    jointFileNameINT = join(outdir, 'tmp.txt')
    interpolatePoses(jointFileName0, jointFileName1, jointFileNameINT, nFrames)
    linecache.checkcache(jointFileNameINT)
    for frame in range(nFrames):
        frame = frame + 1
        humanparam.loadHandPose(basedir, jointFileNameINT, frame)
        frname = join(outdir, 'hnd%05d' % frame)
        scenemanip.stereoshot(frname, sil=False, stereo=False)
    os.remove(jointFileNameINT)


def pinchgrasp(side, val):
    # bend all the fingers together
    bend_finger_lim([-35, 0, 25, 0, 0], [15, 20, 25, -25, -30],
                    side+' Thumb ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 50, 20, 10], side+' Index ', val)


def bargrasp(side, val):
    # bend all the fingers together
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 60, 45, 45], side+' Index ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 60, 45, 30], side+' Mid ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 60, 45, 30], side+' Ring ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 75, 45, 30], side+' Pinky ', val)


def powergrasp(side, val):
    # bend all the fingers together
    bend_finger_lim([-35, 0, 25, 0, 0], [30, 0, -30, -30, -30],
                    side+' Thumb ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [7, 0, 75, 30, 15], side+' Index ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 75, 20, -10], side+' Mid ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [0, 0, 75, 0, 40], side+' Ring ', val)
    bend_finger_lim([0, 0, 0, 0, 0], [-15, 0, 75, 45, 30], side+' Pinky ', val)


def bend_thumb(bnd=None):
    # val is in persentage of bending - positive
    ph = phalangs('Right Thumb ')
    # default - a random value
    if bnd is None:
        bnd = unirnd(0, 1)
    # define limits of bending
    # (t1t, t1b, t2b, t3b)
    limlow = [-35, 25, 0, 0]
    limhigh = [30, -30, -30, -30]
    limrange = map(lambda x, y: x-y,  limhigh, limlow)

    #compute actual bend values
    vals = map(lambda x, y: x*y,  [(bnd)]*len(limlow),  limrange)
    vals = map(lambda x, y: x+y,  vals,  limlow)
    # compute the needed deformation
    map(lambda x, y: x.Parameter('Bend').SetValue(y),  ph, vals[1:])
    #r = map(lambda x, y: x.Name()+'.Parameter(Bend).SetValue('+str(y)+')',  ph, vals[1:])
    ph[0].Parameter('Twist').SetValue(vals[0])


def bend_finger(finger,  bnd=None):
    # finger is given by name: 'rIndex | rMid | rRing | rPinky'
    # val is in persentage of bending - positive or negative...

    ph = phalangs(finger)
    # default - a random value
    if bnd is None:
        bnd = unirnd(-1, 1)
    # find the limits of bend
    if bnd > 0:
        lim = map(lambda x: x.Parameter('Bend').MaxValue(),  ph)
    else:
        lim = map(lambda x: x.Parameter('Bend').MinValue(),  ph)

    #compute actual bend values
    vals = map(lambda x, y: x*y,  [abs(bnd)]*len(lim),  lim)
    # compute the needed deformation
    map(lambda x, y: x.Parameter('Bend').SetValue(y),  ph, vals)


def grasp(side, val):
    # bend all the fingers together
    bend_finger(side+'Index ', val)
    bend_finger(side+'Mid ', val)
    bend_finger(side+'Ring ', val)
    bend_finger(side+'Pinky ', val)


def forearm():
    fa = scene.Actor('Right Forearm')
    for parmname in ['Bend', 'Twist', 'Side-Side']:
        parm = fa.Parameter(parmname)
        parm.SetValue(unirnd(parm.MinValue(), parm.MaxValue()))


def spread(side, val=None):
    #val is percentage 0..1
    if val is None:
        val = unirnd(-1, 1)
    ss = map(lambda x: scene.Actor(side + ' '+x+' 1').Parameter('Side-Side'),
             __finger_names)
    # index and mid: positive side-side
    ss[0].SetValue(ss[0].MaxValue()*val)
    ss[1].SetValue(ss[1].MaxValue()*val)
    # ring,  pinky - negative...
    ss[2].SetValue(ss[2].MinValue()*val)
    ss[3].SetValue(ss[3].MinValue()*val)
