from Tkinter import *
from ttk import *
import time, Client
class GUI(Frame):
  
    def __init__(self, parent,client):
        self.blacklists = client.blacklists
        self.parent = parent
        self.parent.title("SafeSurf")
        self.initStyle()
        self.themes = self.style.theme_names()
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
        input_frame = Frame(self,style='I.TFrame')
        input_frame.place(relheight=0.7,relx=0.35,rely=0.3,relwidth=0.65)
        input_directory = Menubutton(input_frame,style='I.TMenubutton',text="Choose directory:")
        #input_directory.place(rely=0.1,relx=0.3)
        self.input_blacklist=Menubutton(input_frame,style='I.TMenubutton',text="Choose blacklist:")
        self.blacklist_menu = Menu(self.input_blacklist,tearoff=0)
        self.input_blacklist['menu'] = self.blacklist_menu
        for blacklist in self.blacklists:
            self.blacklist_menu.add_command( label=blacklist[0])
        self.input_subblacklist=Menubutton(input_frame,style='I.TMenubutton',text="Choose sub-blacklist:")
        self.subblacklist_menu = Menu(self.input_subblacklist,tearoff=0)
        self.input_subblacklist['menu'] = self.subblacklist_menu
        #input_blacklist.place(rely=0.1,relx=0.1)
        #input_subblacklist.place(rely=0.1,relx=0.5)
        self.input_entry = Entry(input_frame)
        #input_entry.place(rely=0.8,relx=0.3)
        user_label = Label(input_frame,text="Username: ",font=("Arial", 12),style='LOGIN.TLabel')
        user_label.place(rely=0.2,relx=0.15,relwidth=0.265)
        self.user_entry = Entry(input_frame)
        self.user_entry.place(rely=0.2,relx=0.415)
        pass_label = Label(input_frame,text="Password:  ",font=("Arial", 12),style='LOGIN.TLabel')
        pass_label.place(rely=0.4,relx=0.15)
        self.pass_entry = Entry(input_frame, show="*")
        self.pass_entry.place(rely=0.4,relx=0.415)
        self.login_button = Button(input_frame,text="Login",
                                   command=lambda: self.callback('LOGIN'))
        self.login_button.place(rely=0.6,relx=0.35)
                                

    def initStyle(self):
        self.style = Style()
        self.style.theme_use('xpnative')
        self.style.configure('BG.TFrame',foreground='black',background='green')
        self.style.configure('BTN.TFrame',foreground='black',background='blue')
        self.style.configure('I.TFrame',foreground='black',background='lightblue',bd=10,relief=GROOVE)
        self.style.configure('BTNLOGO.TLabel',foreground='lightblue',background='blue',anchor=CENTER)
        self.style.configure('O.TLabel',foreground='black',background='lightblue',
                             anchor=CENTER,wraplength=300,justify=CENTER,relief=GROOVE)
        self.style.configure('I.TMenubutton',foreground='black',padding=10,relief=RAISED)
        self.style.configure('LOGIN.TLabel',foreground='black',relief=RAISED)
                         
    def callback(self,method):
        if method == 'GET':
            self.GET()
        elif method == 'ADD':
            self.change_parameters('ADD')
        elif method == 'REMOVE':
            self.change_parameters('REMOVE')
        elif method == 'LOGIN':
            pass

    def change_parameters(self,method):
        if method == 'ADD':
            #self.text_label['text'] = "Choose blacklist and sub-blacklist to add to, then enter the parameter you wish to add."
            self.text_label['text'] = "Choose blacklist to add to"
        elif method == 'REMOVE':
            #self.text_label['text'] = "Choose blacklist and sub-blacklist to remove from, then enter the parameter you wish to remove."
            self.text_label['text'] = "Choose blacklist to remove from"
        self.input_blacklist.place(rely=0.1,relx=0.1)        
        #self.input_subblacklist.place(rely=0.1,relx=0.5)   

def main(blacklists):
    client = Client()
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    app = GUI(root,blacklists,client)
    root.mainloop()  

if __name__ == "__main__":
    main((('list1','sub11','sub12'),
          ('list2','sub21','sub22','sub23')))  
