def escape(code):
	return '\033['+code
def getrgb(r,g,b):
	return escape(f'38;2;{r};{g};{b}m')
def gethex(hexdata):
	return getrgb(*tuple(int(hexdata[i:i+2], 16) for i in (0, 2 ,4)))
def graphic(_id):
	names = {
		'reset':0,
		'bold':1,
		'faint':2,
		'italic':3,
		'reverse':7,
		'conceal':8,
		'reveal':28,
		'black':30,
		'darkred':31,
		'darkgreen':32,
		'orange':33,
		'darkblue':34,
		'darkmagenta':35,
		'darkcyan':36,
		'gray':37,
		'gray2':90,
		'red':91,
		'green':92,
		'yellow':93,
		'blue':94,
		'magenta':95,
		'cyan':96,
		'white':97
	}
	if str(_id).lower() in names:
		_id = names[_id]
	return escape(f'{_id}m')
