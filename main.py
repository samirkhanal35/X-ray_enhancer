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
left_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
left_frame.place(x=40,y=150)
left_frame.pack_propagate(0)

#left image label
# inp_image = tk.Label(left_frame, text="Input Image", font=("none Bold",10))
# inp_image.pack()


#left label
left_label = tk.Label(window, text="Input Image", font=("none Bold",20))
left_label.place(x=200,y=120)


#rigt_frame
rigt_frame = tk.Frame(window, width=400, height=400, highlightbackground="black", highlightthickness=1)
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
    
    img1 = cv2.resize(img,(400,400)) #(a high-quality downsampling filter)       
    return img1

def Enhance():
    img_rgb = variables.img
    # img_oil = cv2.xp
    # hoto.oilPainting(img_rgb, 3, 1)
    numDownSamples = 2 # number of downscaling steps
    numBilateralFilters = 4 # number of bilateral filtering steps

    # -- STEP 1 --
    # downsample image using Gaussian pyramid
    img_color = img_rgb
    for _ in range(numDownSamples):
        img_color = cv2.pyrDown(img_color)

    # repeatedly apply small bilateral filter instead of applying
    # one large filter
    
    for _ in range(numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 7, 15, 20) 
        #cv2.bilateralFilter(src, d, sigmaColor, sigmaSpace[, dst[, borderType]]) 

    # upsample image to original size
    
    for _ in range(numDownSamples):
        img_color = cv2.pyrUp(img_color)

    
    # img_gray = cv2.GaussianBlur(img_color, (21, 21), 0)
    # img_weight = cv2.addWeighted(img_gray, 1.5, img_gray, -0.9, 0)
    
    #sharpening the image
    filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    img_sharp = cv2.filter2D(img_color,-1,filter)
    img_sharp = cv2.filter2D(img_sharp,-1,filter)
    # img_final = cv2.blur(img_sharp,(5,5))
    img_final = cv2.GaussianBlur(img_sharp, (9, 9), 0)
    img_final = cv2.filter2D(img_final,-1,filter)

    #sharpening the image
    # filter = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    # img_weight = cv2.filter2D(img_weight,-1,filter)
    
    #histogram_equalization
    

    # img = cv2.equalizeHist(img_weight)
    b, g, r = cv2.split(img_final)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    img = cv2.merge((blue, green, red))


    #brightness decrement
    value = 30
    lim = 60
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    v[v > lim] -= value

    
    

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)


    #signature
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX 

    # org 
    h,w,d = img.shape
    
    org = (w-60, h-20) 
    
    # fontScale 
    fontScale = 1

    # Blue color in BGR 
    color = (0, 0, 255) 

    # Line thickness of 1 px 
    thickness = 2

    # Using cv2.putText() method 
    img = cv2.putText(img, 'S.K.', org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 

    

    #resizing for image display
    variables.out_img = resize_img(img)
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
