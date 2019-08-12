#coding:utf-8
#Python中声明文件编码的注释，编码格式指定为utf-8

import time					#导入time库，可使用时间函数。

print 'Hello World!'		#打印字符串： Hello World！ ，注意使用单引号。
for i in range(1,10):		#调用rang（）循环函数，功能类似 for（i =1;i<10;i++ ）

	print 'i =  %d '%i		#（TAB键）把i的当前值打印出来

	time.sleep(0.5)			#（TAB键）time中的延时函数，单位为秒，此处是延时0.5s
'''
整个程序功能为：
	打印 Hello World!
	每隔0.5s，从i = 1打印到 i = 9
	程序结束
'''