#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import core, visual, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import time, numpy, random


# Setup Experiment
expName = 'randomdot_confidence_v1.py'
expInfo = {'subjectID':'101',
           'condition' : 1,
           'threshold': 0.152}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName



#make a text file to save data
fileName = 'S' + expInfo['subjectID'] + '_B' + str(expInfo['condition']) + '_' + dateStr
dataFile = open('data/'+fileName+'.csv', 'w')
dataFile.write('Trial,Direction,Coherence,Response,ResponseCode,ResponseCorrect,Condition,VP,Thresholdf\n')

# Define Variables & Stimuli

globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window([2048,1152],fullscr = True, allowGUI=False, monitor='testMonitor', units='pix', color = [-1,-1,-1])

dots = visual.DotStim(win=win, name='dots',
    nDots=100, dotSize=3,
    speed=0.001, dir=1.0, coherence=1.0,
    fieldPos=[0.0, 0.0], fieldSize=400,fieldShape='circle',
    signalDots='same', noiseDots='direction',dotLife=3,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1, depth=0.0)

fixation = visual.TextStim(win, pos=[0,0],text='+', color = [1,1,1], opacity = 0.3)

threshold = expInfo['threshold']

#Create 3 blocks with different intensities. 

levels = [threshold, 4.6 * threshold, 0.6 * threshold] * 1
random.shuffle(levels)

# Create thirty trials per block, at the moment 5

directions = [0, 180] * 1


instr1 = u'''Vielen Dank für deine Teilnahme am Experiment. \n
Im Folgenden werden dir für kurze Zeit (0.5 Sekunden) Punktewolken, mit sich bewegenden Punkten, gezeigt.\n
Ein Teil der Punkte hat dabei eine zufällige Bewegungsrichtung, während der Rest sich entweder nach links oder rechts bewegt.\n
Drücke die Leertaste um mit der Instruktion weiterzufahren.'''

instr2 = u'''Wenn du denkst, die Punkte bewegen sich nach links, drücke \n
\t\t\t\t'f' \n
Wenn du denkst, die Punkte bewegen sich nach rechts, drücke\n
\t\t\t\t'j' \n
Bitte antworte erst, wenn der Stimulus verschwunden ist. \nj
Drücke die Leertaste um mit der Instruktion weiterzufahren.'''


instruction = visual.TextStim(win, text = instr1, height = 30, wrapWidth = 900)


#create your list of stimuli
stimList = []
for coherence in levels:
    random.shuffle(directions)
    for ori in directions:
        stimList.append(
            {'coherence':coherence, 'ori':ori} #this is a python 'dictionary'
            )


trials = data.TrialHandler(trialList = stimList, nReps = 1, method='sequential')



event.Mouse(visible=False) 
instruction.draw()
win.flip()
event.waitKeys(keyList = ['space'])

instruction.setText(instr2)
instruction.draw()
win.flip()
event.waitKeys(keyList = ['space'])




trial = 0
for thisTrial in trials: #handler can act like a for loop
    trial += 1
    
    #set location of stimuli
    Direction = thisTrial['ori'] #will be either 0(right) or 180(left)
    DirectionCue = Direction/180 #will be either -1(right) or 1(left)
    DirectionCoded = DirectionCue*2-1
    dots.setDir(Direction)


    #set orientation of probe
    dots.setFieldCoherence(thisTrial['coherence'])
     
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
                thisResp = 1#correct
            elif (thisKey=='j' and Direction==180) or (thisKey=='f' and Direction==0):
                thisResp = 0#incorrect
            elif thisKey in ['q', 'escape']:
                core.quit()#abort experiment
        event.clearEvents('mouse')#only really needed for pygame windows
    event.Mouse(visible=True) 
    fixation.setAutoDraw(False)
        
    if thisKey == 'f':
        resp = 1
    elif thisKey == 'j':
        resp = 0
    fixation.draw()
    win.flip()
        
    coher = DirectionCoded * thisTrial['coherence']
    dataFile.write('%i,%i,%.2f,%s,%i,%i,%i,%s,%.2f\n' %(trial,Direction,coher,thisKey,resp,thisResp,expInfo['condition'],expInfo['subjectID'], expInfo['threshold']))

    core.wait(1)

