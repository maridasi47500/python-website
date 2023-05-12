from http.server import HTTPServer, BaseHTTPRequestHandler
import sqlite3
import http.server
import socketserver
import io
import cgi
import os
import premierepage
from directory import directory
from glass import glasspage
from soda import sodapage
from premierepage import premierepage
from sqlite3 import Error
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs
from urllib import parse
from urllib.parse import urlparse
print("ok")
global __words__
__mots__ = {"/": {"debut": "salut", "quelquesmots": "La bienvenue"}, "/glass": {"debut": "mon verre"}, "/soda": {"debut": "Tous les sodas"}}
Program=directory("hi")
Program.set_path(".\\")
def render_figure():
	j=open((os.getcwd()+Program.get_path().replace(".","")+"\index.html"),"rb")
	return j.read() % (Program.gettitle(),Program.getcss(),Program.getbody(),Program.getjs())
def render_figure(filename):
	print(filename)
	myfile=os.getcwd()+"\\"+filename
	print(myfile)
	j=open(myfile,"rb")
	return j.read() % (Program.gettitle(),Program.getcss(),Program.getbody(),Program.getjs())
def render_figure(filename,Program):
	print(filename)
	myfile=Program.get_file_from_directory()+"\\"+filename
	print(myfile)
	j=open(myfile,"rb")
	#print((Program.gettitle(),Program.getcss(),Program.getbody(),Program.getjs()))
	#print(j.read())
	encoding = 'ISO-8859-1'
	Program.sethtmlcode(j.read().rstrip().decode('utf-8') % (Program.gettitle(),Program.getcss(),Program.getbody(),Program.getjs()))
	return Program
def firstpage():
	filename="index.html"
	j=open((os.getcwd()+"\\"+filename),"rb")
	Program.sethtmlcode(j.read().decode('utf-8') % (Program.gettitle()))
	return Program
def datareach():
	return render_figure("data_reach.html",Program)
def glass():
	Program=glasspage(".","glass")
	return render_figure("glass.html",Program)
def soda(query_components):
	try:
		print("my sodas")
		Program=sodapage(".\\glass","soda",query_components)
		print("my function")
		return render_figure("soda.html",Program)
	except:
		Program.sethtmlcode("erreur soda")
		return Program

	
def cleanup(url):
    try:
        return unquote(url, errors='strict')
    except UnicodeDecodeError:
        return unquote(url, encoding='latin-1')

def force_to_unicode(unicode_or_str):
	if isinstance(unicode_or_str, str):
		text = unicode_or_str
		decoded = False
	else:
		text = unicode_or_str.decode(encoding)
		decoded = True
	return text


class web_server(BaseHTTPRequestHandler):
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
	def _get_erreur(self):
		print("erreur")
		#print("erreur",e)
		print(self.path)
		
		self.send_header('Location',self.path)
		self.send_header('Content-type', 'text/html')
		self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))
		self.end_headers()
		
	def _get_erreur_post(self):
		#print("erreur",e)
		print(self.path)
		
		self.send_header('Location',self.path)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
	def do_GET(self):
		try:
			#Program=premierepage("hi")
			#Program.set_path(os.getcwd())
			try:
				query = self.path.split("?")[1]
			except:
				query=""
			print(query)
			if query == "":
				query_components = params = {}
			else:
				query_components = params = dict(qc.split("=") for qc in query.split("&"))
			mesposts=""
			print(self.path)
			if self.path == "/datareach":
				Program=datareach()
			if self.path == "/glass":
				Program=glass()
				print("ok glass")		
			if self.path == "/":
				Program=firstpage()
			print("ok")
			code=Program.gethtmlcode()
			for path in __mots__:
				mots=__mots__[path]
				try:
					qqmots=code.index(mots["quelquesmots"])
				except:
					qqmots=False
				try:
					debut=code.index(mots["debut"])
				except:
					debut=False
				try:
					partie=code.index(mots["partiedemesmots"])
				except:
					partie=False
				try:
					fin=code.index(mots["findemesmots"])
				except:
					fin=False
				try:
					if (qqmots | fin | debut | partie):
						Program.file(200)
						break
				except Exception as e:
					print("erreur",e)
					
						
				print("code 200")
			if Program.get_code() == 200:	
				print(code.encode('utf-8'))
				#self.send_header('Location',self.path)
				print("code 200 ok")
				self._set_response()
				self.wfile.write(code.encode('utf-8'))
			

		except Exception as e:
			print("erreur",e)
			self._get_erreur()
	def do_POST(self):
		try:
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
				str(self.path), str(self.headers), post_data.decode('utf-8'))
			#self._set_response()

			params = fields = parse.parse_qs(post_data.decode('utf-8'))
			print(params, "query components")
			if self.path == "/soda":
				Program=soda(params)
				print("code ok", self.path)
				print(Program.gettitle(), "titre")	
			code=Program.gethtmlcode()		
			for path in __mots__:
				mots=__mots__[path]
				try:
					qqmots=code.index(mots["quelquesmots"])
				except:
					qqmots=False
				try:
					debut=code.index(mots["debut"])
				except:
					debut=False
				try:
					partie=code.index(mots["partiedemesmots"])
				except:
					partie=False
				try:
					fin=code.index(mots["findemesmots"])
				except:
					fin=False
				try:
					if (qqmots | fin | debut | partie):
						Program.file(200)
						break
				except Exception as e:
					print("erreur",e)

			code=Program.gethtmlcode()
			if Program.get_code() == 200:
				print("code 200")
				print(code.encode('utf-8'))
				#self.send_header('Location',self.path)
				print("code 200 ok")
				self._set_response()
			#self.send_response(301)
			#self.send_header('Location','/')
			#self.end_headers()
			self.wfile.write(code.encode('utf-8'))
		except Exception as e:
			print("erreur 1",e)
			self._get_erreur_post()
httpd = HTTPServer(('localhost', 8080), web_server)
print("http://localhost:8080")
httpd.serve_forever()
