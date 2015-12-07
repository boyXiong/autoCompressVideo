#coding=utf-8

import os
import sys
import subprocess
import commands
#时间
import time 
import datetime

#根据一个路径获取路径下面有多少个视频路径
def GetFileWith(path):
	command = "find %s -name *.mp4" %(path)

	tupleAllVideoPath = commands.getstatusoutput(command)

	charFilter = [' ', '(', ')']

	allVideoPath = []

	allCompressionVideoPath = tupleAllVideoPath[1].split("\n")

	for tmp in allCompressionVideoPath:

		if type(tmp) == str:

			newVideoNameAllPath = ""

			tmpChar = '\\'
			for char in tmp:
				if char in charFilter:
					newVideoNameAllPath =  newVideoNameAllPath + tmpChar[0] + char
				else:
					newVideoNameAllPath += char
			allVideoPath.append(newVideoNameAllPath)
				
	return allVideoPath

#得到当前用户的桌面路径
def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


#创建文件夹 返回文件的路径
def createFolder():
	currentTime = time.localtime()
	folderName = "%d%d压缩视频" %(currentTime.tm_mon, currentTime.tm_mday)
	folderPath = GetDesktopPath() + '/' + folderName
	createCommand = "mkdir %s" %(folderPath)
	tst = commands.getstatusoutput(createCommand)
	return folderPath

#用于查看是不是还有没有没转换的视频
def needCompression(allVideoPath):
	compressionVideoFolderPath	= createFolder()

	tmpTuple = GetFileWith(compressionVideoFolderPath)

	allCompressionVideoPath = tmpTuple[1].split("\n")

	if len(allCompressionVideoPath) == len(allVideoPath):
		return False
	return True



#转换
def CompressionTranscoding(allVideoPath):
	#创建文件夹，并得到路径
	compressionVideoFolderPath	= createFolder()

	#防止重复压缩

	#得到已经压缩的视频路径 list
	allCompressionVideoPath = GetFileWith(compressionVideoFolderPath)
	
	#已经压缩了的视频
	hadCompressionVoideName = []

	for tmpVoidePath in allCompressionVideoPath:
		#得到所有已经压缩的名字
		hadCompressionVoideName.append(tmpVoidePath.split("/")[-1])

	#遍历每个的路径，开始转换

	for singlePath in allVideoPath:
		# singlePath = allVideoPath[i]
		if type(singlePath) is str:
			#这里就开始进行转换了
			#拿到本身的文件名 -1 是的到list的最后一个元素
			videoName = singlePath.split("/")[-1]


			if videoName in hadCompressionVoideName :
				print "video %s had Compression" %(videoName)
				#执行下面的循环
				continue 

			#拼接压缩路径
			videoCompressionPath = compressionVideoFolderPath + "/" + videoName
			#执行shell 转码

			command = "/usr/local/bin/ffmpeg -i %s -vcodec h264 -s 1280*720 -r 6 %s " %(singlePath, videoCompressionPath)
			
			p2 = subprocess.Popen(command,shell=True)
			
			#等待
			p2.wait()

	#循环
	start()




#开始high
def High():
	#.检查有没有视频后缀为.mp4 ,搜索路径
	videoPath = GetDesktopPath() + "/视频"

	allVideoPath = GetFileWith(videoPath)

	if len(allVideoPath) > 0:
		#转换
		CompressionTranscoding(allVideoPath)


#计算时间得到秒
def howManySecondsBefore(now , atTime):
	d1 = datetime.datetime(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
	#根据输入的参数，返回一个datetime对象
	d2 = datetime.datetime(atTime.tm_year, atTime.tm_mon, atTime.tm_mday, atTime.tm_hour, atTime.tm_min, atTime.tm_sec)
	second = (d2 - d1).seconds 

	return second


#开始运行
def start():
	#1.得到当前的详细时间
	currentTime = time.localtime()

	wantTime = "%d-%d-%d 13:00:00" %(currentTime.tm_year, currentTime.tm_mon, currentTime.tm_mday) 
	
	if currentTime.tm_hour >= 13 and currentTime.tm_min > 0 and currentTime.tm_hour < 18 :
		print "affternoon"
		wantTime = "%d-%d-%d 18:00:00" %(currentTime.tm_year, currentTime.tm_mon, currentTime.tm_mday)
	
	#当前时间大于的时候，就休眠,因为电脑可能没关退出
	elif currentTime.tm_hour >= 21:
		#休眠12个小时
		for i in (0, 1000):
			time.sleep(44)		
		

	#3.目标执行的时间
	targetTime =  time.strptime(wantTime, '%Y-%m-%d %X')

	print targetTime

	#4.离运行时间的秒
	runTimeSecond = howManySecondsBefore(currentTime, targetTime)

	print runTimeSecond
	#4.1判断当前时间 防止老师没将完
	if currentTime.tm_hour >= 18:
		print "High"
		runTimeSecond = 5

	#5.睡眠
	time.sleep(runTimeSecond)

	print "close"

	#6. 起来high
	High()



if __name__ == "__main__":
	print "start"
	start()
	


