#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""measure 1-down-1-up (0.5 threshold)"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import time, numpy


expName = 'randomdot_staircase_v1.py'
expInfo = {'subjectID':''}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

#make a text file to save data
fileName = expInfo['subjectID'] + '_' + dateStr
dataFile = open('data/'+fileName+'_staircase.csv', 'w')
dataFile.write('Trial,Direction,Coherence,Response,ResponseCode,ResponseCorrect,stairCase\n')



globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window([2048,1152],fullscr = True, allowGUI=False, monitor='testMonitor', units='pix', color = [-1,-1,-1])


dots = visual.DotStim(win=win, name='dots',
    nDots=100, dotSize=3,
    speed=5, dir=1.0, coherence=1.0,
    fieldPos=[0.0, 0.0], fieldSize=400,fieldShape='circle',
    signalDots='same', noiseDots='direction',dotLife=3,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1, depth=1.0)

fixation = visual.TextStim(win, pos=[0,0],text='+', color = [1,1,1], opacity = 0.3)

instr1 = u'''Vielen Dank für deine Teilnahme am Experiment. \n
Im Folgenden werden dir für kurze Zeit (0.5 Sekunden) Punktewolken, mit sich bewegenden Punkten, gezeigt.\n
Ein Teil der Punkte hat dabei eine zufällige Bewegungsrichtung, während der Rest sich entweder nach links oder rechts bewegt.\n
Drücke die Leertaste um mit der Instruktion weiterzufahren.'''

instr2 = u'''Wenn du denkst, die Punkte bewegen sich nach links, drücke \n
\t\t\t\t'f' \n
Wenn du denkst, die Punkte bewegen sich nach rechts, drücke\n
\t\t\t\t'j' \n
Bitte antworte erst, wenn der Stimulus verschwunden ist. \n
Drücke die Leertaste um mit der Instruktion weiterzufahren.'''

pause = u'''Dies war Block 1 von 2. Druecke die Leertaste um weiterzufahren'''

instruction = visual.TextStim(win, text = instr1, height = 30, wrapWidth = 900)
pausetxt = visual.TextStim(win, text = pause, height = 30)


# Stepsizes of the staircase (in percent coherence)
# these are chosen very arbitrarily, and there might be better ways to do this
# e.g. consider logarithmic stepsizes
steps = [0.05,0.05,0.04,0.04,0.03,0.03,0.02,0.02,0.01,0.01]

# What I did here was start one from high and one from low coherence, these are interleaved, see documentation for params
# You could also think about doing one for leftward and one for rightward motion
conditions=[
    {'label':'low', 'startVal': 0.05, 'stepType' : 'lin', 'minVal' : 0.01, 'maxVal' : 1, 'nUp' : 1, 'nDown' : 2, 'stepSizes' : steps},
    {'label':'high','startVal': 0.95, 'stepType' : 'lin', 'minVal' : 0.01, 'maxVal' : 1, 'nUp' : 1, 'nDown' : 2, 'stepSizes' : steps}]


stairs = data.MultiStairHandler(conditions=conditions, nTrials=100)

instruction.draw()
win.flip()
event.waitKeys(keyList = ['space'])

instruction.setText(instr2)
instruction.draw()
win.flip()
event.waitKeys(keyList = ['space'])

trial = 0
for thisIncrement in stairs: #will step through the staircase
    trial += 1

    if trial == 101:
        pausetxt.draw()
        fixation.setAutoDraw(False)
        win.flip()
        event.waitKeys(keyList = ['space'])



    #set Motion Direction (one is for encoding correct resp

    DirectionCue = round(numpy.random.random()) #will be either 0(right) or 180(left)
    DirectionCoded = DirectionCue*2-1 #will be either -1(right) or 1(left)
    Direction = DirectionCue*180 #will be either 0(right) or 180(left)
    dots.setDir(Direction)

    #set orientation of probe
    dots.setFieldCoherence(thisIncrement[0])

    #draw all stimuli
    fixation.setAutoDraw(True)
    dots.setAutoDraw(True)
    for f in xrange(30): win.flip()

    #blank screen
    dots.setAutoDraw(False)
    win.flip()

    #get response
    thisResp=None
    while thisResp is None:
        allKeys=event.waitKeys()
        for thisKey in allKeys:
            if (thisKey=='f' and Direction==180) or (thisKey=='j' and Direction==0):
                thisResp = 1  # correct
            elif (thisKey == 'j' and Direction == 180) or (thisKey == 'f' and Direction == 0):
                thisResp = 0  # incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()  # abort experiment
        event.clearEvents('mouse')  # only really needed for pygame windows

    #add the data to the staircase so it can calculate the next level
    stairs.addResponse(thisResp)
    if thisKey == 'f':
        resp = 1
    elif thisKey == 'j':
        resp = 0

    dataFile.write('%i,%i,%.2f,%s,%i,%i,%s\n' %(trial,Direction,thisIncrement[0],thisKey,resp,thisResp,thisIncrement[1]['label']))
    core.wait(0.5)
