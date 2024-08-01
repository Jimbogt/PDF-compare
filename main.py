from pdf2image import convert_from_path
poppler_local = "C:/Users/AUJB508470/Documents/Projects/Python/Programs/poppler-24.02.0/Library/bin"
from tkinter import Tk, filedialog, messagebox, StringVar, Label, Button, mainloop
from tkinter import *

import sys
import os, os.path
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter
import numpy as np
 
# Browse for an input folder 1 destination & store directory as input_dir_1
def browse_input_dir_1():
    filename = filedialog.askdirectory()
    input_dir_1.set(filename)
    
# Browse for an input folder 2 destination & store directory as input_dir_2
def browse_input_dir_2():
    filename = filedialog.askdirectory()
    input_dir_2.set(filename)
 
# Browse for an output destination & store directory as dest_dir
def browse_input_dir_3():
    filename = filedialog.askdirectory()
    input_dir_3.set(filename)

# Browse for an output destination & store directory as dest_dir
def browse_output_dir():
    filename = filedialog.askdirectory()
    output_dir.set(filename)
    
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
    
    img = img.convert("RGBA")

    pixdata = img.load()

    # Iterate over all pixels and replace white with transparent
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == orig_colour:
                pixdata[x, y] = replacement_colour
                    
    return img
    
# Takes two PILLOW images and returns a coloured image of their differences 
def get_img_abs_diff(img1, img2):

    img_diff = ImageChops.difference(img1, img2)
    img_diff = ImageOps.invert(img_diff)
    img_diff = img_diff.convert("RGBA")

    # Make all white pixels transparent
    orig_colour = (255, 255, 255, 255)
    replacement_colour = (255, 255, 255, 0)
    img_diff = img_colour_replace_rgba(img_diff, orig_colour, replacement_colour)

    return img_diff

# Takes binary PILLOW image and creates yellow 'halo' around all positive (pixel val = 1)
# elements in the image. Opacity is value from 0 (transparent) to 255 (opaque).
def create_img_halo(img, opacity):
    # Convolve twice with 5x5 kernel to add 'halo' around detected changes
    # applying the Kernel filter 
    kernel = [0, 1, 2, 1, 0,
            1, 2, 4, 2, 1,
            2, 4, 8, 4, 1,
            1, 2, 4, 2, 1,
            0, 1, 2, 1, 0]
    img = img.filter(ImageFilter.Kernel((5, 5), kernel, 1, 0))
    img = img.filter(ImageFilter.Kernel((5, 5), kernel, 1, 0))

    # Colour replace: all white to cyan (yellow following uninversion)
    orig_colour = (255,255,255) # White
    replacement_colour = (0,0,255) # Cyan 
    img = img_colour_replace(img, orig_colour, replacement_colour)
    
    # Uninvert image.
    img = ImageOps.invert(img)
    
    # Make all white pixels transparent
    orig_colour = (255, 255, 255, 255) # White, 100% opacity
    replacement_colour = (255, 255, 255, 0) # White, 0% opacity 
    img = img_colour_replace_rgba(img, orig_colour, replacement_colour)
    
    # Reduce opacity of yellow in halo effect
    orig_colour = (255, 255, 0, 255) # Yellow, 100% opacity
    replacement_colour = (255, 255, 0, opacity) # Yellow, 38% opacity
    img = img_colour_replace_rgba(img, orig_colour, replacement_colour)

    return img

# Takes image and erases all pixels which aren't predominantly green
def extract_greenoffs(img):

    img = img.convert("RGBA")

    pixdata = img.load()

    erase = (255, 255, 255, 0) # Transparent white

    # Iterate over all pixels and replace white with transparent
    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel = pixdata[x, y]
            if pixel[0] < 200 and pixel[1] > 200 and pixel[2] < 200: # checks if green value in RGB is strong
                pass
            else:    
                pixdata[x, y] = erase
                    
    return img


