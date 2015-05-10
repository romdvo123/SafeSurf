from Tkinter import Tk, BOTH
from ttk import Frame, Button, Style

class GUI(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.parent.title("SafeSurf")
        self.geometry(500,500)
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.button("QUIT")
    def button(self,name):
        quitButton = Button(self, text="Quit",command=self.quit)
        quitButton.place(x=100, y=100)
    def geometry(self,width,height):
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width-width)/2
        y = (screen_height-height)/2
        self.parent.geometry('%dx%d+%d+%d' % (width, height, x, y))
        

def main():
  
    root = Tk()
    app = GUI(root)
    root.mainloop()  


if __name__ == '__main__':
    main()  
