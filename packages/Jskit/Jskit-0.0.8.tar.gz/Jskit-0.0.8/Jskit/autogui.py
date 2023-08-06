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


	def auto_login(self, url, username, passwd, tab_times=0, pause=False):
		'''login in template'''
		os.system('nohup google-chrome 2>&1 &')#不占终端运行
		sleep(3)
		pyautogui.hotkey('ctrlleft', 'shiftleft', 'n')
		sleep(3)
		pyautogui.hotkey('ctrlleft', 'winleft', 'up')
		# pyautogui.hotkey('ctrlleft', 'altleft', '5') # Ubuntu server?
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
		if pause:
			pyautogui.alert('Next') # 手动输入验证码时，暂停
		pyautogui.press('enter')
		sleep(3)


	def copy(self):
		'''use gedit to get the contnet'''
		os.system('nohup gedit temp') # self.getter = pyautogui.prompt(text='', title='' , default='')


	def confirm(self):
		'''confirm the promopt frame'''
		pyautogui.hotkey('ctrlleft', 'v')
		sleep(3)
		pyautogui.hotkey('ctrlleft', 's')
		sleep(3)
		pyautogui.hotkey('altleft', 'f4')


	def get_copy(self):
		'''use threading to skip the block of the thread'''
		try:
			os.remove('temp')
		except:
			pass
		
		process_copy = threading.Thread(target=self.copy, name='process_copy')
		sleep(2)
		pyautogui.hotkey('ctrlleft', 'c')
		sleep(2)
		process_copy.start()
		sleep(1)
		self.confirm()
		sleep(2)

		with open ('temp', 'r') as temp:
			self.getter = temp.read()


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