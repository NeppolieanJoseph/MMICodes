from Tkinter import *
import tkMessageBox
from PyQt5 import *
import Tkinter
import ctypes, sys
import Tkinter as tk
from PIL import Image, ImageTk
import yaml, zipfile, webbrowser, os, sys, win32serviceutil, subprocess, pywintypes, shutil, re, time
from subprocess import Popen, PIPE, STDOUT
from tkFont import Font
from ttk import Progressbar
import ttk
from sys import exit

if os.path.exists("C:\\Rexs_Installation_log\\rexs_installation_log.log"):
		os.remove("C:\\Rexs_Installation_log\\rexs_installation_log.log")

if not os.path.exists("C:\\Rexs_Installation_log"):
		os.makedirs("C:\\Rexs_Installation_log")	
sys.stdout = open("C:\\Rexs_Installation_log\\rexs_installation_log.log", 'w+')

window = Tk()
rmts_url_value='rexs-win-sqlserver-standalone.ebmxonline.com'
db_engine_value='sqlserver://rexs-win-db.ctef3gm2vljo.us-west-2.rds.amazonaws.com'
db_user_value='ruleexecutor_master'
db_pass_value='newmentor#123'
log_location_value='C:\\logs'

def ui_page():
	global CheckVar1
	global CheckVar2
	window = Tk()
	window.wm_iconbitmap('motive.ico')
	CheckVar1 = IntVar(value=1)
	CheckVar2 = IntVar()
	window.title("Welcome to REXS installation")
	window.resizable(0,0)
	window.resizable(width=FALSE, height=FALSE)
	window.geometry('560x500+150+100')
	window.configure(bg='grey')
	def repopulate_defaults(event):
		if rmts_url_txt != window.focus_get() and rmts_url_txt.get() == '':
			rmts_url_txt.insert(0, rmts_url_value)
		if db_engine_txt != window.focus_get() and db_engine_txt.get() == '':
			db_engine_txt.insert(0, db_engine_value)
		if db_user_txt != window.focus_get() and db_user_txt.get() == '':
			db_user_txt.insert(0, db_user_value)
		if db_pass_txt != window.focus_get() and db_pass_txt.get()== '':
			db_pass_txt.insert(0,db_pass_value)
		if log_location_txt != window.focus_get() and log_location_txt.get() == '':
			log_location_txt.insert(0,log_location_value)
	rows = 0
	while rows < 15:
		window.rowconfigure(rows, weight=1)
		window.columnconfigure(rows, weight=1)
		rows += 1
	lbl = Label(window,font=Font(family="Times New Roman", size=14), text="Please enter the following values", bg='grey')
	lbl.place(x=50,y=10,width=510,height=30)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Application base URL", bg='grey')
	lbl.grid(column=0, row=2, sticky="w")
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database URL", bg='grey')
	lbl.grid(column=0, row=4, sticky="w")
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database username", bg='grey')
	lbl.grid(column=0, row=6, sticky="w")
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database password", bg='grey')
	lbl.grid(column=0, row=8, sticky="w")
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Log file location", bg='grey')
	lbl.grid(column=0, row=10, sticky="w")

	rmts_url_txt = Entry(window,width=60)
	rmts_url_txt.insert(0, rmts_url_value)
	rmts_url_txt.bind('<FocusOut>', repopulate_defaults)
	rmts_url_txt.place(x=150,y=60,width=365,height=30)
	
	db_engine_txt = Entry(window,width=60)
	db_engine_txt.insert(0, db_engine_value)
	db_engine_txt.bind('<FocusOut>', repopulate_defaults)
	db_engine_txt.place(x=150,y=133,width=365,height=30)
	
	db_user_txt = Entry(window,width=60)
	db_user_txt.insert(0, db_user_value)
	db_user_txt.bind('<FocusOut>', repopulate_defaults)
	db_user_txt.place(x=150,y=210,width=365,height=30)
	
	db_pass_txt = Entry(window,show='*',width=60)
	db_pass_txt.insert(0, db_pass_value)
	db_pass_txt.bind('<FocusOut>', repopulate_defaults)
	db_pass_txt.place(x=150,y=285,width=365,height=30)
	
	log_location_txt = Entry(window,width=60)
	log_location_txt.insert(0, log_location_value)
	log_location_txt.bind('<FocusOut>', repopulate_defaults)
	log_location_txt.place(x=150,y=360,width=365,height=30)
	
	def login(*event):
		global rmts_url
		global db_engine
		global db_user
		global db_pass
		global log_location
		global data
		
		rmts_url=rmts_url_txt.get()
		db_engine=db_engine_txt.get()
		db_user=db_user_txt.get()
		db_pass=db_pass_txt.get()
		log_location=log_location_txt.get()
		
		result=tkMessageBox.askyesno("REXS Installation","Would you like to save the data and continue?")
		if result == True:
			data=db_engine.split(":")
			if data[0] == 'mysql' or data[0] == 'sqlserver':
				window.destroy()
				return rmts_url, db_engine, db_user, db_pass, log_location, data[0]
			else:
				tkMessageBox.showwarning("REXS Installation", "The RDS_db_end_point should start mysql or sqlserver")
				rmts_url_value=rmts_url
				db_engine_value=db_engine
				db_user_value=db_user
				db_pass_value=db_pass
				log_location_value=log_location
				return rmts_url_value, db_engine_value, db_user_value, db_pass_value, log_location_value
				window.destroy()
				ui_page()
		else:
			rmts_url_value=rmts_url
			db_engine_value=db_engine
			db_user_value=db_user
			db_pass_value=db_pass
			log_location_value=log_location
			return rmts_url_value, db_engine_value, db_user_value, db_pass_value, log_location_value
			window.destroy()
			ui_page()
		
	def submitted():
		window.destroy()
		exit()
		
	btn = Button(window, bg='grey',text="Install", command=login)
	btn.place(x=336,y=460,width=80,height=30)
	btn = Button(window, bg='grey',text="Cancel", command=submitted)
	btn.place(x=240,y=460,width=80,height=30)
	C1 = Checkbutton(window, text = "Launch the health check URL", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=5, bg='grey', \
                 width = 50)
	C1.place(x=190,y=420,width=280,height=15)
	C2 = Checkbutton(window, text = "Secure Server", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=5, bg='grey', \
                 width = 50)
	C2.place(x=140,y=420,width=100,height=15)
	return CheckVar1.get()
	return CheckVar2.get()
	
