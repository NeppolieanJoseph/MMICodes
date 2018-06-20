###################################################################################################################
# File Name        : deploy_win_standalone.py
# Author           : Neppoliean.Joseph
# Modified Date    : 29-Mar-2018
# Modified Date    : 19-Jun-2018
# Reviewer         : Me
# Description      : This script has designed to deploy statndalone_importer and exporter artifact foiles to windows tomcat webserver 
# Notes            : This script has designed to extract the bundle.zip file and collect the war files inside that it make untokenize some token files and then deploy in to the windows tomcat server.
# Parameter(s)     : This script accept two arguments one is bundle.zip file it have the war files second one is Input token file contains host details and ELB url details.
##################################################################################################################

import yaml
import zipfile
import os, sys
import win32serviceutil
import subprocess
import shutil, re, time
from subprocess import Popen, PIPE, STDOUT
import pywintypes

#if not os.path.exists("C:\\Logs\\Deployment"):#
#		os.makedirs("C:\\Logs\\Deployment")	
#sys.stdout = open("C:\\Logs\\Deployment\\deploy_script.log", 'w+')
#os.system('xdg-open C:\\Logs\\Deployment\\deploy_script.log')


def flyway_update(tokenfile):
	key=None
	value=None
	token_file=sys.argv[2]+'1'
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
	with open(sys.argv[2]) as token_f:
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
	shutil.move('temp_token.txt', sys.argv[2] )
	token_f.close()

def untokenize(tokenfile):
	line=None
	key=None
	value=None
	token_file=sys.argv[2]
	print sys.argv[2]
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
	if db_type == "sql_server":
		os.chdir( work_space+"\\flyway")
		cwd=os.getcwd()
		for db in config_db_names:
			if os.path.exists("conf\\sql_server\\"+db+".conf") == True:
				if flyway_update(cwd+'\\conf\\sql_server\\'+db+'.conf') != None:
					copy_token_file()
				os.system("flyway.cmd -configFile=conf\\sql_server\\" + db + ".conf migrate")
		os.chdir( work_space )
	elif db_type =="Mysql":
		os.chdir( work_space+"\\flyway")
		cwd=os.getcwd()
		for db in config_db_names:
			if os.path.exists("conf\\"+db+".conf") == True:
				if flyway_update(cwd+'\\conf\\'+db+'.conf') != None:
					copy_token_file()
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
	
	with open("config.yaml", 'r') as stream:
		try:
			yaml_config_doc = yaml.load(stream)
		except yaml.YAMLError as exc:
			print(exc)
	
	work_space=yaml_config_doc['workspace']
	cat_home=yaml_config_doc['cathome']
	tomcat_home=yaml_config_doc['tomcat_server']
	db_type=yaml_config_doc['dbserver']
	config_artifacts=yaml_config_doc['artifacts']
	config_db_names=yaml_config_doc['db_names']
	
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
	os.chdir(cat_home +'\\webapps')
	if os.path.exists(cat_home +'\\'+arfifact)==True:
		shutil.rmtree(arfifact, ignore_errors=True)
	if os.path.exists(cat_home +'\\'+arfifact+'.war')==True:
		shutil.rmtree(arfifact +'.war', ignore_errors=True)
	shutil.copyfile(work_space+'\\'+arfifact+'.war', cat_home +'\\webapps' + '\\' + arfifact + '.war')
			
			
def un_zip(workspace, cathome):
	try:
		os.chdir(workspace)
	except (KeyboardInterrupt,IOError,pywintypes.error,WindowsError) as e:
		print str(e)
	zip_ref = zipfile.ZipFile(workspace+'\\'+sys.argv[1], 'r')
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
		try:
			print 
			deploy_war(artifacts_item)
		except (KeyboardInterrupt,IOError,pywintypes.error,WindowsError) as e:
			print str(e)
			copy_token_file()
			delete_unwanted_in_workspace()
			exit()
			
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
		os.chdir(cat_home+"\\webapps")
		if os.path.exists(filename)==True:
			shutil.rmtree(filename, ignore_errors=True)
	for f in os.listdir(cat_home+"\\webapps"):
		os.chdir(cat_home+"\\webapps")
		if re.search("_temp", f):
			shutil.rmtree(f, ignore_errors=True)
	for f in os.listdir(work_space):
		os.chdir(work_space)
		if re.search(".war", f):
			os.remove(f)

def copy_token_file():
	shutil.copyfile(sys.argv[2]+"1", sys.argv[2])
	os.remove(sys.argv[2]+"1")

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
		if db_type == "sql_server":
			shutil.move(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1', work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf')
		if db_type == "Mysql":
			shutil.move(work_space+'\\flyway\\conf\\'+i+'.conf1', work_space+'\\flyway\\conf\\'+i+'.conf')

def flyway_conf_duplicate():
	for i in config_db_names:
		if db_type == "sql_server":
			shutil.copyfile(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf', work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1')
		if db_type == "Mysql":
			shutil.copyfile(work_space+'\\flyway\\conf\\'+i+'.conf', work_space+'\\flyway\\conf\\'+i+'.conf1')

def delete_conf_files():
	for i in config_db_names:
		if db_type == "sql_server":
			os.remove(work_space+'\\flyway\\conf\\sql_server\\'+i+'.conf1')
		if db_type == "Mysql":
			os.remove(work_space+'\\flyway\\conf\\'+i+'.conf1')

def main():
	#Clear the screen for perfect output logs.
	os.system('cls')
	print '\nTaking Backup for tokens file'
	#Take a backup of Token "tokens_rexs-win-sqlserver_standalone" file
	shutil.copyfile(sys.argv[2], sys.argv[2]+"1")
	
	try:
		# Call the decrypt_call() function to Encrypt the username and password.
		decrypt_call()
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed 
		print '\n'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		#Handle the KeyboardInterrupt Exception.
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	try:
		# Call the read_config() function to to get the inputs from config.yaml file.
		read_config()
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed
		print '\nError in read the configuration file'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		#Handle the KeyboardInterrupt Exception.
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()

	try:
		# Call the tomcat_control() function to to stop the service for the deployments.
		tomcat_control('stop')
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed
		print '\n'+tomcat_home+' is not available in this machine please update correct version in the config.yaml file'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		#Handle the KeyboardInterrupt Exception.
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	
	try:
		# Call the read_config() function to to get the inputs from config.yaml file.
		un_zip( work_space, cat_home)
		
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed
		print '\n'+str(e)
		copy_token_file()
		remove_unwanted()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		#Handle the KeyboardInterrupt Exception.
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		remove_unwanted()
		delete_unwanted_in_workspace()
		exit()
	
	try:
		# Call the read_config() function to to get the inputs from config.yaml file.
		remove_unwanted()
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed
		print '\nThe removing files are not in the location.'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	
	try:
		# Call the read_config() function to to get the inputs from config.yaml file.
		tomcat_control('start')
	except (IOError,pywintypes.error,WindowsError) as e:
		#Handling the Exception If build failed
		print '\nProblem In starting the'+ tomcat_home +'service'
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	except (KeyboardInterrupt) as e:
		#Handle the KeyboardInterrupt Exception.
		print '\n The Deployment is stoped by keyboard Interrupt'+str(e)
		copy_token_file()
		delete_unwanted_in_workspace()
		exit()
	
	os.chdir(work_space)
	if os.path.exists(sys.argv[2]+"1")==True:
		copy_token_file()
	delete_conf_files()

if __name__=="__main__":
        main()
