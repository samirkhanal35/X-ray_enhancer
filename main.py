import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np

#from tkinter import *
window = tk.Tk()

window.title("X-ray Enhancer")
window.geometry('1200x800')

#header
header = tk.Label(window, text="GET YOUR X-Ray Enhanced HERE!", bg="red", fg="black" ,font=("none bold",35), anchor="n") 
#anchor=n for top-central justification
header.place(x=300,y=1)
#header.pack()

#left frame
left_frame = tk.Frame(window, width=400, height=500, highlightbackground="black", highlightthickness=1)
left_frame.place(x=40,y=150)
left_frame.pack_propagate(0)

#left image label
# inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
# inp_image.pack()


#left label
left_label = tk.Label(window, text="Input Image", font=("none Bold",20))
left_label.place(x=200,y=120)


#rigt_frame
rigt_frame = tk.Frame(window, width=400, height=500, highlightbackground="black", highlightthickness=1)
rigt_frame.place(x=760,y=150)
rigt_frame.pack_propagate(0)

#right image label
# out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
# out_image.pack()



#right label
right_label = tk.Label(window, text="Output Image", font=("none Bold",20))
right_label.place(x=930,y=120)



class variables:
    img = ""
    inp_img = ""
    out_img = ""

    #left image label
    inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
    inp_image.pack()

    #right image label
    out_image = tk.Label(rigt_frame, text="Output Image", font=("none Bold",10))
    out_image.pack()

def working_design():
    #image selection button
    img_selection_btn = tk.Button(window, text="Select Image", fg="black", font=("none Bold",20) , command=open_file)
    img_selection_btn.place(x=520, y=100)
    #*--------------------------------
    # #sketching button
    img_sketching_btn = tk.Button(window, text="Enhance", fg="black", font=("none Bold",20) , command=Enhance)
    img_sketching_btn.place(x=520, y=150)


def open_file(): 
    filename = filedialog.askopenfilename(filetypes=(("JPEG","*.jpg"),("PNG","*.png"),("All Files","*.*"))) 

    if filename!="" :
        variables.img = cv2.imread(filename).astype('uint8')
        #resizing for image display
        variables.inp_img = resize_img(variables.img)
        #Rearranging the color channel
        b,g,r = cv2.split(variables.inp_img)
        img = cv2.merge((r,g,b))

        #convert image object into TkPhoto object
        im = Image.fromarray(img)
        img1 = ImageTk.PhotoImage(image=im)

        variables.inp_image.pack_forget()
        left_frame.update()

        variables.inp_image = tk.Label(left_frame, image=img1)
        variables.inp_image.image = img1
        variables.inp_image.pack()
        left_frame.update()

        
        
 

def resize_img(img):
    
    img1 = cv2.resize(img,(400,500)) #(a high-quality downsampling filter)       
    return img1

def Enhance():
    img_rgb = variables.img
    #gray conversion
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    #blurrring to remove noise
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    #Laplacian filter
    
    ddepth = cv2.CV_64F
    kernel_size = 3
    laplacian = cv2.Laplacian(blur, ddepth, ksize=kernel_size)

    # converting back to uint8
    dst = cv2.convertScaleAbs(laplacian)

    #subtraction of image
    sub = cv2.subtract(gray, dst)
    # avg1 = cv2.blur(sub, (5, 5))


    #sobel filter
    scale = 2
    delta = 1
    ddepth = cv2.CV_64F
    grad_x = cv2.Sobel(sub, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    # Gradient-Y
    # grad_y = cv2.Scharr(gray,ddepth,0,1)
    grad_y = cv2.Sobel(sub, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    
    
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    
    
    sobel_img = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    #smoothing with 5x5 averaging filter
    avg = cv2.blur(sobel_img, (5, 5))
    # avg = cv2.GaussianBlur(sobel_img, (3, 3), 0)

    #mask = multiplication of result of subtraction and smoothed image
    # mask = cv2.multiply(sub, avg)
    # mask = cv2.bitwise_xor(sub, avg)
    # mask = cv2.add(sub, avg)
    # mask = cv2.bitwise_or(sub, avg)
    mask = cv2.bitwise_and(sub, avg)

    #adding mask with first gray image
    summ = cv2.add(gray, mask)
    # sub = cv2.subtract(summ, dst)

    # blur = cv2.GaussianBlur(summ, (3, 3), 0)







    color = cv2.cvtColor(summ, cv2.COLOR_GRAY2BGR)


    #resizing for image display
    variables.out_img = resize_img(color)
    #Rearranging the color channel
    b,g,r = cv2.split(variables.out_img)
    img = cv2.merge((r,g,b))
    #convert image object into TkPhoto object
    im = Image.fromarray(img)
    img1 = ImageTk.PhotoImage(image=im)
    
    variables.out_image.pack_forget()
    rigt_frame.update()

    variables.out_image = tk.Label(rigt_frame, image=img1)
    variables.out_image.image = img1
    variables.out_image.pack()
    rigt_frame.update()


working_design()

window.mainloop()
