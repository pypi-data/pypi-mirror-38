import sys
import termios
import os
import string
import xterm.helpers as h

width, height = os.get_terminal_size()
stream = sys.stdin
mode = termios.tcgetattr(stream)
mode[3] = mode[3] &~ (termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
termios.tcsetattr(sys.stdin,1,mode)
print(h.escape('?1003h'),end='') # click detection
print(h.escape('?1006h'),end='') # make it better
print(h.escape('?25l'),end='') # hide cursor
print(h.escape('?7h'),end='') # don't  line wrap
print(h.escape('2J'),end=h.escape('H'),flush=True) # clear screen

class mouseClick():
	def __init__(self,name,_id,x,y,clicking):
		self.type = name
		self.id = _id
		self.x = x
		self.y = y
		self.down = clicking
	def __str__(self):
		return f'{self.type} {"down" if self.down else "up"}'
	def __repr__(self):
		return f'<{self.type} {"1" if self.down else "0"} ({self.x}, {self.y})>'


def parseMouseCode():
	mouseid = ''
	while True:
		text = stream.read(1)
		if text == ';':break
		mouseid += text
	x = ''
	while True:
		text = stream.read(1)
		if text == ';':break
		x += text
	y = ''
	while True:
		text = stream.read(1)
		if text in 'Mm':break
		y += text
	x, y, mouseid = int(x)-1, int(y)-1, int(mouseid)
	mousenames = {0:'click',33:'mouse up',32:'mouse dragged',2:'mouse 2',34:'mouse 2 dragged',64:'scroll up',65:'scroll down',1:'middle mouse down',33:'middle mouse scroll',4:'forward button down',36:'forward button still down',35:'back button down'}
	if mouseid in mousenames:
		return mousenames[mouseid],mouseid,x,y,text=='M'
	else:
		return 'unknown',mouseid,x,y,text=='M'

def parseMagicKeys(esccode):
	oof = esccode[-1]
	esccode = esccode[:-1]
	data = esccode.split(';')
	if oof == '~':
		if len(data) == 1:
			if data[0] == '3':
				return 'DELETE'
			elif data[0] == '6':
				return 'PAGEDOWN'
			elif data[0] == '5':
				return 'PAGEUP'
			elif data[0] == '15':
				return 'F5'
			elif data[0] == '17':
				return 'F6'
			elif data[0] == '18':
				return 'F7'
			elif data[0] == '19':
				return 'F8'
			elif data[0] == '20':
				return 'F9'
			elif data[0] == '21':
				return 'F10'
			elif data[0] == '24':
				return 'F12'
	elif oof == 'A':
		if len(data) == 2:
			if data[1] == '2':
				return 'SHIFT+UP'
			elif data[1] == '9':
				return 'CMD+UP'
	elif oof == 'B':
		if len(data) == 2:
			if data[1] == '2':
				return 'SHIFT+DOWN'
			elif data[1] == '9':
				return 'CMD+DOWN'
	elif oof == 'C':
		if len(data) == 2:
			if data[1] == '2':
				return 'SHIFT+RIGHT'
			elif data[1] == '9':
				return 'CMD+RIGHT'
	elif oof == 'D':
		if len(data) == 2:
			if data[1] == '2':
				return 'SHIFT+LEFT'
			elif data[1] == '9':
				return 'CMD+LEFT'
	return str(esccode)+' '+str(data)+' '+str(oof)

def parseEscapeCode():
	esccode=''
	while True:
		text = stream.read(1)
		esccode += text
		if text in string.ascii_letters+'<~':
			if esccode == '[D':#left arrow
				return 'LEFT'
			elif esccode == '[C':#right arrow
				return 'RIGHT'
			elif esccode == '[A':#up arrow
				return 'UP'
			elif esccode == '[B':#down arrow
				return 'DOWN'
			elif esccode == '[O':#unfocus
				return 'UNFOCUS'
			elif esccode == '[I':#focus
				return 'FOCUS'
			elif esccode == '[H':#home
				return 'HOME'
			elif esccode == '[F':#end
				return 'END'
			elif esccode == 'O':#f 1-4
				f = stream.read(1)
				return f'F{ord(f)-79}'
			elif esccode == '[<':#better mouse
				mousedata = parseMouseCode()
				mousedata = mouseClick(*mousedata)
				return mousedata
			elif esccode[-1] in '~ABCDF':#idek what these do
				return parseMagicKeys(esccode[1:])
			else:
				raise NameError(f'Unknown escape code: {esccode}')
			esccode = ''
			break
def readchr():
	c = stream.read(1)
	if ord(c)==27:#escape
		key = parseEscapeCode()
		return key
	elif ord(c)==127:
		return 'BACKSPACE'
	elif ord(c)==10:
		return 'ENTER'
	else:
		return c
