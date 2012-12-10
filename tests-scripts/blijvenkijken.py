#!/usr/bin/env python
# -*- coding: utf-8 -*-
from scribus import *

def shrinkObject(Lambda, Thing):
        ThingSize = getSize(Thing)
        sizeObject(Lambda*ThingSize[0], Lambda*ThingSize[1], Thing)
        xMove = ((1-Lambda)*ThingSize[0]) / 2
        yMove = ((1-Lambda)*ThingSize[1]) / 2
        moveObject(xMove, yMove, Thing)

def growObject(Lambda, Thing):
        ThingSize = getSize(Thing)
        sizeObject(Lambda*ThingSize[0], Lambda*ThingSize[1], Thing)

class Character:
        def seesPrince(self):
                self.Scribus = 'Prince'
		self.Species = 'Prince'
		self.Colors = ['PrinceInitialFill', 'PrinceFinalFill']
                self.Factor = pow((1.0/PrinceScale), 1.0/(Pages-1))
		self.generation = 1
        def seesFrog(self):
                self.Scribus = 'Frog'
		self.Species = 'Frog'
		self.Colors = ['FrogInitialFill', 'FrogFinalFill']
                self.Factor = pow(FrogScale, 1.0/(Pages-1))
		self.generation = 1

        def blushes(self):
		#what colors did the designer design? dialog twixt designer&pybus
                self.InitialFill = getColor(self.Colors[0])
                self.FinalFill = getColor(self.Colors[1])
		tmp = self.Species + 'InitialFill'
                setFillColor(tmp, self.Scribus)

        def calculates(self):
        	#get position&size. these are supposed to be prince-specific.
	        #so this will only get called once.
                self.Size = getSize(self.Scribus)
                self.Position = getPosition(self.Scribus)
                self.fillStep = {}
                self.fillStep['c'] = (self.FinalFill[0] - self.InitialFill[0]) / Pages
                self.fillStep['y'] = (self.FinalFill[1] - self.InitialFill[1]) / Pages
                self.fillStep['m'] = (self.FinalFill[2] - self.InitialFill[2]) / Pages
                self.fillStep['k'] = (self.FinalFill[3] - self.InitialFill[3]) / Pages

        #this is where the color gets changed
        def changesColor(self):
                C = int(self.InitialFill[0] + (self.fillStep['c'] * (self.generation - 1)))
                Y = int(self.InitialFill[1] + (self.fillStep['y'] * (self.generation - 1)))
                M = int(self.InitialFill[2] + (self.fillStep['m'] * (self.generation - 1)))
                K = int(self.InitialFill[3] + (self.fillStep['k'] * (self.generation - 1)))
		tmp = self.Species + 'Fill' + str(self.generation)
                defineColor(tmp, C, Y, M, K)
                setFillColor(tmp, self.Scribus)

	def division(self):
		correctPosition = getPosition(self.Scribus)
		duplicateObject(self.Scribus)
		#we only need to create one page per iteration
		if self.Species == 'Frog':
			newPage(-1)
		moveObject(0, pageSize[1], self.nextScribus())
		gotoPage(self.generation + 1)
		moveObjectAbs(correctPosition[0], correctPosition[1],\
		self.nextScribus())
		linkTextFrames(self.Scribus, self.nextScribus())
		self.Scribus = self.nextScribus()
		self.generation += 1

	def grows(self):
		growObject(self.Factor, self.Scribus)
	        midSize = getSize(self.Scribus)
	        xMove = self.Position[0] + ((self.Size[0]-midSize[0]) / 2)
	        yMove = self.Position[1] + ((self.Size[1]-midSize[1]) / 2)
	        moveObjectAbs(xMove, yMove, self.Scribus)

	#this exists solely because of scribus' weird duplicateObject()
	def nextScribus(self):
		if self.Scribus == self.Species:
			return 'Copy of ' + self.Scribus
		else:
			x = str(self.generation)
			return 'Copy of ' + self.Species +\
			' (' + x + ')'

	def swaps(self):
		if self.Species == 'Frog':
	                sentToLayer('Bottom', Frog.Scribus) 
		else:
	                sentToLayer('Top', Prince.Scribus)

	def shrinks(self):
		shrinkObject(self.Factor, self.Scribus)	

	#i get the feeling that this is pushing the oop too far
	def takesPlace(self):
		shrinkObject(PrinceScale, 'Prince')
		sentToLayer('Top', 'Prince')
		sentToLayer('Bottom', 'Frog')

#dialogue with designer via dialogs
Pages = int(valueDialog('pages', 'number of pages in scribus document.'))
PrinceScale = float(valueDialog('how small will the prince get?', ' \
How much will the prince shrink? Halfsize = 0.5, quartersize = 0.25, etc.'))
FrogScale = float(valueDialog('how small will the frog get?', ' \
How much will the frog shrink? Halfsize = 0.5, quartersize = 0.25, etc.'))
FrogFile = str(valueDialog('content', "IGNORE"))
PrinceFile = str(valueDialog('content', "IGNORE"))
FileName = str(valueDialog('document', 'IGNORE'))
pageSize = getPageSize()

#for the swaping
createLayer('Bottom')
createLayer('Top')

#prince
Prince = Character()
Prince.seesPrince()
Prince.blushes()
Prince.calculates()

#frog
Frog = Character()
Frog.seesFrog()
Frog.blushes()
Frog.calculates()
Frog.takesPlace()

for i in range(1, Pages-1):
	Frog.division()
	Prince.division()
	Frog.shrinks()
	Prince.grows()
	Frog.changesColor()
	Prince.changesColor()
	#swap at the middle
        if i >= int(Pages/2):
		Frog.swaps()
		Prince.swaps()

#this is so that the Prince ends up where the designer originally put it. 'tis very ugly.
Frog.division()
Prince.division()
Frog.shrinks()
sizeObject(Prince.Size[0], Prince.Size[1], Prince.Scribus)
moveObjectAbs(Prince.Position[0], Prince.Position[1])
setFillColor('FrogFinalFill', Frog.Scribus)
setFillColor('PrinceFinalFill', Prince.Scribus)
Frog.swaps()
Prince.swaps()

#get txt
ft = open(FrogFile, 'r')
FrogStory = ft.read()
pt = open(PrinceFile, 'r')
PrinceStory = pt.read()
setText(FrogStory, 'Frog')
setText(PrinceStory, 'Prince')

saveDocAs(FileName)
