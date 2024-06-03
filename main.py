

from pdf2image import convert_from_path
from tkinter import Tk, filedialog, messagebox, StringVar, Label, Button, mainloop
from tkinter import *

import sys
import os, os.path
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter
import numpy as np
 
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
    
# Replaces a given colour in a PIL Image with another. Colours provided as RGB tuple
def img_colour_replace(img, orig_colour, replacement_colour):
    
    # Convert to RGB & load into np array
    img = img.convert('RGB')
    img_data = np.array(img)
    
    # Replace all instances of orig_colour to replacement_colour
    img_data[(img_data == orig_colour).all(axis = -1)] = replacement_colour
    
    # Return image as PIL Image
    return Image.fromarray(img_data, mode='RGB')

# Makes all white pixels in a provided PIL Image transparent.
def img_colour_replace_rgba(img, orig_colour, replacement_colour):
    
    # orig_colour = (255, 255, 255, 255)
    # replacement_colour = (255, 255, 255, 0)
    
    img = img.convert("RGBA")

    pixdata = img.load()

    # Iterate over all pixels and replace white with transparent
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == orig_colour:
                pixdata[x, y] = replacement_colour
                    
    return img

    # # Convert to RGBA & load into np array
    # img = img.convert('RGBA')
    # img_data = np.array(img)
    
    # # Replace all instances of orig_colour to replacement_colour
    # img_data[(img_data == (white_rgba)).all()] = transparent_rgba
    
    # # Return image as PIL Image
    # return Image.fromarray(img_data, mode='RGB')
    