def pre_requist():
	cwd=os.getcwd()
	dirlist = os.listdir(cwd)
	old_label_image = None
	for f in dirlist:
		if re.search("motive-logo-transparent.png", f):
			window.wm_iconbitmap('motive.ico')
			image1 = Image.open(f)
			window.geometry('380x300+250+200')
			tkpi = ImageTk.PhotoImage(image1)
			label_image = Tkinter.Label(window, image=tkpi, background='grey')
			label_image.place(x=0,y=0,width=400,height=300)
			window.title('Motive Medical Intelligence: Rule Executor')
			window.resizable(0,0)
			if old_label_image is not None:
				old_label_image.destroy()
			old_label_image = label_image
			
			def check():
				try:
					proc=Popen('set | findstr CATALINA_HOME', shell=True, stdout=PIPE,)
					output=proc.communicate()[0]
					try:
						tmcat_home=output.split('=')[1]
					except:
						tmcat_home=''
				except:
					tmcat_home=''
					
				try:
					proc=Popen('sc queryex type= service state= all | find /i "Tomcat"', shell=True, stdout=PIPE,)
					output=proc.communicate()[0]
					try:
						tomcat_service=output.split()[1]
					except:
						tomcat_service=''
				except:
					tomcat_service=''
				try:
					proc=Popen('set | findstr JAVA_HOME', shell=True, stdout=PIPE,)
					output=proc.communicate()[0]
					try:
						java_home=output.split()[1]
					except:
						java_home=''
				except:
					java_home=''
				try:
					proc=Popen('jps', shell=True, stdout=PIPE,)
					output=proc.communicate()[0]
					try:
						java_service=output.split('=')[0]
					except:
						java_service=''
				except:
					java_service=''
					
				if java_service == '':
					tkMessageBox.showwarning("Pre-requisites", "Java and Tomcat are not installed. Please install it and continue.")
					window.destroy()
					exit()
				elif java_home=='':
					tkMessageBox.showwarning("Pre-requisites", "Set JAVA_HOME on your machine")
					window.destroy()
					exit()
				elif tomcat_service == '':
					tkMessageBox.showwarning("Pre-requisites", "Tomcat is not installed. Please install it and continue.")
					window.destroy()
					exit()
				elif tmcat_home == '':
					tkMessageBox.showwarning("Pre-requisites", "Set CATALINA_HOME on your machine")
					window.destroy()
					exit()
				else:
					tkMessageBox.showinfo("Pre-requisites","Java and Tomcat are installed")
					window.destroy()
					ui_page()
			btn = Button(window, bg='grey', text="Check Pre-requisites", command=check)
			btn.place(x=33,y=250,width=300,height=40)
			window.mainloop()