# Compares all PDFs in input folders against each other by first converting all
# to PIL images. Outputs results as images in selected directory.
def compare_pdfs():

    # try:    
    ############################################################
    # Debugging (Home PC)
    # input_dir_1.set("C:/Users/james/Documents/Personal/Prsojects/Python/PDF-compare/test/Current Set")
    # input_dir_2.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test/Markups")
    # output_dir.set("C:/Users/james/Documents/Personal/Projects/Python/PDF-compare/test")

    # Debugging (Work PC)
    # input_dir_1.set("C:/Users/AUJB508470/Documents/Projects/Python/PDF-compare/test_greenedoff/Input Folder 1")
    # input_dir_2.set("C:/Users/AUJB508470/Documents/Projects/Python/PDF-compare/test_greenedoff/Input Folder 2")
    # output_dir.set("C:/Users/AUJB508470/Documents/Projects/Python/PDF-compare/test_greenedoff/Output Folder")
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
    # print(input_files_1)
    # print(input_files_2)
    ############################################################
    
    # Check the number of files in each input folder matches
    if len(input_files_1) != len(input_files_2):
        Result = "Number of PDFs in each input folder doesn't match. Please check the contents of each folder."
        messagebox.showinfo("Error", Result)
        return

    ############################################################
    # Debugging
    print("Input Folder 1 Contents: ")
    print(os.listdir(input_dir_1.get()))
    print("Input Folder 2 Contents: ")
    print(os.listdir(input_dir_2.get()))
    ############################################################
    
    num_pdf_pairs = len(input_files_1)
    for pdf_index in range(num_pdf_pairs): #debugging

        # Pseudo progress bar
        b4.config(text="Comparing file {}/{}".format(pdf_index + 1, num_pdf_pairs))
        master.update()

        # Home dev
        # img_1 = convert_from_path(input_files_1[pdf_index])
        # img_2 = convert_from_path(input_files_2[pdf_index])

        # Work dev
        img_1 = convert_from_path(input_files_1[pdf_index], poppler_path=poppler_local)
        img_2 = convert_from_path(input_files_2[pdf_index], poppler_path=poppler_local)
        
        # Take absolute magnitude difference, pixel-by-pixel
        img_diff = get_img_abs_diff(img_1[0], img_2[0]) # Indexing img_1 and img_2 assumes each PDF is only one page long
        img_out_1 = img_diff

        img_greenoffs = extract_greenoffs(img_diff)
        # img_greenoffs.show()
        
        # Grayscale image & threshold.
        img_out_1 = ImageOps.grayscale(img_out_1)
        img_out_1 = img_out_1.point(lambda p: 0 if p > 250 else 255)
        img_out_2 = img_out_1 # img_out_1 ends up being yellow halo, img_out_2 being red diffs

        halo_opacity = 100 # 255/100 -> approx 30% opacity
        img_out_1 = create_img_halo(img_out_1, halo_opacity)
        
        ############# img_out_2 processing (red text)
        img_out_2 = ImageOps.invert(img_out_2)
        
        # Colour replace: all black to red
        orig_colour = (0,0,0) # Black
        replacement_colour = (255,0,0) # Red
        img_out_2 = img_colour_replace(img_out_2, orig_colour, replacement_colour)

        # Make all white pixels transparent
        orig_colour = (255, 255, 255, 255)
        replacement_colour = (255, 255, 255, 0)
        img_out_2 = img_colour_replace_rgba(img_out_2, orig_colour, replacement_colour)
        
        ####################################################################################
        # Overlay image 1 (halo) and 2 (red diffs)

        img_out_1.paste(img_out_2, (0,0), mask = img_out_2) 
        img_out_1.paste(img_greenoffs, (0,0), mask = img_greenoffs) 
        
        ####################################################################################

        # Overlay mask on original 
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
    
    # Change button text back to "Compare PDFs"
    b4.config(text="Compare PDFs")
    master.update()

    Result = "PDF Comparison Complete."
    messagebox.showinfo("Success!", Result)
    
    # except:
    #     Result = "Invalid folder location, or no PDFs found in folder."
    #     messagebox.showinfo("Result", Result)
 
    # else:
    #     Result = "PDF Comparison Complete."
    #     messagebox.showinfo("Success!", Result)
 
 
# Initialise GUI
master = Tk()
master.title("PDF Comparison Tool V3")

# Global variables for storing directories of input files
input_dir_1 = StringVar()
input_dir_2 = StringVar()
input_dir_3 = StringVar()
# Output path
output_dir = StringVar()

Label(master, text="Input Folder 1 Location:").grid(row=0, sticky=W) 
Label(master, text="Input Folder 2 Location:").grid(row=1, sticky=W) 
# Label(master, text="Greened Off Markups Folder Location:").grid(row=2, sticky=W) 
Label(master, text="Output Folder Location:").grid(row=2, sticky=W) 

# Dynamic labels updated when directories are selected
lbl1 = Label(master,textvariable=input_dir_1)
lbl1.grid(row=0, column=1)
lbl2 = Label(master,textvariable=input_dir_2)
lbl2.grid(row=1, column=1)
lbl3 = Label(master,textvariable=output_dir)
lbl3.grid(row=2, column=1)
# lbl3 = Label(master,textvariable=output_dir)
# lbl3.grid(row=3, column=1)
 
# Buttons for selecting input/output directories
b1 = Button(master, text="Browse", command=browse_input_dir_1)
b1.grid(row=0, column=2, padx=5, pady=5)
b2 = Button(master, text="Browse", command=browse_input_dir_2)
b2.grid(row=1, column=2, padx=5, pady=5)
b3 = Button(master, text="Browse", command=browse_output_dir)
b3.grid(row=2, column=2, padx=5, pady=5)
# b4 = Button(master, text="Browse", command=browse_output_dir)
# b4.grid(row=3, column=2, padx=5, pady=5)

# Button to run tool
b4 = Button(master, text="Compare PDFs", command=compare_pdfs)
b4.grid(row=3, column=0, columnspan=3, rowspan=2, padx=5, pady=5)
  
mainloop()