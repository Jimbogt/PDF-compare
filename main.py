import sys
import os, os.path
from PIL import Image, ImageDraw, ImageChops


from pdf2image import convert_from_path
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
 
# Browse for an input folder 1 destination & store directory as input_dir_1
def browse_input_1():
    filename = filedialog.askdirectory()
    input_dir_1.set(filename)
    
    # Debugging
    print(filename) 
    
# Browse for an input folder 2 destination & store directory as input_dir_2
def browse_input_2():
    filename = filedialog.askdirectory()
    input_dir_2.set(filename)
    
    # Debugging
    print(filename) 
 
# Browse for an output destination & store directory as dest_dir
def browse_input_3():
    filename = filedialog.askdirectory()
    output_dir.set(filename)
    
    # Debugging
    print(filename) 

# Compares all PDFs in input folders against each other by first converting all
# to PIL images. Outputs results as images in selected directory.
def pdf2img():
    try:
        
        # Debugging
        input_dir_1.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test/Current Set")
        input_dir_2.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test/Markups")
        output_dir.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test")
        
        # Ensure all directories are specified first by user
        if len(input_dir_1.get()) == 0 or input_dir_2 == "" or output_dir == "":
            Result = "Please select input/output folder locations."
            messagebox.showinfo("Error", Result)
            return
        # Ensure input directories are different
        elif input_dir_1.get() == input_dir_2.get():
            Result = "Please select two different input folders."
            messagebox.showinfo("Error", Result)
            return
        
        # Debugging
        print(os.listdir(input_dir_1.get()))
        print(os.listdir(input_dir_2.get()))
        
        input_files_1 = list()
        input_files_2 = list()
        
        # Compile list of file directories in first input folder
        for file in os.listdir(input_dir_1.get()):
            if os.path.isfile(os.path.join(input_dir_1.get(), file)):
                input_files_1.append(os.path.join(input_dir_1.get(), file).replace("\\","/"))
                
        # Compile list of file directories in second input folder
        for file in os.listdir(input_dir_2.get()):
            if os.path.isfile(os.path.join(input_dir_2.get(), file)):
                input_files_2.append(os.path.join(input_dir_2.get(), file).replace("\\","/"))
         
        # debugging        
        #print(input_files_2)
        
        #images = convert_from_path(str(e1.get()))
        #for img in images:
        #    img.save('new_folder\output.jpg', 'JPEG')
 
    except:
        Result = "NO pdf found"
        messagebox.showinfo("Result", Result)
 
    else:
       Result = "PDF Comparison Complete."
       messagebox.showinfo("Success!", Result)
 
 
# Initialise GUI
master = Tk()

# Global variables for storing directories of input files
input_dir_1 = StringVar()
input_dir_2 = StringVar()
# Output path
output_dir = StringVar()

Label(master, text="Input Folder 1 Location:").grid(row=0, sticky=W) 
Label(master, text="Input Folder 2 Location:").grid(row=1, sticky=W) 
Label(master, text="Output Folder Location:").grid(row=2, sticky=W) 

# Dynamic labels updated when directories are selected
lbl1 = Label(master,textvariable=input_dir_1)
lbl1.grid(row=0, column=1)
lbl2 = Label(master,textvariable=input_dir_2)
lbl2.grid(row=1, column=1)
lbl3 = Label(master,textvariable=output_dir)
lbl3.grid(row=2, column=1)
 
# Entry fields
#e1 = Entry(master)
#e1.grid(row=0, column=1)
#e2 = Entry(master)
#e2.grid(row=1, column=1)
#e3 = Entry(master)
#e3.grid(row=2, column=1)
 
# Buttons for selecting input/output directories
b1 = Button(master, text="Browse", command=browse_input_1)
b1.grid(row=0, column=2, padx=5, pady=5)
b2 = Button(master, text="Browse", command=browse_input_2)
b2.grid(row=1, column=2, padx=5, pady=5)
b3 = Button(master, text="Browse", command=browse_input_3)
b3.grid(row=2, column=2, padx=5, pady=5)

# Button to run tool
b3 = Button(master, text="Compare PDFs", command=pdf2img)
b3.grid(row=3, column=0,columnspan=3, rowspan=2,padx=5, pady=5)
  
mainloop()