'''
you shouldnt use this because its kinda not good
'''

from .. import main as xterm
#from . import async as xterm
from threading import Thread

class data:
	x,y=0,0
class pixel:
	def __init__(self,letter,modifier,x,y):
		self.letter=letter
		self.modifier=modifier
		self.x=x
		self.y=y
class positionQueue:
	def __init__(self):
		self.queue = []
	def add(self,item):
		self.queue.append(item)
		data.x+=1

#queue=[]
#def addtoqueue
def frame():
	pass
def isevent(eventtype,char):
	if eventtype in ['mouse','click','drag']:
		if type(char) != str:
			if eventtype == 'click':
				return char.type == 'mouse' and char.down
			elif eventtype == 'drag':
				if char.type == 'mouse' and char.down:
					return True
				elif char.type == 'mouse dragged':
					return True
			else:
				return True
	elif eventtype in ['key','chr']:
		if type(char) == str:
			if eventtype == 'chr':
				return len(char) == 1
			else:
				return True
	else:
		return True

def start(fps=5):
	for char in xterm.readchrs():
		for listener in eventlisteners:
			func = listener[0]
			eventtype = listener[1]
			if isevent(eventtype,char):
				func(char)
eventlisteners = []
eventtypes = ('all','key','mouse','chr','click','drag')
def event(arg='all'):
	if arg not in eventtypes:
		raise ReferenceError(f'Unknown event type. Please choose one of the following: {eventtypes}')
	def createlistener(func):
		global eventlisteners
		eventlisteners.append((func,arg))
	return createlistener