pre_requist()

proc=Popen('set | findstr CATALINA_HOME', shell=True, stdout=PIPE,)
output=proc.communicate()[0]
tmcat_home=output.split('=')[1]
	
proc=Popen('sc queryex type= service state= all | find /i "Tomcat"', shell=True, stdout=PIPE,)
output=proc.communicate()[0]
tomcat_service=output.split()[1]

proc=Popen('set | findstr JAVA_HOME', shell=True, stdout=PIPE,)
output=proc.communicate()[0]
java_home=output.split('=')[1]
		
proc=Popen('jps', shell=True, stdout=PIPE,)
output=proc.communicate()[0]
java_service=output.split()[0]

log_location=log_location.replace( '\\', '\\\\' )


if CheckVar2.get() == 0:
	http_value='http'
	flag_value='false'
else:
	http_value='https'
	flag_value='true'

host_type=rmts_url.split(':')[0]
if host_type == 'localhost' or host_type == '127.0.0.1':
	with open ('temp_token.txt', 'a+') as dup_token:
		dup_token.write('RMTS_BASE_URL==>'+http_value+'://'+rmts_url+'/rmts/api\n')
		dup_token.write('RMTS_LOG4J_FILE==>'+log_location+'\\\\rmts.log''\n')
		dup_token.write('RULE-EXECUTOR_LOG4J_FILE==>'+log_location+'\\\\rule-executor.log''\n')
		dup_token.write('RULE-EXECUTOR_SECURE_FLAG==>'+flag_value+'\n')
		dup_token.write('REXS-UI_SECURE_FLAG==>'+flag_value+'\n')
		dup_token.write('HIBERNATE_DIALECT==>org.hibernate.dialect.MySQLDialect''\n')
		dup_token.write('RULE_EX_DB_URL==>jdbc:'+db_engine+':3306/rule_ex_db\n')
		dup_token.write('RULE_EX_DB_FLYWAY_URL==>jdbc:'+db_engine+':3306\n')
		dup_token.write('RULE_EX_DB_SCHEMA==>rule_ex_db\n')
		dup_token.write('RULE_EX_DB_USER_ENCRYPTED==>'+db_user+'\n')
		dup_token.write('RULE_EX_DB_PASSWORD_ENCRYPTED==>'+db_pass+'\n')
		dup_token.write('RULE_EX_DB_DRIVER==>com.mysql.jdbc.Driver''\n')
		dup_token.write('RMTS_DB_URL==>jdbc:'+db_engine+':3306/rmts_db\n')
		dup_token.write('RMTS_DB_FLYWAY_URL==>jdbc:'+db_engine+':3306\n')
		dup_token.write('RMTS_DB_SCHEMA==>rmts_db\n')
		dup_token.write('RMTS_DB_USERNAME_ENCRYPTED==>'+db_user+'\n')
		dup_token.write('RMTS_DB_PASSWORD_ENCRYPTED==>'+db_pass+'\n')
		dup_token.write('RMTS_DB_DRIVER_CLASS==>com.mysql.jdbc.Driver')
	dup_token.close()

