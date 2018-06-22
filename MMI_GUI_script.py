from Tkinter import *
import tkMessageBox

window = Tk()

db_url_value=''
db_engine_value=''
db_user_value=''
db_pass_value=''

def ui_page():
	window.title("Welcome to MMI Installation Input Page")
	window.geometry('600x300')
	
	def clear_widget(event):
		if db_txt == window.focus_get() and db_txt.get() == db_url_value:
			db_txt.delete(0, END)
			
		if db_engine_txt == window.focus_get() and db_engine_txt.get() == db_engine_value:
			db_engine_txt.delete(0, END)

		if user_txt == window.focus_get() and user_txt.get() == db_user_value:
			user_txt.delete(0,END)

		if pass_txt == pass_txt.focus_get() and pass_txt.get() == db_pass_value:
			pass_txt.delete(0, END)
	
	def repopulate_defaults(event):
		if db_txt != window.focus_get() and db_txt.get() == '':
			db_txt.insert(0, db_url_value)
		
		if db_engine_txt != window.focus_get() and db_engine_txt.get() == '':
			db_engine_txt.insert(0, db_engine_value)

		if user_txt != window.focus_get() and user_txt.get() == '':
			user_txt.insert(0, db_user_value)

		if pass_txt != window.focus_get() and pass_txt.get()== '':
			pass_txt.insert(0,db_pass_value)
	
	rows = 0
	while rows < 10:
		window.rowconfigure(rows, weight=1)
		window.columnconfigure(rows, weight=1)
		rows += 1
	
	lbl = Label(window, text="Enter the DB_URL*")
	lbl.grid(column=0, row=0)
	lbl = Label(window, text="Enter DB_Engine(Mysql or sql_server)*")
	lbl.grid(column=0, row=1)
	lbl = Label(window, text="Enter the DB_UserName*")
	lbl.grid(column=0, row=2)
	lbl = Label(window, text="Enter the DB_Password*")
	lbl.grid(column=0, row=3)
	
	db_txt = Entry(window,width=50)
#	print 'Db_Txt:' +db_url_value
	db_txt.insert(0, db_url_value)
	db_txt.bind("<FocusIn>", clear_widget)
	db_txt.bind('<FocusOut>', repopulate_defaults)
	db_txt.grid(row=0, column=2, sticky='NS')
	
	db_engine_txt = Entry(window,width=50)
	db_engine_txt.insert(0, db_engine_value)
	db_engine_txt.bind("<FocusIn>", clear_widget)
	db_engine_txt.bind('<FocusOut>', repopulate_defaults)
	db_engine_txt.grid(row=1, column=2, sticky='NS')
	
	user_txt = Entry(window,width=50)
	user_txt.insert(0, db_user_value)
	user_txt.bind("<FocusIn>", clear_widget)
	user_txt.bind('<FocusOut>', repopulate_defaults)
	user_txt.grid(row=2, column=2, sticky='NS')
	
	pass_txt = Entry(window,show='*',width=50)
	pass_txt.insert(0, db_pass_value)
	pass_txt.bind("<FocusIn>", clear_widget)
	pass_txt.bind('<FocusOut>', repopulate_defaults)
	pass_txt.grid(row=3, column=2, sticky='NS')
	
	
	def login(*event):
		global db_url
		global db_engine
		global db_user
		global db_pass
		
		db_url=db_txt.get()
		db_engine=db_engine_txt.get()
		db_user=user_txt.get()
		db_pass=pass_txt.get()
		
		if db_url=='' or db_engine=='' or db_user=='' or db_pass=='':
			tkMessageBox.showwarning("REXS Installation", "All FIeld Should get Values")
			ui_page()
		else:
			print 'Db_URL: ' + db_url
			print 'Db_Engine:' + db_engine
			print 'User_Name: ' + db_user
			print 'Db_Pass:' + db_pass
#		window.destroy()
		
	def submitted():
		ui_page()
	btn = Button(window, text="Save", command=login)
	btn.grid(column=0, row=4)
	btn = Button(window, text="Cancel", command=submitted)
	btn.grid(column=1, row=4)
ui_page()
window.mainloop()
