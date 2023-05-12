import os
class directory():
	def __init__(self,title):
		self.title=title
		self.css=""
		self.js=""
		self.body=""
		self.path=""
		self.code=""
		self.htmlcode=""
		self.url=""
	def get_path(self):
		return self.path
	def work(self,code):
		self.code=code
	def get_code(self):
		return self.code
	def file(self,code):
		self.code=code
	def redirect(self,path):
		self.url=path
	def get_redirect(self):
		return self.url
	def set_path(self,path):
		self.path=path
	def get_file_from_directory(self):
		return os.getcwd()+self.get_path().replace(".","")
	def getcss(self):
		return self.css
	def getjs(self):
		return self.js
	def setbody(self,body):
		self.body=body
	def sethtmlcode(self,code):
		self.htmlcode=code
	def gethtmlcode(self):
		return self.htmlcode
	def getbody(self):
		return self.body
	def gettitle(self):
		return self.title