else:
	with open ('temp_token.txt', 'a+') as dup_token:
		dup_token.write('RMTS_BASE_URL==>'+http_value+'://'+rmts_url+'/rmts/api\n')
		dup_token.write('RMTS_LOG4J_FILE==>'+log_location+'\\\\rmts.log''\n')
		dup_token.write('RULE-EXECUTOR_LOG4J_FILE==>'+log_location+'\\\\rule-executor.log''\n')
		dup_token.write('RULE-EXECUTOR_SECURE_FLAG==>'+flag_value+'\n')
		dup_token.write('REXS-UI_SECURE_FLAG==>'+flag_value+'\n')
		dup_token.write('HIBERNATE_DIALECT==>org.hibernate.dialect.SQLServer2012Dialect''\n')
		dup_token.write('RULE_EX_DB_URL==>jdbc:'+db_engine+':1433;databaseName=rule_ex_db\n')
		dup_token.write('RULE_EX_DB_FLYWAY_URL==>jdbc:'+db_engine+':1433\n')
		dup_token.write('RULE_EX_DB_SCHEMA==>rule_ex_db\n')
		dup_token.write('RULE_EX_DB_USER_ENCRYPTED==>'+db_user+'\n')
		dup_token.write('RULE_EX_DB_PASSWORD_ENCRYPTED==>'+db_pass+'\n')
		dup_token.write('RULE_EX_DB_DRIVER==>com.microsoft.sqlserver.jdbc.SQLServerDriver''\n')
		dup_token.write('RMTS_DB_URL==>jdbc:'+db_engine+':1433;databaseName=rmts_db\n')
		dup_token.write('RMTS_DB_FLYWAY_URL==>jdbc:'+db_engine+':1433\n')
		dup_token.write('RMTS_DB_SCHEMA==>rmts_db\n')
		dup_token.write('RMTS_DB_USERNAME_ENCRYPTED==>'+db_user+'\n')
		dup_token.write('RMTS_DB_PASSWORD_ENCRYPTED==>'+db_pass+'\n')
		dup_token.write('RMTS_DB_DRIVER_CLASS==>com.microsoft.sqlserver.jdbc.SQLServerDriver')
	dup_token.close()

