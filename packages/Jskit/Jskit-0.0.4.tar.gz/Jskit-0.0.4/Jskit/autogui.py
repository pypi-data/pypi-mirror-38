from time import sleep
import pyautogui
import threading


class autogui():
	'''auto gui everything!'''

	def __init__(self):
		self.getter = None # get the ctrl+c content
		pyautogui.PAUSE = 0.5
		pyautogui.FAILSAFE = False


	def copy(self):
		'''use promopt frame to get the contnet'''
		self.getter = pyautogui.prompt(text='', title='' , default='')


	def confirm(self):
		'''confirm the promopt frame'''
		pyautogui.hotkey('ctrlleft', 'v')
		sleep(1)
		pyautogui.press('enter')


	def get_copy(self):
		'''use threading to skip the block of the thread'''
		process_copy = threading.Thread(target=self.copy, name='process_copy')
		process_confirm = threading.Thread(target=self.confirm, name='process_confirm')
		process_copy.start()
		sleep(1)
		process_confirm.start()
		sleep(2)


	def get_position(self):
		'''get the position of mouse, should run this method in a terminal to quit easily'''
		print('Press Ctrl-C to quit!')
		try:
			while True:
				x, y = pyautogui.position()
				positionStr = 'X: {} Y: {}'.format(*[str(x).rjust(4) for x in [x, y]])
				print(positionStr, end='')
				print('\b' * len(positionStr), end='', flush=True)
		except KeyboardInterrupt:
			print('\n')




# ag = autogui()
# ag.get_copy()
# # ag.get_position()
# print(ag.getter)