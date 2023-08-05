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

class Pong_Feedback(item):

	"""
	This class (the class with the same name as the module) handles the basic
	functionality of the item. It does not deal with GUI stuff.
	"""

	# Provide an informative description for your plug-in.
	description = u'Feedback for a single pong-like task trial.'

	def reset(self):

		"""
		desc: 
			Resets plug-in to initial values.
		"""

		# Here we provide default values for the variables that are specified
		# in info.json. If you do not provide default values, the plug-in will
		# work, but the variables will be undefined when they are not explicitly
		# set in the GUI.

		self.var.have_feedback = u'yes'
		self.var._fromFeedback = 0
		self.var._toFeedback = 0
		self.var._backcolor =  '#000000'
		
		self.var._Feedbackcolor = '#ff0000'
		self.var._FeedbackDelay = 600
		self.var._FeedbackcolorDuration = 200
		self.var._FromFeedbackDuration = 200
		self.var._ToFeedbackDuration = 800
		
	def prepare(self):
		return

	def late_prepare(self):

		"""The preparation phase of the plug-in goes here."""
		# Call the parent constructor.
		item.prepare(self)
		
		# make sure we are using uniform coordinates.
		# uniform coordinates have (0,0) in the middle of the screen.
		if  self.var.uniform_coordinates == u'no':
			raise osexception(u'When using the PONG plugin you should use uniform coordinates in the experiment settings.')
		
		# prepare the feedback screens
		# feedbackColor_canvas = color screen
		# feedback1_canvas = numbers, emphasis on old score
		# feedback2_canvas = numbers, emphasis on new score
		
		if (self.var.have_feedback == 'yes'):
			self.var.Feedback1_canvas = Canvas(self.experiment, background_color = self.var._backcolor)
			self.var.Feedback2_canvas = Canvas(self.experiment, background_color = self.var._backcolor)
			self.var.Feedback3_canvas = Canvas(self.experiment, background_color = self.var._Feedbackcolor)
			
			totsize = self.var.width-200
			for i in range (0,11):
				
				if (self.var._fromFeedback + 5 == i):
					self.var.Feedback1_canvas.rect( (-self.var.width/2)+100+(i*(totsize/11)),
														(-self.var.height/2)+200,
														totsize/11,
														100, 
														fill=True, color='#000055')
					
				self.var.Feedback1_canvas.rect( (-self.var.width/2)+100+(i*(totsize/11)),
													(-self.var.height/2)+200,
													totsize/11,
													100, 
													fill=False, color=self.var._Feedbackcolor)
					
				if (self.var._toFeedback + 5 == i):
					self.var.Feedback2_canvas.rect(  (-self.var.width/2)+100+(i*(totsize/11)),
														(-self.var.height/2)+200,
														totsize/11,
														100, 
														fill=True, color='#111155')
														
				self.var.Feedback2_canvas.rect( (-self.var.width/2)+100+(i*(totsize/11)),
													(-self.var.height/2)+200,
													totsize/11,
													100, 
													fill=False, color=self.var._Feedbackcolor)

				self.var.Feedback1_canvas.text(i-5, x=(-self.var.width/2)+100+((i+.5)*(totsize/11)), y=(-self.var.height/2)+250, font_size=32)
				self.var.Feedback2_canvas.text(i-5, x=(-self.var.width/2)+100+((i+.5)*(totsize/11)), y=(-self.var.height/2)+250, font_size=32)
				
			
			

	def perc2uni(self, perc, sizeval):
		return sizeval  * ((perc  - 50.0) / 100.0)


	def run(self):

		"""The run phase of the plug-in goes here."""

		# self.set_item_onset() sets the time_[item name] variable. Optionally,
		# you can pass a timestamp, such as returned by canvas.show().
		#
		# UPDATE THE POSITIONS OF THE PADDLE AND THE BALL
		# if the ball is on the floor (position of the paddle)
		# end the animation and calculate the response.		
		#
		# preparation tbd after pong task ready:
		
		self.late_prepare()
		
		#self.set_item_onset(self.var.my_canvas.show())
		

		if (self.var.have_feedback == 'yes'):
			self.set_item_onset(self.var.Feedback3_canvas.show())
			self.clock.sleep(self.var._FeedbackDelay)
			self.var.FeedbackColor_canvas = Canvas(self.experiment, background_color = self.var._Feedbackcolor)
			self.var.FeedbackColor_canvas.show()
			self.clock.sleep(self.var._FeedbackcolorDuration)
			
			self.var.Feedback1_canvas.show();
			self.clock.sleep(self.var._FromFeedbackDuration)
			self.var.Feedback2_canvas.show();
			self.clock.sleep(self.var._ToFeedbackDuration)


		

class qtPong_Feedback(Pong_Feedback, qtautoplugin):

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
		Pong_Feedback.__init__(self, name, experiment, script)
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