cwd=os.getcwd()
shutil.move('temp_token.txt', cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone')
def custom_properties_change():
	os.chdir(work_space)
	print '\nCustom.properties file updated'
	with open ('custom.properties') as custom_file:
		with open('custom_dup.txt','w+') as custom_tup:
			for line in custom_file:
				found = re.search('%%%rmts_url%%%', line)
				if found:
					line = line.replace('%%%rmts_url%%%', http_value+'://'+rmts_url)
					custom_tup.write(line)
				else:
					custom_tup.write(line)
		custom_tup.close()
	custom_file.close()
	shutil.move('custom_dup.txt', 'custom.properties' )				
def flyway_update(tokenfile):
	key=None
	value=None
	token_file=cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+'1'
	print ('\nUpdating the flyway configuration files\n')
	with open(token_file) as token_f:
			for line in token_f:
				data=line.split("==>")
				key=data[0]
				value=data[1]
				pattern = "%%%"+ key + "%%%"
				with open('tempfile.lst', 'w+') as outfile:
					with open(tokenfile, 'r') as token_replace:
						for line_replace in token_replace:
							found = re.search(pattern, line_replace)
							if found:
								line_replace = line_replace.replace(pattern, value)
								outfile.write(line_replace)
							else:
								outfile.write(line_replace)
					token_replace.close()
				outfile.close
				shutil.move('tempfile.lst', tokenfile )
	print tokenfile+' has updated\n'
def decrypt_call():
	print '\nEncrypted Username and Password\n'
	tokens_to_encrypt=['RULE_EX_DB_USER','RULE_EX_DB_PASSWORD','RMTS_DB_USERNAME','RMTS_DB_PASSWORD']
	pattern='_ENCRYPTED'
	with open(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone') as token_f:
		with open('temp_token.txt','a')as replace_file:
			for line in token_f:
				found = re.search(pattern, line)
				if not found:
					replace_file.write(line)
				else:
					for i in tokens_to_encrypt:
						dbencrypted=re.search(i+pattern, line)
						if dbencrypted:
							data=line.split("==>")
							value=data[1]
							proc=Popen('java -jar des_encryption.jar'+" "+value, shell=True, stdout=PIPE, )
							output=proc.communicate()[0]
							encrypt=output.split()[2]
							new_pattern=value
							new_pattern=line.replace(value,encrypt)
							print new_pattern
							replace_file.write(new_pattern+"\n")
			replace_file.close()
	shutil.move('temp_token.txt', cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone' )
	token_f.close()
def untokenize(tokenfile):
	line=None
	key=None
	value=None
	token_file=cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'
	print cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'
	config_tokenized=tokenfile
	config_tokenized=config_tokenized.replace( '\\', '\\\\' )
	print "tokenized file..."
	print config_tokenized
	config_untokenized=config_tokenized.replace( '_tokenized', '' )
	print "untokenized file..."
	print config_untokenized
	shutil.copy(config_tokenized, config_untokenized)
	print "Copied untokenized file successfully"
	print token_file
	print config_untokenized
	with open(token_file) as token_f:
			for line in token_f:
				data=line.split("==>")
				key=data[0]
				value=data[1]
				pattern = "%%%"+ key + "%%%"
				with open('tempfile.lst', 'w+') as outfile:
					with open(config_untokenized, 'r') as token_replace:
						for line_replace in token_replace:
							found = re.search(pattern, line_replace)
							if found:
								line_replace = line_replace.replace(pattern, value)
								outfile.write(line_replace)
							else:
								outfile.write(line_replace)
					token_replace.close()
				outfile.close
				shutil.move('tempfile.lst', config_untokenized )
def run_flyway( ):
	if db_type == "sqlserver":
		os.chdir( work_space+"\\flyway")
		cwd=os.getcwd()
		for db in config_db_names:
			if os.path.exists("conf\\sql_server\\"+db+".conf") == True:
				if flyway_update(cwd+'\\conf\\sql_server\\'+db+'.conf') != None:
					copy_token_file()
				the_output = os.popen("flyway.cmd -configFile=conf\\sql_server\\" + db + ".conf migrate").read()
		os.chdir( work_space )
	elif db_type =="mysql":
		os.chdir( work_space+"\\flyway")
		cwd=os.getcwd()
		for db in config_db_names:
			if os.path.exists("conf\\"+db+".conf") == True:
				if flyway_update(cwd+'\\conf\\'+db+'.conf') != None:
					copy_token_file()
				the_output = os.popen("flyway.cmd -configFile=conf\\" + db + ".conf migrate").read()
		os.chdir( work_space )
	else:
		print "\nError::Please Enter the correct database name in the config.yaml file"
		copy_token_file()
		remove_unwanted()
		delete_unwanted_in_workspace()
		exit()
def read_config():
	global work_space
	global cat_home
	global db_type
	global config_artifacts
	global config_db_names
	global tomcat_home
	
	cwd=os.getcwd()
	with open("config.yaml", 'r') as stream:
		try:
			yaml_config_doc = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			pass
	config_artifacts=yaml_config_doc['artifacts']
	config_db_names=yaml_config_doc['db_names']
	work_space=cwd
	cat_home=tmcat_home
	db_type=data[0]
	tomcat_home=tomcat_service

	if work_space==None or cat_home==None or db_type==None or config_artifacts==None or tomcat_home==None or config_db_names==None:
		print "\nFill All field in the YAML config file All Fields should get value"
		exit()
	return 0
def tomcat_control(action):
	if action == 'stop':
		if win32serviceutil.QueryServiceStatus(tomcat_home)[1] == 4:
			win32serviceutil.StopService(tomcat_home)
			print 'Tomcat Version='+tomcat_home
			print "\nTomcat is Stopped"
		else:
			print "\nTomcat Already Stopped"
			pass
	else:
		if win32serviceutil.QueryServiceStatus(tomcat_home)[1] != 4:
			win32serviceutil.StartService(tomcat_home)
			print "\nPlease wait for 60 seconds " +tomcat_home+ " is loading..."
			time.sleep(60)
def deploy_war(arfifact):
	os.chdir(cat_home.strip('\r\n') +'\\webapps')
	if os.path.exists(cat_home.strip('\r\n') +'\\webapps\\'+arfifact+'.war')==True:
		print 'Deleting old '+arfifact+'.war'
		shutil.rmtree(cat_home.strip('\r\n') +'\\webapps\\'+arfifact, ignore_errors=True)
	shutil.copyfile(work_space+'\\'+arfifact+'.war', cat_home.strip('\r\n') +'\\webapps' + '\\' + arfifact + '.war')
def un_zip(workspace, cathome):
	try:
		os.chdir(workspace)
	except (KeyboardInterrupt,IOError,pywintypes.error,WindowsError) as e:
		print str(e)
		pass
	zip_ref = zipfile.ZipFile(workspace+'\\bundle.zip', 'r')
	zip_ref.extractall(workspace)
	for artifacts_item in config_artifacts:
		print "\n deploying %s ..." % artifacts_item
		tempdir="%s_temp" % artifacts_item
		if not os.path.exists(tempdir):
			os.makedirs(tempdir)
		os.chdir(tempdir)
		the_output = os.popen('jar xf ' + workspace + '\\'+artifacts_item + '.war').read()
		os.remove(workspace + '\\'+artifacts_item + '.war')
		token_file_tmp=subprocess.Popen("dir/s/b *_tokenized", stdout=subprocess.PIPE, shell=True).communicate()
		token_file_tmp=token_file_tmp[0].split('\n')
		print token_file_tmp[0].strip('\r')
		for item in token_file_tmp:
			print "\nIterating token file to get untokenize..\n"
			if "tokenized" in item:
				item = item.strip('\r\n')
				print item
				if untokenize(item) != None:
					copy_token_file()
				print "\nUntokenized - %s" % item
		print "\nExecute building war file..."
		the_output = os.popen('jar cf ' + workspace + '\\'+artifacts_item + '.war  *').read()
		print "\nBuild completed - %s.war" % artifacts_item
		os.chdir(workspace)
		print "\nRemoving the temp dir..."
		shutil.rmtree(tempdir, ignore_errors=True)
		print "\ntemp dir removed..."
		print "\nDeploying war..."
		print "artifacts_item"
		print artifacts_item
		deploy_war(artifacts_item)
		print "\n %s deployed!" % artifacts_item
	try:
		print '\n Taking Backup the flyway conf files'
		flyway_conf_duplicate()
	except (KeyboardInterrupt,IOError,pywintypes.error,WindowsError) as e:
		delete_conf_files()
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	try:
		print '\n Running Migration from flyway'
		run_flyway( )
	except (IOError,pywintypes.error,WindowsError) as e:
		print '\nError:::'+str(e)
		copy_flyway_conf_to_original()
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except KeyboardInterrupt as e:
		print '\n The Deployment is stoped by keyboard Interrupt'
		copy_flyway_conf_to_original()
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	return 0
def remove_unwanted():
	rootfolder=['ROOT','examples','docs']
	for filename in rootfolder:
		os.chdir(cat_home.strip('\r\n')+"\\webapps")
		if os.path.exists(filename)==True:
			shutil.rmtree(filename, ignore_errors=True)
	for f in os.listdir(cat_home.strip('\r\n')+"\\webapps"):
		os.chdir(cat_home.strip('\r\n')+"\\webapps")
		if re.search("_temp", f):
			shutil.rmtree(f, ignore_errors=True)
	for f in os.listdir(work_space):
		os.chdir(work_space)
		if re.search(".war", f):
			os.remove(f)
def copy_token_file():
	shutil.copyfile(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1", cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone')
	os.remove(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1")
def delete_unwanted_in_workspace():
	try:
		for f in os.listdir(work_space):
			os.chdir(work_space)
			if re.search(".war", f):
				os.remove(f)
			if re.search("_temp", f):
				shutil.rmtree(f, ignore_errors=True)
	except (KeyboardInterrupt,IOError,pywintypes.error,WindowsError) as e:
		print str(e)
		pass
def copy_flyway_conf_to_original():
	for i in config_db_names:
		if db_type == "sqlserver":
			shutil.move(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1', work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf')
		if db_type == "mysql":
			shutil.move(work_space+'\\flyway\\conf\\'+i+'.conf1', work_space+'\\flyway\\conf\\'+i+'.conf')
def flyway_conf_duplicate():
	for i in config_db_names:
		if db_type == "sqlserver":
			shutil.copyfile(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf', work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1')
		if db_type == "mysql":
			shutil.copyfile(work_space+'\\flyway\\conf\\'+i+'.conf', work_space+'\\flyway\\conf\\'+i+'.conf1')
def delete_conf_files():
	for i in config_db_names:
		if db_type == "sqlserver" and os.path.exists(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1'):
			os.remove(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1')
		if db_type == "mysql" and os.path.exists(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1'):
			os.remove(work_space+'\\flyway\\conf\\'+i+'.conf1')
def progress_bar(bar_value,percent):
	percent_val=str(percent)
	progress['value']=bar_value
	tk.update_idletasks()
	lbl = Label(tk, text=percent_val+'%', bg='grey', fg='purple')
	lbl.place(x=420,y=310,width=30,height=20)
	time.sleep(1)
def print_lable(stmnt):
	lbl = Label(tk, text=stmnt, bg='CadetBlue4', fg='purple')
	lbl.place(x=47,y=70,width=366,height=100)
	time.sleep(4)
def main():
	global progress
	global tk
	tk=Tk()
	tk.wm_iconbitmap('motive.ico')
	tk.title("REXS installation")
	tk.resizable(0,0)
	tk.resizable(width=FALSE, height=FALSE)
	tk.geometry('460x400+250+200')
	tk.configure(bg='grey')
	lbl = Label(tk, text="REXS Installation in progress", bg='grey', fg='purple')
	lbl.place(x=47,y=40,width=366,height=20)
	lbl = Label(tk, text="-----------------------------------------------", bg='grey', fg='purple')
	lbl.place(x=47,y=180,width=366,height=20)
	progress=ttk.Progressbar(tk,orient=HORIZONTAL,length=370, mode='determinate')
	def bar():
		print '\nTaking Backup for tokens file'
		shutil.copyfile(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone', cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1")
		print '\nTaking Backup for custom.properties file'
		shutil.copy('custom1.properties','custom.properties')
		try:
			decrypt_call()
			print_lable("User name and passwords are encrypted")
			progress_bar(20,20)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\n'+str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		except (KeyboardInterrupt) as e:
			print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		try:
			read_config()
			print_lable("Read the db and artifacts details from config file")
			progress_bar(30,40)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\nError in read the configuration file'
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		except (KeyboardInterrupt) as e:
			print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()

		try:
			tomcat_control('stop')
			print_lable("Tomcat stoped for the installation progress")
			progress_bar(40,60)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\nTomcat is not available in this machine please Install tomcat'
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		except (KeyboardInterrupt) as e:
			print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		try:
			un_zip( work_space, cat_home)
			progress_bar(50,80)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\n'+str(e)
			copy_token_file()
			remove_unwanted()
			delete_unwanted_in_workspace()
			exit()
		except (KeyboardInterrupt) as e:
			print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
			copy_token_file()
			remove_unwanted()
			delete_unwanted_in_workspace()
			exit()
		try:
			remove_unwanted()
			progress_bar(90,90)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\nThe removing files are not in the location.'
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		try:
			tomcat_control('start')
			progress_bar(100,95)
		except (IOError,pywintypes.error,WindowsError) as e:
			print '\nProblem in starting the'+ tomcat_home +'service'
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		except (KeyboardInterrupt) as e:
			print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
		custom_properties_change()
		os.chdir(work_space)
		if os.path.exists(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1")==True:
			copy_token_file()
		copy_flyway_conf_to_original()
		delete_conf_files()
		progress_bar(120,100)
		time.sleep(9)
		tkMessageBox.showinfo("Installation completed","REXS installed successfully on you machine.\n Please check the log file C:\\Rexs_Installation_log\\rexs_installation_log.log ")
		if CheckVar1.get() == 1:
			print '\nPlease wait health check URL is Launching'
			webbrowser.open(http_value+'://'+rmts_url+'/ruleexecutor/healthcheck.html')
		exit()
	progress.pack(fill='y', side='bottom', padx=20, pady=70)
	bar()
	tk.mainloop()
if __name__=="__main__":
	main()
