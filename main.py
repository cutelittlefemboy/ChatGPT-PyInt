from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

class Main:
    is_running = True
    def loop(self):
        while Main.is_running:
            root.update()
    def stop(self):
        Main.is_running = False
        
main = Main()


ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=main.stop).grid(column=0, row=2)
ttk.Entry(frm, width=60).grid(column=0, row=1)


main.loop()