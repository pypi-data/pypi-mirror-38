from .. import main as xterm
from threading import Thread
def frame():
	pass
def start(*,fps=5):
	xterm.clear()
	print('done')
	while True:
		c = xterm.readchr()
		if type(c) == str:
			print(c)
		else:
			print(c,c.x,c.y)