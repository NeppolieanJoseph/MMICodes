from Tkinter import *
import tkMessageBox
from PyQt5 import *
import Tkinter
import shutil, re, time
from PIL import Image, ImageTk
import yaml
import zipfile
import os, sys
import win32serviceutil
import subprocess
import shutil, re, time
from subprocess import Popen, PIPE, STDOUT
import pywintypes
from tkFont import Font

window = Tk()

rmts_url_value='rexs-win-sqlserver-standalone.ebmxonline.com'
db_engine_value='sqlserver://rexs-win-db.ctef3gm2vljo.us-west-2.rds.amazonaws.com'
db_user_value='ruleexecutor_master'
db_pass_value='newmentor#123'
log_location_value='C:\\logs'

def ui_page():
	#font=Font(family="Times New Roman", size=12)
	window = Tk()
	window.title("Welcome to MMI Installation Page")
	window.resizable(0,0)
	window.resizable(width=FALSE, height=FALSE)
	window.geometry('600x500')
	window.configure(bg='grey')
	
	def clear_widget(event):
		
		if rmts_url_txt == window.focus_get() and rmts_url_txt.get() == rmts_url_value:
			rmts_url_txt.delete(0, END)
		
		if db_engine_txt == window.focus_get() and db_engine_txt.get() == db_engine_value:
			db_engine_txt.delete(0, END)

		if db_user_txt == window.focus_get() and db_user_txt.get() == db_user_value:
			db_user_txt.delete(0,END)

		if db_pass_txt == db_pass_txt.focus_get() and db_pass_txt.get() == db_pass_value:
			db_pass_txt.delete(0, END)
		
		if log_location_txt == window.focus_get() and log_location_txt.get() == log_location_value:
			log_location_txt.delete(0,END)
			
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
	lbl = Label(window,font=Font(family="Times New Roman", size=14), text="Please Enter The Following Values",bg='grey')
	lbl.place(x=50,y=0,width=620,height=30)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Application Base url",bg='grey')
	lbl.grid(column=0, row=2)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database url",bg='grey')
	lbl.grid(column=0, row=4)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database Username",bg='grey')
	lbl.grid(column=0, row=6)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Database Password",bg='grey')
	lbl.grid(column=0, row=8)
	lbl = Label(window,font=Font(family="Times New Roman", size=12), text="Log File Location",bg='grey')
	lbl.grid(column=0, row=10)
	
	rmts_url_txt = Entry(window,width=60)
	rmts_url_txt.insert(0, rmts_url_value)
	rmts_url_txt.bind("<FocusIn>", clear_widget)
	rmts_url_txt.bind('<FocusOut>', repopulate_defaults)
	rmts_url_txt.grid(row=2, column=2, sticky='NS')
	
	db_engine_txt = Entry(window,width=60)
	db_engine_txt.insert(0, db_engine_value)
	db_engine_txt.bind("<FocusIn>", clear_widget)
	db_engine_txt.bind('<FocusOut>', repopulate_defaults)
	db_engine_txt.grid(row=4, column=2, sticky='NS')
	
	db_user_txt = Entry(window,width=60)
	db_user_txt.insert(0, db_user_value)
	db_user_txt.bind("<FocusIn>", clear_widget)
	db_user_txt.bind('<FocusOut>', repopulate_defaults)
	db_user_txt.grid(row=6, column=2, sticky='NS')
	
	db_pass_txt = Entry(window,show='*',width=60)
	db_pass_txt.insert(0, db_pass_value)
	db_pass_txt.bind("<FocusIn>", clear_widget)
	db_pass_txt.bind('<FocusOut>', repopulate_defaults)
	db_pass_txt.grid(row=8, column=2, sticky='NS')
	
	log_location_txt = Entry(window,width=60)
	log_location_txt.insert(0, log_location_value)
	log_location_txt.bind("<FocusIn>", clear_widget)
	log_location_txt.bind('<FocusOut>', repopulate_defaults)
	log_location_txt.grid(row=10, column=2, sticky='NS')
	
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
		
		result=tkMessageBox.askyesno("REXS Installation","Would you like to save the data and Countinue?")
#		tkMessageBox.destroy()
		if result == True:
			data=db_engine.split(":")
			if data[0] == 'mysql' or data[0] == 'sqlserver':
				tkMessageBox.showinfo("REXS Installation", "Your are DB Engine is "+data[0])
				window.destroy()
				return rmts_url, db_engine, db_user, db_pass, log_location, data[0]
			else:
				tkMessageBox.showwarning("REXS Installation", "The RDS_Db_End_Point should start mysql or sqlserver")
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
	btn.grid(column=0, row=13)
	btn.place(x=450,y=420,width=80,height=30)
	btn = Button(window, bg='grey',text="Cancel", command=submitted)
	btn.place(x=250,y=420,width=80,height=30)
#	btn.grid(column=1, row=13)
#	btn.place(x=500,y=500, width=40,height=30)

def pre_requist():
	cwd=os.getcwd()
	window.geometry('600x300')
	dirlist = os.listdir(cwd)
	old_label_image = None
	for f in dirlist:
		if re.search("motive-logo-transparent.png", f):
			image1 = Image.open(f)
			window.geometry('530x300')
