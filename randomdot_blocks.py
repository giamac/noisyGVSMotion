#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import core, visual, gui, data, event, clock
from psychopy.tools.filetools import fromFile, toFile
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
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
dataFile.write('Trial,Direction,Coherence,Response,ResponseCode,ResponseCorrect,ReactionTime,Condition,VP,Threshold\n')

# Define Variables & Stimuli

globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window([2048,1152],fullscr = True, allowGUI=False, monitor='testMonitor', units='pix', color = [-1,-1,-1])

dots = visual.DotStim(win=win, name='dots',
    nDots=100, dotSize=3,
    speed=5, dir=1.0, coherence=1.0,
    fieldPos=[0.0, 0.0], fieldSize=400,fieldShape='circle',
    signalDots='same', noiseDots='direction',dotLife=3,
    color=[1.0,1.0,1.0], colorSpace='rgb', opacity=1, depth=0.0)

fixation = visual.TextStim(win, pos=[0,0],text='+', color = [1,1,1], opacity = 0.3)

threshold = expInfo['threshold']

#Create 3 blocks with different intensities. 

levels = [threshold, 2 * threshold, 0.5 * threshold] * 1
random.shuffle(levels)

# Create thirty trials per block, at the moment 5

directions = [0, 180] * 50


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

pause = u'''Kurze Pause. Druecke die Leertaste um weiterzufahren'''

instruction = visual.TextStim(win, text = instr1, height = 30, wrapWidth = 900)

pausetxt = visual.TextStim(win, text = pause, height = 30)
endExpNow = False

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
    
    #Make a pause after a block
    if trial == 101 or trial == 201:
        pausetxt.draw()
        fixation.setAutoDraw(False)
        win.flip()
        event.waitKeys(keyList = ['space'])
    
    #set location of stimuli
    Direction = thisTrial['ori'] #will be either 0(right) or 180(left)
    DirectionCue = Direction/180 #will be either -1(right) or 1(left)
    DirectionCoded = DirectionCue*2-1
    dots.setDir(Direction)


    #set orientation of probe
    dots.setFieldCoherence(thisTrial['coherence'])
    
# ------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    dots.refreshDots()
    key_resp_2 = event.BuilderKeyResponse()
    # keep track of which components have finished
    trialComponents = [dots, key_resp_2]
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "trial"-------
    while continueRoutine:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *dots* updates
        if t >= 0.0 and dots.status == NOT_STARTED:
            # keep track of start time/frame for later
            dots.tStart = t
            dots.frameNStart = frameN  # exact frame index
            dots.setAutoDraw(True)
        if dots.status == STARTED and frameN >= (dots.frameNStart + 30):
            dots.setAutoDraw(False)
        
        # *key_resp_2* updates
        if t >= 0.0 and key_resp_2.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_2.tStart = t
            key_resp_2.frameNStart = frameN  # exact frame index
            key_resp_2.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_2.status == STARTED and frameN >= (key_resp_2.frameNStart + 180):
            key_resp_2.status = STOPPED
        if key_resp_2.status == STARTED:
            theseKeys = event.getKeys(keyList=['f','j','escape'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                key_resp_2.rt = key_resp_2.clock.getTime()
                # a response ends the routine
                continueRoutine = False
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys=None
    
    if key_resp_2.keys != None:
        thisKey = key_resp_2.keys[-1]
    else:
        thisKey = 'NA'
        key_resp_2.rt = 999
    
    if (thisKey=='f' and Direction==180) or (thisKey=='j' and Direction==0):
        thisResp = 1  # correct
    else:
        thisResp = 0  # incorrect
    
    if thisKey == 'f':
        resp = 1
    elif thisKey == 'j':
        resp = 0
    else:
        resp = 2
    fixation.draw()
    win.flip()
        
    coher = DirectionCoded * thisTrial['coherence']
    dataFile.write('%i,%i,%.2f,%s,%i,%i,%.2f,%.2f,%s,%.2f\n' %(trial,Direction,coher,thisKey,resp,thisResp,key_resp_2.rt,expInfo['condition'],expInfo['subjectID'], expInfo['threshold']))

    core.wait(1)

