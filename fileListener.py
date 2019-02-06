

import os
import numpy as np
import cv2
import tkinter as tk
from PIL import ImageGrab, Image
import threading
import time
import rawpy
import imageio
import PIL.ExifTags

path = {}
oldFileList = [];
imageList = [];
global currentImageName;


def setupFolder():
    data = open('./path.txt','r')
    for line in data:
        path[line.split(":")[0]] = line.split(":")[1].strip();
    for filename in os.listdir(path['folderPath']):
        oldFileList.append(filename);

def folderListen():
    newFileList = [];
    global received;
    global currentImageName;
    global oldFileList;
    fileListCopy = oldFileList
    received = 0;
    for filename in os.listdir(path['folderPath']):
        newFileList.append(filename);
    if len(newFileList) != len(fileListCopy):
        for file in newFileList:
            if file not in fileListCopy :
                fileListCopy.append(file);
                img = cv2.imread(path['folderPath']+'/'+file,-1);
                print(file);
                imageList.append(img);
                currentImageName = file;
                received = 1;
    oldFileList = newFileList;
            
def GUIListener():
    global photo
##    photo = tk.PhotoImage(file=path['folderPath']+"/"+ currentImageName)
    photo = tk.PhotoImage(file=path['folderPath']+"/"+ "1.png")
    canvas.create_image(20,20, anchor='nw', image=photo)

def propertyListener():
##    state = os.stat(path['folderPath']+"/" + currentImageName);
    state = os.stat(path['folderPath']+"/" + "1.png");
    print(state);
##    canvas.create_text

def setupGUI():
    global root
    global canvas
    global photo
    global photoList
    
    root.title("Camaro Analysis");
    root.overrideredirect(True);
    root.overrideredirect(False);
    root.attributes('-fullscreen',True);
    canvas = tk.Canvas(root, width=root.winfo_screenwidth(),height=root.winfo_screenheight());
    canvas.pack();
    photoList = tk.Canvas(root, width=root.winfo_screenwidth(),height=root.winfo_screenheight());
    photoList.pack();
    scrollbar = Scrollbar(root)
    scrollbar.pack( side = RIGHT, fill = Y )
##    photo = tk.PhotoImage(file=path['folderPath']+"/"+ "JRBVR.png")
##    canvas.create_image(20,20, anchor='nw', image=photo)

def loopImage():
    while 1:
        folderListen();
        if received == 1:
##            GUIListener();
            propertyListener();
            break;

def find_canon():
    global opencv_img;
    global error
##    img = cv2.imread(path['imagePath'],-1);
    img = Image.open(path['imagePath']);
    
    pil_img = ImageGrab.grab();
    opencv_img = np.array(pil_img);
    bw_img = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2RGB);
    pix = pil_img.load();
    
    targetPix = img.load();

    print(img.size);
    print(targetPix[1,1]);
    print(pil_img.width);

 
    for width in range(0, pil_img.width):
        for height in range(0,pil_img.height):
            invalid = False;
            w = width
            h = height
            for a in range(0,img.width):
                h = height;
                for b in range(0,img.height):  
                    if not (pix[w,h][0] == targetPix[a,b][0] and pix[w,h][1] == targetPix[a,b][1] and pix[w,h][2] == targetPix[a,b][2]):
                        invalid = True;
                        break;                    
                    else:
                        h+=1;
                if (invalid):
                    break;
                else:
                    w+=1;
        if not invalid:
            print("hi");
            break;
    if invalid:
        error = tk.Tk();
        error.title("Error");
        warning = tk.Canvas(error, width=300,height=100);
        warning.pack();
        warning.create_text(150,50,text="Cannot Find EOS, Please Open Manually");
        error.mainloop();

def showData():
    global raw;
    global canvas;
    img = PIL.Image.open('./test.JPG')
    exif = {
        PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS
    }
    info = "";
    for k in exif:
        info += k + ": "  + str(exif[k]) + "\n\n";
    canvas.create_text(root.winfo_screenwidth()/ 3 * 2,root.winfo_screenheight() / 5, text=info);
##setupFolder();
####find_canon();
##
##root = tk.Tk();
##setupGUI();
##canvas.create_line(5,5,root.winfo_screenwidth()-5,5,root.winfo_screenwidth()-5,root.winfo_screenheight()-5,5,root.winfo_screenheight()-5,5,5,fill="black");
##raw = rawpy.imread('./IMG_4405.cr2')
##showData();

from tkinter import *
root=Tk()
frame=Frame(root,width=300,height=300)
frame.grid(row=0,column=0)
canvas=Canvas(frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
hbar=Scrollbar(frame,orient=HORIZONTAL)
hbar.pack(side=BOTTOM,fill=X)
hbar.config(command=canvas.xview)
vbar=Scrollbar(frame,orient=VERTICAL)
vbar.pack(side=RIGHT,fill=Y)
vbar.config(command=canvas.yview)
canvas.config(width=300,height=300)
canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
canvas.pack(side=LEFT,expand=True,fill=BOTH)

root.mainloop()

##rgb = raw.postprocess()
##rgb.
##print(raw.raw_image) 
##photo = tk.PhotoImage(file="./target.png")
##print("hi");
##photo = ImageTk.PhotoImage(Image.open(file=path['folderPath']+"/"+ "JRBVR.png"));
##print(raw.raw_image_visible)
##rgb.size()
##cv2.imshow('image',rgb.);
##canvas.create_image(20,20, anchor='nw', r)


##loopFolderThread = threading.Thread(target=loopImage);
##loopFolderThread.daemon=True
##loopFolderThread.start();

##root.mainloop();




