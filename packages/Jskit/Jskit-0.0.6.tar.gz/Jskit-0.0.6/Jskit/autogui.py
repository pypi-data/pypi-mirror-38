from time import sleep
import pyautogui
import threading
import os

class autogui():
	'''auto gui everything!'''

	def __init__(self):
		self.getter = None # get the ctrl+c content
		pyautogui.PAUSE = 0.5
		pyautogui.FAILSAFE = False


	def auto_login(self, url, username, passwd, tab_times=0):
		'''login in template'''
		os.system('nohup google-chrome 2>&1 &')#不占终端运行
		sleep(3)
		pyautogui.hotkey('ctrlleft', 'shiftleft', 'n')
		sleep(3)
		pyautogui.hotkey('ctrlleft', 'winleft', 'up')
		sleep(3)
		pyautogui.typewrite(url ,0.1)
		pyautogui.press('enter')
		sleep(3)
		for item in range(tab_times):
			pyautogui.press('tab')
			sleep(1)
		pyautogui.typewrite(username,0.1)
		sleep(3)
		pyautogui.press('tab')
		pyautogui.typewrite(passwd,0.1)
		sleep(3)
		pyautogui.press('enter')
		sleep(3)


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
		pyautogui.hotkey('ctrlleft', 'c')
		sleep(2)
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