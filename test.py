import tkinter
from tkinter import ttk


def modify_label_text(event):
    newvalue = entry.get()
    clickme.configure(text=newvalue)
    entry.pack_forget()
    clickme.focus()


def create_entry(event):
    label = event.widget
    entry.pack()
    entry.focus()


root = tkinter.Tk()

newvalue = tkinter.StringVar()

clickme = ttk.Label(root, width=16)
clickme.pack()

clickme.bind("<Button-1>", create_entry)
clickme.focus()

entry = ttk.Entry(clickme, textvariable=newvalue)
entry.bind("<Return>", modify_label_text)

root.mainloop()

# https://gist.github.com/SilasPDJ/8b080881ebc63bc9c6375e1768e54eae
# pyinstaller