#			window.configure(background='blue')
			tkpi = ImageTk.PhotoImage(image1)
			label_image = Tkinter.Label(window, image=tkpi, bg='grey')
			label_image.grid(column=0,row=0)
			label_image.place(x=-10,y=0,width=600,height=300)
			window.title('Pre Requeste Checking Page')
			window.resizable(0,0)
			if old_label_image is not None:
				old_label_image.destroy()
			old_label_image = label_image
			def check():
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
				java_service=output.split('=')[0]
				
				if tomcat_service == '':
					tkMessageBox.showwarning("Pre Request Not satisfied", "Tomcat is not installed on your machine")
					window.destroy()
				if java_service == '':
					tkMessageBox.showwarning("Pre Request Not satisfied", "Java is not installed on your machine")
					window.destroy()
				if tmcat_home == '':
					tkMessageBox.showwarning("Pre Request Not satisfied", "Set CATALINA_HOME on your machine")
					window.destroy()
				if java_home=='':
					tkMessageBox.showwarning("Pre Request Not satisfied", "Set JAVA_HOME on your machine")
				tkMessageBox.showinfo("Pre Request are satisfied","Java and Tomcat are installed in this Machine")
				window.destroy()
				ui_page()
			btn = Button(window, bg='grey', text="Pre Requests Check", command=check)
			btn.place(x=60,y=250,width=400,height=40)
			window.mainloop()

pre_requist()
#window.destroy()

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
with open ('temp_token.txt', 'a+') as dup_token:
	dup_token.write('RMTS_BASE_URL==>https://'+rmts_url+'/rmts/api\n')
	dup_token.write('RMTS_LOG4J_FILE==>'+log_location+'\\\\rmts.log''\n')
	dup_token.write('RULE-EXECUTOR_LOG4J_FILE==>'+log_location+'\\\\rule-executor.log''\n')
	dup_token.write('RULE-EXECUTOR_SECURE_FLAG==>false''\n')
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
	#move orignal file to backup and move to untokenize
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
#				os.system("flyway.cmd -configFile=conf\\sql_server\\" + db + ".conf migrate >>conf\\sql_server\\"+db+".log")
				os.system("flyway.cmd -configFile=conf\\sql_server\\" + db + ".conf migrate")
		os.chdir( work_space )
	elif db_type =="mysql":
		os.chdir( work_space+"\\flyway")
		cwd=os.getcwd()
		for db in config_db_names:
			if os.path.exists("conf\\"+db+".conf") == True:
				if flyway_update(cwd+'\\conf\\'+db+'.conf') != None:
					copy_token_file()
#				os.system("flyway.cmd -configFile=conf\\" + db + ".conf migrate>>conf\\"+db+".log")
				os.system("flyway.cmd -configFile=conf\\" + db + ".conf migrate")
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
	
	config_artifacts=yaml_config_doc['artifacts']
	config_db_names=yaml_config_doc['db_names']
	work_space=cwd
	cat_home=tmcat_home
	db_type=data[0]
	tomcat_home=tomcat_service
	
	print 'CAT_HOME='+cat_home
	print 'WORKSPACE='+work_space
	print 'DB_TYPE='+db_type
	print config_artifacts
	print config_db_names
	
	if work_space==None or cat_home==None or db_type==None or config_artifacts==None or tomcat_home==None or config_db_names==None:
		print "\nFill All field in the YAML config file All Fields should get value"
		exit()
	return 0

def tomcat_control(action):
	if action == 'stop':
		if win32serviceutil.QueryServiceStatus(tomcat_home)[1] == 4:
			win32serviceutil.StopService(tomcat_home)
			print "\nTomcat is Stopped"
		else:
			print "\nTomcat Already Stopped"
	else:
		if win32serviceutil.QueryServiceStatus(tomcat_home)[1] != 4:
			win32serviceutil.StartService(tomcat_home)
			print "\nPlease wait for 30 seconds " +tomcat_home+ " is loading..."
			time.sleep(30)	
			
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
	zip_ref = zipfile.ZipFile(workspace+'\\bundle.zip', 'r')
	zip_ref.extractall(workspace)
	for artifacts_item in config_artifacts:
		print "\n deploying %s ..." % artifacts_item
		tempdir="%s_temp" % artifacts_item
		if not os.path.exists(tempdir):
			os.makedirs(tempdir)
		os.chdir(tempdir)
		os.system('jar xf ' + workspace + '\\'+artifacts_item + '.war')
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
		os.system('jar cf ' + workspace + '\\'+artifacts_item + '.war  *' )
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
		print '\Error:::'+str(e)
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

def main():

	os.system('cls')
	print '\nTaking Backup for tokens file'
	shutil.copyfile(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone', cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1")
	
	try:
		decrypt_call()
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
	except (IOError,pywintypes.error,WindowsError) as e:
		print '\n'+tomcat_home+' is not available in this machine please update correct version in the config.yaml file'
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
	except (IOError,pywintypes.error,WindowsError) as e:
		print '\nThe removing files are not in the location.'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	
	try:
		tomcat_control('start')
	except (IOError,pywintypes.error,WindowsError) as e:
		print '\nProblem In starting the'+ tomcat_home +'service'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	
	os.chdir(work_space)
	if os.path.exists(cwd+'\\tokens\\tokens_rexs-win-sqlserver_standalone'+"1")==True:
		copy_token_file()
	copy_flyway_conf_to_original()
	delete_conf_files()
if __name__=="__main__":
	main()
