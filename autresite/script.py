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
from soda import deletesodaaction
from logoutsite import logoutfunc
from premierepage import premierepage
from datareach import datareachpage
from inscription import inscriptionpage
from connexion import connexionpage
from user import userpage
from user import infouserpage
from sqlite3 import Error
from urllib.parse import unquote
from urllib.parse import urlparse, parse_qs
from urllib import parse
from random import randint
from urllib.parse import urlparse
sessions = {}
print("ok")
global __words__
__mots__ = {"/deletesoda":{"debut":"juste pour voir"},"/datareach":{"debut":"juste pour voir"},"/": {"debut": "salut", "quelquesmots": "La bienvenue"}, "/glass": {"debut": "mon verre : choisir un soda"},"/deconnexion":{"debut":"déconnecté(e)"}, "/soda": {"debut": "Tous les sodas"},"/connexion":{"debut":"Connexion"},'/inscription':{"debut":"Inscription"}}
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
	if Program.get_code() == 301:
		return Program
	print(filename)
	myfile=Program.get_file_from_directory()+"\\"+filename
	print(myfile)
	j=open(myfile,"rb")
	jcontent=j.read()
	encoding = 'ISO-8859-1'
	print(Program.gettitle(),"=title",Program.getcss(),"=css",Program.getbody(),"=body",Program.getjs(),"=js")
	Program.sethtmlcode(jcontent.decode('utf-8') % (Program.gettitle(),Program.getcss(),Program.getbody(),Program.getjs()))
	return Program
def infouser(params):	
	Program=infouserpage(".\\user","à propos",params)
	return render_figure("user.html",Program)
