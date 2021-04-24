#!/usr/bin/env python
#----------------------------------------------------------------
#	Note:
#		ds18b20's data pin must be connected to pin7.
#		replace the 28-XXXXXXXXX as yours.
#----------------------------------------------------------------
import os  #导入操作系统的库os

ds18b20 = ''

def setup():
	global ds18b20
	for i in os.listdir('/sys/bus/w1/devices'):
	#os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
	
		if i != 'w1_bus_master1':
	#里面除了文件'w1_bus_master1'，另外一个就是温度数据文件所在的文件夹
	
			ds18b20 = i   
	#将温度数据文件所在的文件夹名赋值给全局变量ds18b20

def read():

	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
	#location是温度数据文件的地址
	
	tfile = open(location)  
	#os.open(file, flags[, mode])打开一个文件
	text = tfile.read()     
	#  os.read(fd, n)从文件描述符 fd 中读取最多 n 个字节，返回包含
	#  读取字节的字符串，文件描述符 fd对应文件已达到结尾, 返回一个空字符串。
	
	tfile.close()
	#os.close(fd)关闭文件描述符 fd
	
	secondline = text.split("\n")[1]
	#   string.split(str="", num=string.count(str))
	#   以 str 为分隔符切片 string，如果 num 有指定值，则仅分隔 num+ 个子字符串
	#计算机里序号是从0开始计算，取1即是第二行
	
	temperaturedata = secondline.split(" ")[9]
	#以空格为分隔符，取序号为9的字符段，如：t=17375
	
	temperature = float(temperaturedata[2:])
	#取字符串（如：t=17375）第2位及以后部分，即数字部分17375
	
	temperature = temperature / 1000
	return temperature
	
def loop():
	while True:
		if read() != None:
			print "Current temperature : %0.3f C" % read()
           #以单精度浮点小数的形式输出，保留三位小数
def destroy():
	pass

if __name__ == '__main__':
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()