# Compares all PDFs in input folders against each other by first converting all
# to PIL images. Outputs results as images in selected directory.
def compare_pdfs():
    
    ############################################################
    # Debugging
    input_dir_1.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test/Current Set")
    input_dir_2.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test/Markups")
    output_dir.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test")
    ############################################################
    
    
    # Ensure all directories are specified first by user
    if len(input_dir_1.get()) == 0 or len(input_dir_2.get()) == 0 or len(output_dir.get()) == 0:
        Result = "One or more folders haven't been selected. Please select input and output folder locations first."
        messagebox.showinfo("Error", Result)
        return
    # Ensure input directories are different
    elif input_dir_1.get() == input_dir_2.get():
        Result = "Please select two different input folders."
        messagebox.showinfo("Error", Result)
        return
    
    
    ############################################################
    # Debugging
    #print(os.listdir(input_dir_1.get()))
    #print(os.listdir(input_dir_2.get()))
    ############################################################
    

    # Compile list of file directories in first input folder
    input_files_1 = list()
    # Iterate through all files in input_dir_1
    for file in os.listdir(input_dir_1.get()):
        # Omits folders in input_dir_1
        if os.path.isfile(os.path.join(input_dir_1.get(), file)):
            dir_len = len(os.path.join(input_dir_1.get(), file).replace("\\","/"))
            # Only adds PDFs to input_files_1
            if os.path.join(input_dir_1.get(), file).replace("\\","/")[dir_len - 4:] == ".pdf":
                input_files_1.append(os.path.join(input_dir_1.get(), file).replace("\\","/"))
            
    # Compile list of file directories in second input folder
    input_files_2 = list()
    # Iterate through all files in input_dir_2
    for file in os.listdir(input_dir_2.get()):
        # Omits folders in input_dir_2
        if os.path.isfile(os.path.join(input_dir_2.get(), file)):
            dir_len = len(os.path.join(input_dir_2.get(), file).replace("\\","/"))
            # Only adds PDFs to input_files_2                
            if os.path.join(input_dir_2.get(), file).replace("\\","/")[dir_len - 4:] == ".pdf":
                input_files_2.append(os.path.join(input_dir_2.get(), file).replace("\\","/"))


    ############################################################
    # Debugging
    print(input_files_1)
    print(input_files_2)
    ############################################################
    
    
    # Check the number of files in each input folder matches
    if len(input_files_1) != len(input_files_2):
        Result = "Number of PDFs in each input folder doesn't match. Please check the contents of each folder."
        messagebox.showinfo("Error", Result)
        return
    
    num_pdf_pairs = len(input_files_1)
    for pdf_index in range(num_pdf_pairs): #debugging
        print(input_files_1[pdf_index])
        img_1 = convert_from_path(input_files_1[pdf_index])
        img_2 = convert_from_path(input_files_2[pdf_index])
        
        # Assumes each PDF is only one page long
        
        # Take absolute magnitude difference, pixel-by-pixel
        img_out_1 = ImageChops.difference(img_1[0], img_2[0])
        
        # Grayscale image & threshold.
        img_out_1 = ImageOps.grayscale(img_out_1)
        img_out_1 = img_out_1.point(lambda p: 255 if p > 5 else 0)
        img_out_2 = img_out_1

        # Convolve with 5x5 kernel to add 'halo' around detected changes
        # applying the Kernel filter 
        kernel = [0, 1, 2, 1, 0,
                  1, 2, 4, 2, 1,
                  2, 4, 8, 4, 1,
                  1, 2, 4, 2, 1,
                  0, 1, 2, 1, 0]
        img_out_1 = img_out_1.filter(ImageFilter.Kernel((5, 5), kernel, 1, 0))
        img_out_1 = img_out_1.filter(ImageFilter.Kernel((5, 5), kernel, 1, 0))

        # Colour replace: all white to cyan (yellow following uninversion)
        orig_colour = (255,255,255) # White
        replacement_colour = (0,0,255) # Cyan 
        img_out_1 = img_colour_replace(img_out_1, orig_colour, replacement_colour)
        
        # Uninvert image.
        img_out_1 = ImageOps.invert(img_out_1)
        
        # Make all white pixels transparent
        orig_colour = (255, 255, 255, 255) # White, 100% opacity
        replacement_colour = (255, 255, 255, 0) # White, 0% opacity 
        img_out_1 = img_colour_replace_rgba(img_out_1, orig_colour, replacement_colour)
        
        # Reduce opacity of yellow in halo effect
        orig_colour = (255, 255, 0, 255) # Yellow, 100% opacity
        replacement_colour = (255, 255, 0, 100) # Yellow, 38% opacity
        img_out_1 = img_colour_replace_rgba(img_out_1, orig_colour, replacement_colour)
        
        ############# img_out_2 processing (red text)
        img_out_2 = ImageOps.invert(img_out_2)
        
        # Colour replace: all black to red
        orig_colour = (0,0,0) # Black
        replacement_colour = (255,0,0) # Red
        img_out_2 = img_colour_replace(img_out_2, orig_colour, replacement_colour)
        
        orig_colour = (255, 255, 255, 255)
        replacement_colour = (255, 255, 255, 0)
        img_out_2 = img_colour_replace_rgba(img_out_2, orig_colour, replacement_colour)
        
        # Overlay image 1 and 2
        img_out_1.paste(img_out_2, (0,0), mask = img_out_2) 

        # Overlay output on original 
        img_1[0].paste(img_out_1, (0,0), mask = img_out_1) 
        
        # Useful funcs
        # PIL.Image.alpha_composite(im1: Image, im2: Image) → Image[source]
        # PIL.Image.composite(image1: Image, image2: Image, mask: Image)
        
        # Save image as e.g. "PDF 1.jpg"
        output_name = "PDF " + str(pdf_index + 1) + ".png"
        img_1[0].save(os.path.join(output_dir.get(), output_name).replace("\\","/"), 'PNG')
        
        # Save image maske as e.g. "PDF 1 Mask.jpg"
        output_name = "PDF " + str(pdf_index + 1) + " Mask.png"
        img_out_1.save(os.path.join(output_dir.get(), output_name).replace("\\","/"), 'PNG')
        
        
        
        #images = convert_from_path(str(e1.get()))
        #for img in images:
        #    img.save('new_folder\output.jpg', 'JPEG')
    
    try:
        
        print("test")

 
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
b3 = Button(master, text="Compare PDFs", command=compare_pdfs)
b3.grid(row=3, column=0,columnspan=3, rowspan=2,padx=5, pady=5)
  
mainloop()