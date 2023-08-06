import base64
import sys
from color_lib import colors

def run():
	colors.init()

	loop = True

	print(colors.fg.cyan('Welcome to the'), colors.bold(colors.fg.lightcyan('Python2 Base64 Util')), colors.fg.cyan('!'))

	while loop:
		print(colors.fg.orange('Valid actions are: {0}, {1}, {2}').format(colors.fg.yellow('encode'), colors.fg.yellow('decode'), colors.fg.yellow('quit')))
		action = input(colors.fg.cyan('What do you want to do? '))
		if action.lower() == 'encode':
			string = input(colors.fg.purple('\nInput the string to encode: '))
			print(colors.fg.green('Your encoded Base64 string is: '), str(base64.b64encode(bytes(string.encode('utf-8'))), 'utf-8'), '\n')
		elif action.lower() == 'decode':
			string = input(colors.fg.purple('\nInput the string to decode: '))
			print(colors.fg.green('Your decoded Base64 string is: '), str(base64.b64decode(bytes(string.encode('utf-8'))), 'utf-8'), '\n')
		elif action.lower() == 'quit':
			loop = False
		else:
			print(colors.bg.black(colors.fg.red('Invalid action\n')))
