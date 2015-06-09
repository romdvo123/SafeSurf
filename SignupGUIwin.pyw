from Tkinter import *
from ttk import *
import tkMessageBox
import SignupBase
class GUI(Frame):
    def __init__(self, parent,client):
        failed = False
        try:
            self.connected = client.connected
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

    def initStyle(self):
        self.style = Style()
        self.style.theme_use('xpnative')
        self.style.configure('BG.TFrame',foreground='black',background='lightblue')
        self.style.configure('SIGNUP.TLabel',foreground='black',relief=RAISED)
        self.style.configure('O.TLabel',foreground='black',background='lightblue',
                             anchor=CENTER,wraplength=300,justify=CENTER,relief=GROOVE)
        
    def initUI(self):
        Frame.__init__(self,self.parent,style = 'BG.TFrame')
        self.center(325,210)
        self.pack(fill=BOTH, expand=1)
        self.signup_menu()
        
    def center(self,width,height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width-width)/2
        y = (screen_height-height)/2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))
        
    def signup_menu(self):
        self.text_label=Label(self,font=("Arial", 12),
                              text="Signup below",
                              style='O.TLabel')
        self.text_label.place(relx=0.3,relwidth=0.4,relheight = 0.2,rely=0.05)
        offset = 0.003
        self.username = StringVar()
        self.password = StringVar()
        self.confirm = StringVar()
        self.user_label = Label(self,text="Username: ",
                                font=("Arial", 12),style='SIGNUP.TLabel')
        self.user_label.place(rely=0.3+offset,relx=0.15,relwidth=0.265)
        self.pass_label = Label(self,text="Password:  ",
                                font=("Arial", 12),style='SIGNUP.TLabel')
        self.pass_label.place(rely=0.45+offset,relx=0.15)
        self.confirm_label = Label(self,text="Confirm:  ",
                                font=("Arial", 12),style='SIGNUP.TLabel')
        self.confirm_label.place(rely=0.6+offset,relx=0.15,relwidth=0.265)
        self.user_entry = Entry(self,textvariable=self.username)
        self.user_entry.place(rely=0.3,relx=0.415)
        self.pass_entry = Entry(self,show="*",textvariable=self.password)
        self.pass_entry.place(rely=0.45,relx=0.415)
        self.confirm_entry = Entry(self,show="*",textvariable=self.confirm)
        self.confirm_entry.place(rely=0.6,relx=0.415)
        self.signup_button = Button(self,text="Signup",
                                 command=lambda: self.do_signup())
        self.signup_button.place(rely=0.8,relx=0.38)
        self.user_entry.focus_set()

    def do_signup(self):
        success = self.client.signup(self.username.get(),
                                     self.password.get(),self.confirm.get())
        if success == 'CHAR':
            tkMessageBox.showwarning("Banned Character",
                                     "Usernames and passwords can't contain ;")
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
            self.user_entry.focus_set()
        elif success == 'NO MATCH':
            tkMessageBox.showwarning("Confirm Password",
                                     "Passwords don't match")
            self.confirm_entry.delete(0, 'end')
            self.confirm_entry.focus_set()
        elif success == 'ERROR':
            tkMessageBox.showerror("Error",
                                     "Error occured, please restart the program")
            self.parent.destroy()
        elif success == 'USERNAME':
            tkMessageBox.showwarning("Username Taken",
                                     "Username already in use, please try a different username")
            self.user_entry.delete(0, 'end')
            self.pass_entry.delete(0, 'end')
            self.confirm_entry.delete(0, 'end')
            self.user_entry.focus_set()
        elif success == 'REGISTERED':
            tkMessageBox.showwarning("Computer Registered",
                                     "Computer is already registered. Closing connection")
            self.parent.destroy()
        elif success == 'SUCCESS':
            tkMessageBox.showinfo("Success","Signup successful! Closing connection")
            self.parent.destroy()

            
def main():
    client = SignupBase.Client()
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    app = GUI(root,client)
    root.mainloop()

if __name__ == '__main__':
    main()  
