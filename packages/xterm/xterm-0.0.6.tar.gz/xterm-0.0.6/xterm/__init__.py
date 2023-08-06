import sys
import termios
import os
import string
import xterm.helpers
print(__name__)
if __name__ == '__main__':
    width, height = os.get_terminal_size()
    stream = sys.stdin
    mode = termios.tcgetattr(stream)
    mode[3] = mode[3] &~ (termios.ECHO | termios.ICANON | termios.IEXTEN | termios.ISIG)
    termios.tcsetattr(sys.stdin,1,mode)
    print(helpers.escape('?1003h'),end='') # click detection
    print(helpers.escape('?1006h'),end='') # make it better
    print(helpers.escape('?25l'),end='') # hide cursor
    print(helpers.escape('?7h'),end='') # don't  line wrap
    print(helpers.escape('2J'),end=helpers.escape('H'),flush=True) # clear screen
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
	mousenames = {0:'Click',33:'Mouse up',32:'Mouse dragged',2:'Mouse 2 down',34:'Mouse 2 dragged',64:'Scroll up',65:'Scroll down',1:'Middle mouse down',33:'Middle mouse scroll',4:'Forward button down',36:'Forward button still down',35:'Back button down'}
	if mouseid in mousenames:
		return mousenames[mouseid],x,y,'Down' if text=='M' else 'Up'
	else:
		return mouseid,x,y,'Down' if text=='M' else 'Up'

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
				return mousedata
			elif esccode[-1] in '~ABCDF':#idek what these do
				return parseMagicKeys(esccode[1:])
			else:
				raise NameError(f'Unknown escape code: {esccode}')
			esccode = ''
			break
def readchr():
    return stream.read(1)
