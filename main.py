import sys
from PIL import Image, ImageDraw, ImageChops


from pdf2image import convert_from_path
from tkinter import *
from tkinter import messagebox
 
 
def pdf2img():
    try:
        images = convert_from_path(str(e1.get()))
        for img in images:
            img.save('new_folder\output.jpg', 'JPEG')
 
    except  :
        Result = "NO pdf found"
        messagebox.showinfo("Result", Result)
 
    else:
        Result = "success"
        messagebox.showinfo("Result", Result)
 
 
 
master = Tk()
Label(master, text="Previous Revision Folder Location:").grid(row=0, sticky=W) 
Label(master, text="Current Revision Folder Location:").grid(row=1, sticky=W) 
 
e1 = Entry(master)
e1.grid(row=0, column=1)
e2 = Entry(master)
e2.grid(row=1, column=1)
 
b1 = Button(master, text="Convert", command=pdf2img)
b1.grid(row=0, column=2,columnspan=2, rowspan=2,padx=5, pady=5)
  
mainloop()