def datareach(params):
	Program=datareachpage(".","à propos de ce site web")
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
	username=""
	def generate_sid(self):
		return "".join(str(randint(1,9)) for _ in range(100))
	def parse_cookies(self, cookie_list):
		return dict(((c.split("=")) for c in cookie_list.split(";"))) if cookie_list else {}
	def _set_response(self,headertype='text/html'):
		self.send_response(200)
		self.send_header('Content-type', headertype)
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
	def inscriptionform(self):
		Program = inscriptionpage("hello")
		Program.inscriptionform(".\connexion","inscription")
		return render_figure("inscription.html",Program)
	def connexionform(self):
		Program = connexionpage("hello")
		Program.connexionform(".\connexion","connexion")
		return render_figure("connexion.html",Program)
	def firstpage(self,params):
		Program=premierepage(".",params, "hello",self.username)
		return render_figure("index.html",Program)
	def inscription(self,params):
		Program = inscriptionpage("hello")
		Program.inscription(".\connexion","inscription",params)
		self.username=Program.getusername()
		if Program.getusername():
			sid = self.generate_sid()
			self.cookie = "sid={}".format(sid)
			sessions[sid] = {Program.getusername()}
		return render_figure("inscription.html",Program)
	def connexion(self,params):
		Program = connexionpage("hello")
		print("program init")
		Program.connexion(".\connexion","connexion",params)
		self.username=Program.getusername()
		print("program ok",Program.getusername())
		if Program.getusername():
			sid = self.generate_sid()
			self.cookie = "sid={}".format(sid)
			sessions[sid] = {Program.getusername()}
		return render_figure("connexion.html",Program)
	def deletesoda(self,params):
		Program = deletesodaaction("hello",params)
		print("program init")
		return render_figure("connexion.html",Program)
	def mylogoutfunc(self,cookies):
		try:
			print("deconnexion",cookies)
			Program=directory("log  out")
			Program.set_path("\connexion")
			if not self.username:
				print("pas de nom d'utilisateyr")
				#Program.setbody("impossible de se déconnecter : aucun(e) utilisateur(trice) connecté(e)<a href=\"/\">Retour</a>")
				
				print("okok")
			else:
				try:
					print("log out")
					self.cookie = "sid="
					print(cookies,"cookies")
					print(sessions,"sessions")
					
					print(cookies["sid"],sessions[cookies["sid"]])
					del sessions[cookies["sid"]]
				except Exception as e:
					print(e,"erreur log out")
				print("log out ok")
			 #Program.work(200)
		except Exception as erreur:
			print(erreur)
		
		return render_figure("logout.html",Program)
	def do_GET(self):
		try:  
			#Program=premierepage("hi")
			#Program.set_path(os.getcwd())
			#self.cookie = "sid={}".format(sid)
			print(self.path, "path ok")
			cookies = self.parse_cookies(self.headers["Cookie"])
			self.cookie = None # Addition
			if "sid" in cookies:
				self.username= list(sessions[cookies["sid"]])[0] if (cookies["sid"] in sessions) else False
			else:
				print("pas de nom utilisateur dans les cookies")
				self.username = False
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
			query_components["username"]=self.username
			if self.path == "/datareach":
				Program=datareach(query_components)
			if self.path == "/infouser":
				Program=infouser(query_components)
			if self.path == "/glass":
				Program=glass()
				print("ok glass")	
			if self.path == "/connexion":
				Program=self.connexionform()
				print("ok connexion")	
			if self.path == "/inscription":
				Program=self.inscriptionform()
				print("ok connexion")	
			if self.path == "/deconnexion":
				print("deconnexion")
				Program=self.mylogoutfunc(cookies)
				print("ok deconnexion")	
			if self.path == "/":
				print("premiere page")
				Program=self.firstpage(query_components)
				print("ok firstpage")	
			print("ok")
			try:
				code=Program.gethtmlcode()
			except:
				code=None
			#for path in __mots__:
			#path=__mots__[self.path]
			try:
				mots=__mots__[self.path]
			except:
				print("erreur mots")
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
					#break
			except Exception as e:
				print("erreur 123",e)		
			print("code 200")
			if self.cookie:
				self.send_header('Set-Cookie', self.cookie) # Addition
			if self.path.split("?")[0].split(".")[-1] in ["css"]:
				print("c'est du css")
				code=open(os.getcwd()+self.path.replace("/","\\"),"rb").read()
				print(code.decode('utf-8'))
				#self.send_header('Location',self.path)
				print("code 200 ok (css)")
				
				self._set_response("text/css")
				self.wfile.write(code)
			elif Program.get_code() == 301:
				print("code 301",Program.get_redirect())
				self.send_response(301)
				self.send_header('Location',Program.get_redirect())
				
				self.end_headers()
			elif Program.get_code() == 200:
	
				print(code.encode('utf-8'))
				#self.send_header('Location',self.path)
				print("code 200 ok")
				
				self._set_response()
				self.wfile.write(code.encode('utf-8'))

			

		except Exception as e:
			print("erreur 0987",e)
			self._get_erreur()
	def do_POST(self):
		try:
			content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
			post_data = self.rfile.read(content_length) # <--- Gets the data itself
			print("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
				str(self.path), str(self.headers), post_data.decode('utf-8'))
			#self._set_response()
			cookies = self.parse_cookies(self.headers["Cookie"])
			self.cookie = None # Addition
			params = fields = parse.parse_qs(post_data.decode('utf-8'))
			
			print(params, "query components")
			if self.path == "/soda":
				Program=soda(params)
				print("code ok", self.path)
				print(Program.gettitle(), "titre")
			if self.path.split("?")[0] == "/connexion":
				Program=self.connexion(params)
				print("ok connexion")	
			if self.path.split("?")[0] == "/deletesoda":
				Program=self.deletesoda(params)
				print("ok delete soda")	
			if self.path.split("?")[0] == "/inscription":
				Program=self.inscription(params)
				print("ok connexion")		
			code=Program.gethtmlcode()		
			mots=__mots__[self.path]
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
				else:
					print("aucun mot trouvé")
			except Exception as e:
				print("erreur 987578",e)

			code=Program.gethtmlcode()			
			print("code 200")

			if Program.get_code() == 301:
				print("code 301",Program.get_redirect())
				self.send_response(301)
				self.send_header('Location',Program.get_redirect())			
				if self.cookie:
					self.send_header('Set-Cookie', self.cookie) # Addition
				self.end_headers()
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
