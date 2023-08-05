#-*- coding:utf-8 -*-

"""
No rights reserved. All files in this repository are released into the public
domain.
"""
from libopensesame.py3compat import *
from libopensesame.item import item
from openexp.keyboard import keyboard
from libopensesame.exceptions import osexception

from libqtopensesame.items.qtautoplugin import qtautoplugin
from openexp.canvas import Canvas
from openexp.canvas_elements import *
import math
import pygame

class pong(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'A single pong-like task trial.'

	def reset(self):

		"""
		desc: 
			Resets plug-in to initial values.
		"""
		self.var._ballsize = 15
		self.var._ballspeed = 5
		self.var._ballpos = 50
		self.var._yballpos = 0
		self.var._paddlepos = 80.0
		
		self.var._ballangle = 0
		self.var._ballcolor = '#ffffff'
		
		self.var._paddlesize = 15
		self.var._paddlecolor = '#ffffff'

		self.var._backcolor = '#000000' 
		
		self.var.have_startbox = True
		self.var._startboxcolor = '#ffffff'
		self.var._startboxloc = 50
		self.var._startboxsize = 20
		self.var._startboxtime = 1000

		self.var.have_endline = False
		self.var._endlinecolor = '#ffffff'
		self.var._endlineloc = 50

		self.var.have_vendline = False
		self.var._vendlinecolor = '#ffffff'
		self.var._vendlineloc = 50

		self.var._Delay = 500

		self.var.maxax = 1
		self.var.minax = -1
		
	def prepare(self):

		"""The preparation phase of the plug-in goes here."""
		# Call the parent constructor.
		item.prepare(self)
		
		# make sure we are using uniform coordinates.
		# uniform coordinates have (0,0) in the middle of the screen.
		if  self.var.uniform_coordinates == u'no':
			raise osexception(u'When using the PONG plugin you should use uniform coordinates in the experiment settings.')

		self._ballangle = self.var._ballangle
		self._ballspeed = self.var._ballspeed
		
		# these variables are unique to the used 'joystick' device. They should hold the values the device returns at leftmost and rightmost position.
		#self.var.maxax = .15
		#self.var.minax = -1
		
		#Create the Canvasses.
		self.var.my_canvas = Canvas(self.experiment, background_color = self.var._backcolor)

		self.var._bally = self.var._yballpos     # the ball starts at 3 % above the screen 
		self.var._paddley = 97	 # assume the paddle on the bottom of the screen

		self._keyboard = keyboard(self.experiment) # enable stopping the experiment using the esc. button.
			
		# convert the positional percentages into uniform coordinates	
		self.var.startboxloc  =  self.perc2uni(self.var._startboxloc, self.var.width)
		self.var.endlineloc   =  self.perc2uni(self.var._endlineloc, self.var.width)
		self.var.vendlineloc  =  self.perc2uni(self.var._vendlineloc, self.var.height)
		self.var._ballx 	  =  self.perc2uni(self.var._ballpos, self.var.width)
		self.var._bally 	  =  self.perc2uni(self.var._bally, self.var.height)
		self.var._paddlex     =  self.perc2uni(self.var._paddlepos, self.var.width)
		self.var._paddley     =  self.perc2uni(self.var._paddley, self.var.height)

		# remember the startpoint of the ball.
		self.var._ballysp =	self.var._bally;
		self.var._ballxsp =	self.var._ballx;

		# calculate paddle width in pixels
		self.var.startboxsize = self.var.width*(self.var._startboxsize/100.0)
		self.var.pw = self.var.width*(self.var._paddlesize/100.0)
		self.var.old_joyax = self.experiment.joystick.get_joyaxes(1)

		self.var.my_canvas['Ball']   = Circle(self.var._ballx, -10000 ,self.var._ballsize, fill=True, color=self.var._ballcolor)
		self.var.my_canvas['Paddle'] = Rect(self.var._paddlex,self.var._paddley,self.var.pw,20, fill=True, color=self.var._paddlecolor)
		
		# put the lines on the canvas if we want them.
		if (self.var.have_endline == u'yes'):		
			self.var.my_canvas['Endline'] = Line(self.var.endlineloc,-self.var.height/2,self.var.endlineloc,self.var.height/2,  color=self.var._endlinecolor)
		if (self.var.have_vendline == u'yes'):		
			self.var.my_canvas['VEndline'] = Line(-self.var.width/2,self.var.vendlineloc,self.var.width/2,self.var.vendlineloc,  color=self.var._vendlinecolor)
			
		if (self.var.have_startbox == u'yes'):
			self.var.my_canvas['StartBox'] = Rect(self.var.startboxloc, self.var._paddley, self.var.startboxsize, 26, fill = False, color= self.var._startboxcolor )
		
		self.var.startvar = (self.var.startboxsize - self.var.pw ) / 2
		
		self.var.Delay = u'no'
		if self.var._Delay > 0:
			self.var.Delay = u'yes'
			

	def perc2uni(self, perc, sizeval):
		return sizeval  * ((perc  - 50.0) / 100.0)

	def ax2pos(self, ax):
		return(self.var.width * ((ax - self.var.minax) /  (self.var.maxax - self.var.minax) - .5)) - (self.var.pw)
	
	
	def WaitForStartBoxBegin(self):
		WaitedLongEnough = False
		waitedfrom = self.clock.time()
		
		while not WaitedLongEnough:
			if self._keyboard is not None:
				self._keyboard.flush()
		
			new_joyax, timestamp = self.experiment.joystick.get_joyaxes(1000.0/60.0)
			if new_joyax is not None: 
				self.var._paddlepos = self.ax2pos(new_joyax[0])
				self.var.my_canvas['Paddle'].x = self.var._paddlepos
			
			if 	abs((self.var._paddlepos + (self.var.pw / 2)) - (self.var.startboxloc + (self.var.startboxsize / 2))) < self.var.startvar:
				#print abs(self.var._paddlepos - self.var.startboxloc) , self.var.startvar
				if (self.clock.time() - waitedfrom) > self.var._startboxtime:
					WaitedLongEnough = True
			else:
				waitedfrom = self.clock.time()
			
			self.var.my_canvas.show()
			
		del self.var.my_canvas['StartBox']
			
	def CheckForHorizontalLines(self):
	# Horizontal  Lines
		if (self.var.have_vendline == u'yes'):		
			if self.var._bally <= self.var.vendlineloc:
				if self.var.Delay == u'no':
					self.var.my_canvas['Ball'].y = self.var._bally
			else:
				self.var.my_canvas['Ball'].y = -self.var.height # not in the picture
			return True
		else:
			self.var.my_canvas['Ball'].y = self.var._bally
			return False

	def CheckForVerticalLines(self):
	# vertical Lines
		if (self.var.have_endline == u'yes'):		
			if self.var._paddlepos <= self.var.endlineloc:
				self.var.my_canvas['Paddle'].x = self.var.endlineloc
				self.var.my_canvas['Paddle'].w = max(1, self.var.pw - (self.var.endlineloc - self.var._paddlepos))
			else:
				self.var.my_canvas['Paddle'].x = self.var._paddlepos
				self.var.my_canvas['Paddle'].w = self.var.pw
			return True
		else:
			return False
		#self.var.my_canvas['Paddle'].x = self.var._paddlepos

	
	def run(self):

		"""The run phase of the plug-in goes here."""

		# self.set_item_onset() sets the time_[item name] variable. Optionally,
		# you can pass a timestamp, such as returned by canvas.show().
		#
		# UPDATE THE POSITIONS OF THE PADDLE AND THE BALL
		# if the ball is on the floor (position of the paddle)
		# end the animation and calculate the response.		
		#
		self.set_item_onset(self.var.my_canvas.show())
		
		#Delay = True
		t0 = self.clock.time()
		
		self.experiment.var.startmoment = None
		#------------------------------------------------------------------------------------------------------------------------
		#while self.var._bally+self.var._ballsize < self.var._paddley-self.var._paddlesize:
		self.var.my_canvas['Paddle'].x = (self.var.width/2)-self.var.pw
		self.var.my_canvas.show()
		pygame.event.set_allowed(pygame.JOYAXISMOTION)

		if self.var.have_startbox == u'yes':
			self.WaitForStartBoxBegin()
		
		if self.var.Delay == u'yes':
			self.var.Delay = u'no'
			self.clock.sleep(self.var._Delay)
		
		t0 = self.clock.time()
		
		while self.var._bally+self.var._ballsize < self.var._paddley:
			if self._keyboard is not None:
				self._keyboard.flush()
		
			t = self.clock.time() - t0;

			self.var._bally = self.var._ballysp + ((t/10.0)*(math.cos(math.radians(self.var._ballangle))) * self.var._ballspeed)
			self.var._ballx = self.var._ballxsp + ((t/10.0)*(math.sin(math.radians(self.var._ballangle))) * self.var._ballspeed)
			
			self.CheckForHorizontalLines()

			new_joyax, timestamp = self.experiment.joystick.get_joyaxes(1000.0/60.0)
			if new_joyax is not None: 
				# first axis movement: if another start is needed do that here.
				if self.experiment.var.startmoment is None:
					self.experiment.var.startmoment = self.clock.time() - t0;
						
				self.var._paddlepos = self.ax2pos(new_joyax[0])

			if not self.CheckForVerticalLines():
				self.var.my_canvas['Paddle'].x = self.var._paddlepos

			self.var.my_canvas.show()
					
		#------------------------------------------------------------------------------------------------------------------------
		
		pd = self.var._ballx - self.var._paddlepos
		self.experiment.var.PongHit =  pd > -(self.var._ballsize) and pd < (self.var.pw + self.var._ballsize)
		self.set_response(None, None, self.experiment.var.PongHit=='yes')
		self.experiment.var.paddlepos 	= self.var._paddlepos
		self.experiment.var.ballx 		= self.var._ballx
		
		pygame.event.set_blocked(pygame.JOYAXISMOTION)



		

class qtpong(pong, qtautoplugin):

	"""
	This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
	usually need to do hardly anything, because the GUI is defined in info.json.
	"""

	def __init__(self, name, experiment, script=None):

		"""
		Constructor.

		Arguments:
		name		--	The name of the plug-in.
		experiment	--	The experiment object.

		Keyword arguments:
		script		--	A definition script. (default=None)
		"""

		# We don't need to do anything here, except call the parent
		# constructors.
		pong.__init__(self, name, experiment, script)
		qtautoplugin.__init__(self, __file__)

	def init_edit_widget(self):

		"""
		Constructs the GUI controls. Usually, you can omit this function
		altogether, but if you want to implement more advanced functionality,
		such as controls that are grayed out under certain conditions, you need
		to implement this here.
		"""

		# First, call the parent constructor, which constructs the GUI controls
		# based on info.json.
		qtautoplugin.init_edit_widget(self)
		# If you specify a 'name' for a control in info.json, this control will
		# be available self.[name]. The type of the object depends on the
		# control. A checkbox will be a QCheckBox, a line_edit will be a
		# QLineEdit. Here we connect the stateChanged signal of the QCheckBox,
		# to the setEnabled() slot of the QLineEdit. This has the effect of
		# disabling the QLineEdit when the QCheckBox is uncheckhed. We also
		# explictly set the starting state.
