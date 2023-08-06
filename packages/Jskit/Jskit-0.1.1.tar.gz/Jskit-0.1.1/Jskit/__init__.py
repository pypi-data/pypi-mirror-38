import logging
import os
import platform


def log_init():
	'''加入run.log，信息打印到屏幕和log文件'''
	logger = logging.getLogger(__name__)
	logging.basicConfig(level=logging.ERROR,
				format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
				datefmt='%a, %d %b %Y %H:%M:%S',
				filename='run.log',
				filemode='w')
	handler = logging.StreamHandler()
	handler.setLevel(logging.INFO)
	formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	if platform.system() == 'Windows':
		logging.info('执行系统：Windows')
	elif platform.system() == 'Linux':
		logging.info('执行系统：Linux')
	else:
		logging.info('执行系统：Unknown!')

#-----------------------------------------------------------------------------------------------
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.ERROR)
# handler = logging.FileHandler('run.log')
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


# logging.basicConfig(level=logging.INFO,
# 			format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
# 			datefmt='%a, %d %b %Y %H:%M:%S',
# 			filename='run.log',
# 			filemode='w')
# console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# console.setFormatter(formatter)
# logging.getLogger('').addHandler(console)