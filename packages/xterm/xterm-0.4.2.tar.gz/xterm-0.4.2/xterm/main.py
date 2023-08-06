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
getrgb = h.getrgb
escape = h.escape

print(escape('?1003h'),end='') # click detection
print(escape('?1006h'),end='') # make it better
print(escape('?25l'),end='') # hide cursor
print(escape('?7l'),end='') # don't  line wrap
def clear():
	print(escape('2J'),end=escape('H'),flush=True)
clear()
class mouseClick():
	def __init__(self,name,_id,x,y,clicking):
		self.type = name
		self.id = _id
		self.x = x
		self.y = y
		self.down = clicking
#	def __str__(self):
#		if self.type in ['mouse','mouse 2','middle mouse']:
#			return f'{self.type} {"down" if self.down else "up"}'
#		else:
#			return str(self.type)
	def __str__(self):
		if self.type in ['mouse','mouse 2','middle mouse']:
			return f'<{self.type} {"down" if self.down else "up"} ({self.x}, {self.y})>'
		else:
			return f'<{self.type} ({self.x}, {self.y})>'

def parse_mouse_sequence():
	mouseid = ''
	while True:
		text = read_stream()
		if text == ';':break
		mouseid += text
	x = ''
	while True:
		text = read_stream()
		if text == ';':break
		x += text
	y = ''
	while True:
		text = read_stream()
		if text in 'Mm':break
		y += text
	x, y, mouseid = int(x)-1, int(y)-1, int(mouseid)
	mousenames = {
		0:'mouse',
		1:'middle mouse',
		2:'mouse 2',
		4:'forward button down',
		32:'mouse dragged',
		34:'mouse 2 dragged',
		64:'scroll up',
		65:'scroll down',
		33:'middle mouse drag',
		36:'forward button still down',
		35:'back button down'
	}
	if mouseid in mousenames:
		return mousenames[mouseid],mouseid,x,y,text=='M'
	else:
		return 'unknown',mouseid,x,y,text=='M'

def combokeys(esccode):
	escapetype = esccode[-1]
	esccode = esccode[:-1]
	data = esccode.split(';')
	extrakeys = ''
	if len(data) == 2:
		arg = int(data[1])
		things={
			2:'SHIFT',
			3:'ALT',
			5:'CTRL',
			6:'CTRL+SHIFT',
			7:'CTRL+ALT',
			8:'CTRL+SHIFT+ALT',
			9:'CMD',
			13:'CMD+CTRL',
			16:'CTRL+SHIFT+ALT+CMD'
		}
		if arg in things:
			extrakeys = things[arg]+'+'
		else:
			extrakeys = f'{arg}+'

	if escapetype == '~':
		arg = int(data[0])
		codes = {
			2:'INSERT',
			3:'DELETE',
			5:'PAGEUP',
			6:'PAGEDOWN',
			15:'F5',
			17:'F6',
			18:'F7',
			19:'F8',
			20:'F9',
			21:'F10',
			23:'F11',
			24:'F12'
		}
		if arg in codes:
			return extrakeys+codes[arg]
	elif escapetype == 'A':
		return extrakeys+'UP'
	elif escapetype == 'B':
		return extrakeys+'DOWN'
	elif escapetype == 'C':
		return extrakeys+'RIGHT'
	elif escapetype == 'D':
		return extrakeys+'LEFT'
	elif escapetype == 'H':
		return extrakeys+'HOME'
	elif escapetype == 'F':
		return extrakeys+'END'

	return 'idk '+str(esccode)+' '+str(data)+' '+str(escapetype)+' '+extrakeys

def parse_csi_sequence():
	esccode=''
	while True:
		text = read_stream()
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
			elif esccode == '[F':#end
				return 'END'
			elif esccode == '[Z':#end
				return 'SHIFT+TAB'
			elif esccode == 'O':#f 1-4
				f = read_stream()
				return f'F{ord(f)-79}'
			elif esccode == '[<':#better mouse
				mousedata = parse_mouse_sequence()
				mousedata = mouseClick(*mousedata)
				return mousedata
			elif esccode[-1] in '~ABCDFH':#idek what these do
				return combokeys(esccode[1:])
			else:
				print(f'WARNING: Unknown escape code: {esccode}')
			esccode = ''
			break
def read_stream():
	return stream.read(1)
def readchr():
	c = read_stream()
	keycode = ord(c)
	if keycode < 32 or keycode >= 127:
		codes = {
			8:'SHIFT+BACKSPACE',
			9:'TAB',
			10:'ENTER',
			127:'BACKSPACE'
		}
		if keycode==27:#escape
			key = parse_csi_sequence()
			return key
		else:
			if keycode in codes:
				return codes[keycode]
			else:
				return keycode
	else:
		return c
def readchrs():
	while True:
		yield readchr()
