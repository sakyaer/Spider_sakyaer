# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import sys

#[x]TODO：精简代码
class Spider:
	def __init__(self):
		self.url = 'http://www.napiantian.com/index.php?i='
		self.curPage = ""
		self.file = None
		self.contents = []
	
	#获得一个网页的内容
	def getPage(self,pageIndex):
		pageUrl = self.url+str(pageIndex)
		#self.contents.append(pageUrl)
		print(pageUrl)
		try:
			request = urllib2.Request(pageUrl)
			response =  urllib2.urlopen(request)
			return response.read()
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print "文章ID："+str(pageIndex)+"不存在，错误原因：",e.reason
				return None
			
	#根据正则式解析html标签
	def getContents(self,pageIndex,param,line):
		pattern = re.compile(param,re.S)
		title = re.findall(pattern,self.curPage)
		if title:
			for item in title:
				self.contents.append(str(item))
			if line:
				self.contents.append('\n\n\n')
			else:
				self.contents.append('\n')
		else:
			print("Conn't Find ")
			self.contents = []
			
	#本地文件写入		
	def saveDate(self):
		try:
			for item in self.contents:
				self.file.write(str(item))
				#print str(item)
		except IOError,e:
			print "Write Error "+e.message
		finally:
			print "Write Finish Article"
	
	#主程序循环
	def loopGet(self, pageCount):
		self.contents = []
		for i in range(1,(pageCount+1)):
			print("Download No: "+str(i)+" ......")
			self.curPage = self.getPage(i)
			self.contents.append("第"+str(i)+"章 ")
			self.getContents(i,r'<div class="h1"><br><br>(.*?)</div>',0)						#Title
			self.getContents(i,r'<div style="color:#888"><br><br><br>(.*?)<br>',0)				#Author
			self.contents.append("\n")		
			self.getContents(i,r'<p class="p1">(.*?)</p>',1)									#Content
			self.saveDate()
			self.contents = []
	
SpiderIns = Spider()
#fileName = raw_input("Input the name of file:\n")
#numPage = raw_input("Input the number of downloading webpage:\n")
fileName = 'Napiantian'
numPage = 240
SpiderIns.file = open(fileName+".txt","w+")
SpiderIns.loopGet(int(numPage))
SpiderIns.file.close()
#quitFlag = raw_input("\nCtrl+Z quit the application")

