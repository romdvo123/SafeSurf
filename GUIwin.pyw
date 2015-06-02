from Tkinter import *
from ttk import *
import tkMessageBox
import time, ClientBase
from tkFileDialog import askdirectory
class GUI(Frame):
  
    def __init__(self, parent,client):
        failed = False
        try:
            self.blacklists = client.blacklists
        except:
            if tkMessageBox.showerror("Connection Error",
                                   "Could not connect to server"):
                parent.destroy()
            failed = True
        if not failed:
            self.client = client
            self.parent = parent
            self.parent.title("SafeSurf")
            self.initStyle()
            self.initUI()
        
    def initUI(self):
        Frame.__init__(self,self.parent,style = 'BG.TFrame')
        self.center(500,300)
        self.pack(fill=BOTH, expand=1)
        self.buttons_menu()
        self.output_menu()
        self.input_menu()

    def center(self,width,height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width-width)/2
        y = (screen_height-height)/2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def buttons_menu(self):
        buttons_frame = Frame(self,style = 'BTN.TFrame')
        buttons_frame.place(relheight=1,relx=0,rely=0,relwidth=0.35)
        self.GET_button = Button(buttons_frame,text="Get report",
                                 command=lambda: self.callback('GET'),
                                 state=DISABLED)
        self.GET_button.pack(side=TOP,fill=X,padx=10,pady=10)
        self.ADD_button = Button(buttons_frame,text="Add block parameter",
                                 command=lambda: self.callback('ADD'),
                                 state=DISABLED)
        self.ADD_button.pack(side=TOP,fill=X,padx=10,pady=10)
        self.REMOVE_button = Button(buttons_frame,text="Remove block parameter",
                                    command=lambda: self.callback('REMOVE'),
                                    state=DISABLED)
        self.REMOVE_button.pack(side=TOP,fill=X,padx=10,pady=10)
        self.logo_label = Label(buttons_frame,text="""Safe\nSurf""",
                                font=("Arial", 30),style='BTNLOGO.TLabel')
        self.logo_label.pack(side=TOP,fill=BOTH,expand=1,padx=10,pady=10)

    def output_menu(self):
        self.text_label=Label(self,font=("Arial", 12),
                         text="Enter username and password.",
                         style='O.TLabel')
        self.text_label.place(relx=0.35,relwidth=0.65,relheight = 0.3)
    def input_menu(self):
        self.active_widgets = []
        self.input_frame = Frame(self,style='I.TFrame')     
        self.input_frame.place(relheight=0.7,relx=0.35,rely=0.3,relwidth=0.65)
        input_directory = Menubutton(self.input_frame,style='I.TMenubutton',text="Choose directory:")
        #input_directory.place(rely=0.1,relx=0.3)
        self.input_blacklist=Menubutton(self.input_frame,style='I.TMenubutton',text="Choose blacklist:")
        self.blacklist_menu = Menu(self.input_blacklist,tearoff=0)
        self.input_blacklist['menu'] = self.blacklist_menu
        self.option_blacklist = IntVar()
        counter = 0
        for blacklist in self.blacklists:
            #command=lambda:self.blacklist_command(self.blacklists.index(blacklist)
            #!!!!change to radio button
            self.blacklist_menu.add_radiobutton( label=blacklist[0],variable=self.option_blacklist,
                                                 value=counter,command=self.blacklist_command)
            counter+=1
        self.input_subblacklist=Menubutton(self.input_frame,style='I.TMenubutton',text="Choose sub-blacklist:")
        self.subblacklist_menu = Menu(self.input_subblacklist,tearoff=0)
        self.input_subblacklist['menu'] = self.subblacklist_menu
        #input_blacklist.place(rely=0.1,relx=0.1)
        #input_subblacklist.place(rely=0.1,relx=0.5)
        self.input = StringVar()
        self.input_entry = Entry(self.input_frame,textvariable=self.input)
        #input_entry.place(rely=0.8,relx=0.3)
        self.username = StringVar()
        self.password = StringVar()
        self.user_label = Label(self.input_frame,text="Username: ",font=("Arial", 12),style='LOGIN.TLabel')
        self.user_label.place(rely=0.2,relx=0.15,relwidth=0.265)
        self.user_entry = Entry(self.input_frame,textvariable=self.username)
        self.user_entry.place(rely=0.2,relx=0.415)
        self.pass_label = Label(self.input_frame,text="Password:  ",font=("Arial", 12),style='LOGIN.TLabel')
        self.pass_label.place(rely=0.4,relx=0.15)
        self.pass_entry = Entry(self.input_frame, show="*",textvariable=self.password)
        self.pass_entry.place(rely=0.4,relx=0.415)
        self.login_button = Button(self.input_frame,text="Login",
                                   command=lambda: self.callback('LOGIN'))
        self.login_button.place(rely=0.6,relx=0.35)
        self.date_label = Label(self.input_frame,text="Date(day-month-year): ",style='LOGIN.TLabel')
        self.date_button = Button(self.input_frame,text="Enter",
                                   command=lambda: self.callback('DATE'))
        self.parameter_label = Label(self.input_frame,text="Parameter: ",style='LOGIN.TLabel')
        self.blacklists_label = Label(self.input_frame,style='LOGIN.TLabel')
        self.subblacklists_label = Label(self.input_frame,style='LOGIN.TLabel')
        self.blacklists_button = Button(self.input_frame,text="Enter",
                                   command=lambda: self.callback('EDIT'))
        self.user_entry.focus_set()
        self.got_directory = False
        self.active_widgets += [self.user_label,self.user_entry,self.pass_label,self.pass_entry,self.login_button]
                                
    def initStyle(self):
        self.style = Style()
        self.style.theme_use('xpnative')
        self.style.configure('BG.TFrame',foreground='black',background='green')
        self.style.configure('BTN.TFrame',foreground='black',background='blue')
        self.style.configure('I.TFrame',foreground='black',background='lightblue',bd=10,relief=GROOVE)
        self.style.configure('BTNLOGO.TLabel',foreground='lightblue',background='blue',anchor=CENTER)
        self.style.configure('O.TLabel',foreground='black',background='lightblue',
                             anchor=CENTER,wraplength=300,justify=CENTER,relief=GROOVE)
        self.style.configure('I.TMenubutton',foreground='black',padding=10,relief=GROOVE)
        self.style.configure('LOGIN.TLabel',foreground='black',relief=RAISED)
                         
    def callback(self,method):
        if method == 'GET':
            for widget in self.active_widgets:
                widget.place_forget()
            self.active_widgets = []
            self.GET()
        elif method == 'ADD':
            for widget in self.active_widgets:
                widget.place_forget()
            self.active_widgets = []
            self.change_parameters('ADD')
        elif method == 'REMOVE':
            for widget in self.active_widgets:
                widget.place_forget()
            self.active_widgets = []
            self.change_parameters('REMOVE')
        elif method == 'LOGIN':
            success = self.client.login(self.username.get(),self.password.get())
            if success == 'OK':
                self.GET_button['state'] = NORMAL
                self.ADD_button['state'] = NORMAL
                self.REMOVE_button['state'] = NORMAL
                '''self.login_button.place_forget()
                self.pass_entry.place_forget()
                self.pass_label.place_forget()
                self.user_entry.place_forget()
                self.user_label.place_forget()'''
                for widget in self.active_widgets:
                    widget.place_forget()
                self.active_widgets = []
                self.text_label['text'] = "Choose a method from the left"
            elif success == 'CLOSE':
                if tkMessageBox.showwarning("Login Failed",
                                         "Exceeded login tries limit, closing connection"):
                    self.parent.destroy()    
                
            else:
                tkMessageBox.showwarning("Login Failed",
                                       success)
                self.user_entry.delete(0, 'end')
                self.pass_entry.delete(0, 'end')
                self.user_entry.focus_set()
        elif method == 'DATE':
            date = self.input.get()
            success = self.client.method_GET(date)
            if success == 'NOT FOUND':
                tkMessageBox.showwarning("Not Found","Could not find report from the date %s"%date)
                self.GET()
            elif success == 'SYNTAX':
                tkMessageBox.showerror("Syntax Error","Syntax error in date, type a new date(day-month-year)")
                self.input_entry.delete(0, 'end')
                self.GET()
            else:
                tkMessageBox.showinfo("Success",success)
        elif method == 'EDIT':
            parameter = self.input.get()
            if self.method == 'ADD':
                success = self.client.method_ADD(self.blacklist[0],self.subblacklist,parameter)
                tkMessageBox.showinfo("Success",success)
            elif self.method == 'REMOVE':
                success = self.client.method_REMOVE(self.blacklist[0],self.subblacklist,parameter)
                tkMessageBox.showinfo("Success",success)


    def change_parameters(self,method):
        self.method = method
        if method == 'ADD':
            #self.text_label['text'] = "Choose blacklist and sub-blacklist to add to, then enter the parameter you wish to add."
            self.text_label['text'] = "Choose blacklist to add to"
        elif method == 'REMOVE':
            #self.text_label['text'] = "Choose blacklist and sub-blacklist to remove from, then enter the parameter you wish to remove."
            self.text_label['text'] = "Choose blacklist to remove from"
        self.input_blacklist.place(rely=0.2,relx=0.1)        
        #self.input_subblacklist.place(rely=0.1,relx=0.5)
        self.active_widgets += [self.input_blacklist]

    def GET(self):
        if not self.got_directory:
            self.text_label['text'] = "Choose directory to save report"
            path = askdirectory(parent=self.input_frame,title="Choose directory to save report: ",mustexist=1)
            path = path.replace('/','\\')
            self.client.directory(path)
            self.got_directory = True
        self.text_label['text'] = "Type the date of the report you wish to get(day-month-year)"
        self.date_label.place(rely=0.4,relx=0.1,height=20)
        self.input_entry.place(rely=0.39,relx=0.4957)
        self.input_entry.focus_set()
        self.date_button.place(rely=0.6,relx=0.35)
        self.active_widgets += [self.date_label,self.input_entry,self.date_button]

    def blacklist_command(self):
        self.text_label['text'] = "Choose subblacklist"
        self.subblacklist_menu.delete(0, 'end')
        self.option_subblacklist = IntVar()
        self.blacklist = self.blacklists[self.option_blacklist.get()]
        self.blacklists_label['text'] = self.blacklist[0]
        self.blacklists_label.place(rely=0.1,relx=0.1,height=20,width=114)
        counter = 1
        for subblacklist in self.blacklist[1:]:
            self.subblacklist_menu.add_radiobutton(label=subblacklist,value=counter,variable=self.option_subblacklist,
                                                   command=self.subblacklist_command)
            counter+=1
        self.input_subblacklist.place(rely=0.2,relx=0.5)
        self.active_widgets += [self.input_subblacklist,self.blacklists_label]

    def subblacklist_command(self):
        if self.method == 'ADD':
            self.text_label['text'] = "Type in the parameter you wish to add"
        elif self.method == 'REMOVE':
            self.text_label['text'] = "Type in the parameter you wish to remove"
        self.parameter_label.place(rely=0.6,relx=0.2,height=20)
        self.input_entry.place(rely=0.59,relx=0.3957)
        self.subblacklist = self.blacklist[self.option_subblacklist.get()]
        self.subblacklists_label['text'] = self.subblacklist
        self.subblacklists_label.place(rely=0.1,relx=0.5,height=20,width=137)
        self.blacklists_button.place(rely=0.8,relx=0.4)
        self.active_widgets += [self.parameter_label,self.input_entry,self.subblacklists_label,self.blacklists_button]
        
def main():
    client = ClientBase.Client()
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    app = GUI(root,client)
    root.mainloop()  

if __name__ == "__main__":
    main()  
