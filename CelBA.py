import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import *
from PIL import ImageTk, Image
import cv2
from matplotlib import pyplot as plt
import os
import Batch_parameters 
import Batch_skeletons 
import Contour_selection
import sys
import subprocess
from threading import Thread
import glob
import numpy as np

###Root
root = tk.Tk()
root.title("First_Program")
root.geometry("1920x1080")

tabControl = Notebook(root) 
  
tab1 = Frame(tabControl) 
tab2 = Frame(tabControl) 
tab3 = Frame(tabControl) 
tab4 = Frame(tabControl)
  
tabControl.add(tab1, text ='Select files') 
tabControl.add(tab2, text ='Contours') 
tabControl.pack(expand = 1, fill ="both") 
  


def open_folder():
    global foldernamevar
    file = filedialog.askdirectory()
    foldernamevar = file
    Foldername.configure(text=foldernamevar)

Openfolder = Button(tab1,text = "Select folder",command=lambda:open_folder())
Openfolder.grid(row=0,column=0)




foldernamevar = "No folder selected"
Foldername = Label(tab1, text = foldernamevar)
Foldername.grid(row=0,column=1)

def process_button_clicked():
    # Download the file in a new thread.
    Thread(target=process).start()

def process():
    Contour_selection.contourslider(foldernamevar, 300)
    Contour_selection.startcontours(foldernamevar,300,[0,1,2,3,4],contourstatus)
    #Make this as big as possible!!
    print("contours done")
    Batch_skeletons.makeskeletons(foldernamevar,5,skeletonstatus)
    print("skeletons done")
    #Batch_parameters.fixswitching(foldernamevar,fixstatus)
    #print("fixswitching done")
    Batch_parameters.overlayskeletonfullimage(foldernamevar,overlaystatus)
    print("overlay done")
    


def contourstatus(count,step, total_data):

    if count == 0:
        # Set the maximum value for the progress bar.
        contourbar.configure(maximum=total_data)
    else:
        # Increase the progress.
        contourbar.step(step)

def skeletonstatus(count,step, total_data):

    if count == 0:
        # Set the maximum value for the progress bar.
        skeletonbar.configure(maximum=total_data)
    else:
        # Increase the progress.
        skeletonbar.step(step)



def overlaystatus(count,step, total_data):

    if count == 0:
        # Set the maximum value for the progress bar.
        overlaybar.configure(maximum=total_data)
    else:
        # Increase the progress.
        overlaybar.step(step)


Process = Button(tab1,text = "Click to process",command=lambda:process_button_clicked())
Process.grid(row=0,column=2)


contourbar = Progressbar(tab1)
contourbar.place(x=110,y=27)
contourtext = Label(tab1,text="Building contours")
contourtext.place(x=0,y=27)


skeletonbar = Progressbar(tab1)
skeletonbar.place(x=110,y=47)
skeletontext = Label(tab1,text="Building skeletons")
skeletontext.place(x=0,y=47)



overlaybar = Progressbar(tab1)
overlaybar.place(x=110,y=67)
overlaytext = Label(tab1,text="Building overlays")
overlaytext.place(x=0,y=67)







#Moving through images 
#Tab 2


filenamevar = "No folder selected"
Filename = Label(tab2, text = filenamevar)
Filename.place(x=805,y=10)
frame = 0

imageblank = ImageTk.PhotoImage(image = Image.fromarray(cv2.imread("blank.jpg")))

myLabel = Label(tab2,image=imageblank)
myLabel.grid(row=2,column=0)

def open_file():
    global relative_path
    global imageseries
    global file
    file = filedialog.askdirectory()
    Filename.configure(text=file)
    start = ""
    relative_path = os.path.relpath(file, start) + "/skeletons/outputoverlay/"
    length_path = relative_path + "0/*.png" 
    imageseries = len(glob.glob(length_path)) -1
    w.configure(to_=imageseries)

Openfile = Button(tab2,text = "Choose folder with Tab1 completed",command=lambda:open_file())
Openfile.grid(row=0,column=0)

imageseries = 750

def setimage():
    global firstname
    global wormnumber
    wormnumber = int(Wormselect.get()) -1
    firstname = relative_path + str(wormnumber) + "/0.png"
    image1 = ImageTk.PhotoImage(image = Image.fromarray(cv2.imread(firstname)))
    myLabel.configure(image=image1)
    myLabel.image = image1

def updateImg(val):
    val = int(round(float(val),2))
    imagename = firstname.replace("0.png","")
    imagenew = imagename + str(val) + ".png"
    print(imagenew)
    image = ImageTk.PhotoImage(image = Image.fromarray(cv2.imread(imagenew)))
    myLabel.configure(image = image)
    myLabel.image = image

    #Updating curling value
    loadnamecurl = file + "/skeletons/frameset.npy"
    currentcurl = "Curling = " + str(np.load(loadnamecurl,allow_pickle=True)[wormnumber][w.get()])
    Curlingtext.configure(text=currentcurl)

    #Updating kappa value
    loadnamekappa = file + "/skeletons/totalcurvature.npy"
    currentkappa = "Curvature = " + str(np.load(loadnamekappa,allow_pickle=True)[wormnumber][w.get()])
    Kappatext.configure(text=currentkappa)

    #Updating turning point value
    loadnametp = file + "/skeletons/totalturningpoints.npy"
    currenttp = "Turning points = " + str(np.load(loadnametp,allow_pickle=True)[wormnumber][w.get()])
    Tptext.configure(text=currenttp)

    #Updating wave number value
    loadnamewavenumber = file + "/skeletons/totalwavenumber.npy"
    currentwavenumber = "Body wave number = " + str(np.load(loadnamewavenumber,allow_pickle=True)[wormnumber][w.get()])
    Wavenumbertext.configure(text=currentwavenumber)

    #Updating asymmetry
    loadnameasymmetry = file + "/skeletons/totalasymmetry.npy"
    currentasymmetry = "Asymmetry = " + str(np.load(loadnameasymmetry,allow_pickle=True)[wormnumber][w.get()])
    Asymmetrytext.configure(text=currentasymmetry)

    #Updating bend
    loadnamebend = file + "/skeletons/totalbend.npy"
    currentbend = "Bend = " + str(np.load(loadnamebend,allow_pickle=True)[wormnumber][w.get()])
    Bendtext.configure(text=currentbend)

    #Updating stretch
    loadnamestretch = file + "/skeletons/totalstretch.npy"
    currentstretch = "Stretch = " + str(np.load(loadnamestretch,allow_pickle=True)[wormnumber][w.get()])
    Stretchtext.configure(text=currentstretch)

    #Updating activity
    loadnameactivity = file + "/skeletons/totalactivity.npy"
    currentactivity = "Activity = " + str(np.load(loadnameactivity,allow_pickle=True)[wormnumber][w.get()])
    Activitytext.configure(text=currentactivity)

    #Updating movement
    loadnamemovement = file + "/skeletons/totalmovement.npy"
    currentmovement = "Movement = " + str(np.load(loadnamemovement,allow_pickle=True)[wormnumber][w.get()])
    Movementtext.configure(text=currentmovement)

    #Updating movement distance
    loadnamemovementdistance = file + "/skeletons/totalmovementdistance.npy"
    currentmovementdistance = "Movement distance (mm) = " + str(np.load(loadnamemovementdistance,allow_pickle=True)[wormnumber][w.get()])
    Movementdistancetext.configure(text=currentmovementdistance)

    #Updating movement speed
    loadnamemovementspeed = file + "/skeletons/totalmovementspeed.npy"
    currentmovementspeed = "Movement speed (mm/s) = " + str(np.load(loadnamemovementspeed,allow_pickle=True)[wormnumber][w.get()])
    Movementspeedtext.configure(text=currentmovementspeed)


w = tk.Scale(tab2, from_=0, to_=imageseries, orient="horizontal", command=updateImg,length=500)
w.grid(row=1,column = 0)



Wormselect = Combobox(
    tab2,
    state="readonly",
    values=[1,2,3,4,5]
    )

Wormselect.place(x=805,y=30)

Updateworm = Button(tab2,text="Update worm",command=setimage)
Updateworm.place(x=950,y=28)



#Curlingstuff

def paramsclick():
    Thread(target=params).start()

def params():
    #Curling
    Batch_parameters.count_curling(file)
    print("Curling done")
    loadnamecurl = file + "/skeletons/frameset.npy"
    currentcurl = "Curling = " + str(np.load(loadnamecurl,allow_pickle=True)[wormnumber][w.get()])
    Curlingtext.configure(text=currentcurl)

    #Kappa
    Batch_parameters.kappa(file)
    print("Kappa done")
    loadnamekappa = file + "/skeletons/totalcurvature.npy"
    currentkappa = "Curvature = " + str(np.load(loadnamekappa,allow_pickle=True)[wormnumber][w.get()])
    Kappatext.configure(text=currentkappa)

    #Turning points
    Batch_parameters.turningpointarray(file)
    print("Turning points done")
    loadnametp = file + "/skeletons/totalturningpoints.npy"
    currenttp = "Turning points = " + str(np.load(loadnametp,allow_pickle=True)[wormnumber][w.get()])
    Tptext.configure(text=currenttp)

    #Wave number
    Batch_parameters.bodywavenumber(file)
    print("Wave number done")
    loadnamewavenumber = file + "/skeletons/totalwavenumber.npy"
    currentwavenumber = "Wave number = " + str(np.load(loadnamewavenumber,allow_pickle=True)[wormnumber][w.get()])
    Wavenumbertext.configure(text=currentwavenumber)

    #Asymmetry
    Batch_parameters.asymmetry(file)
    print("Asymmetry done!")
    loadnameasymmetry = file + "/skeletons/totalasymmetry.npy"
    currentasymmetry = "Asymmetry = " + str(np.load(loadnameasymmetry,allow_pickle=True)[wormnumber][w.get()])
    Asymmetrytext.configure(text=currentasymmetry)

    #Bend
    Batch_parameters.bend(file)
    print("Stretch done!")
    loadnamebend = file + "/skeletons/totalbend.npy"
    currentbend = "Bend = " + str(np.load(loadnamebend,allow_pickle=True)[wormnumber][w.get()])
    Bendtext.configure(text=currentbend)

    #Stretch
    Batch_parameters.stretch(file)
    print("Stretch done!")
    loadnamestretch = file + "/skeletons/totalstretch.npy"
    currentstretch = "Stretch = " + str(np.load(loadnamestretch,allow_pickle=True)[wormnumber][w.get()])
    Stretchtext.configure(text=currentstretch)

    #Activity
    Batch_parameters.activity(file)
    print("Activity done!")
    loadnameactivity = file + "/skeletons/totalactivity.npy"
    currentactivity = "Activity = " + str(np.load(loadnameactivity,allow_pickle=True)[wormnumber][w.get()])
    Activitytext.configure(text=currentactivity)

    #Movement
    Batch_parameters.movement(file)
    print("Movement done!")
    loadnamemovement = file + "/skeletons/totalmovement.npy"
    currentmovement = "Movement = " + str(np.load(loadnamemovement,allow_pickle=True)[wormnumber][w.get()])
    Movementtext.configure(text=currentmovement)

    #Movement distance
    Batch_parameters.movementdistance(file)
    print("Movement distance done!")
    loadnamemovementdistance = file + "/skeletons/totalmovementdistance.npy"
    currentmovementdistance = "Movement distance (mm) = " + str(np.load(loadnamemovementdistance,allow_pickle=True)[wormnumber][w.get()])
    Movementdistancetext.configure(text=currentmovementdistance)

    #Movement speed
    Batch_parameters.movementspeed(file)
    print("Movement speed done!")
    loadnamemovementspeed = file + "/skeletons/totalmovementspeed.npy"
    currentmovementspeed = "Movement speed (mm/s) = " + str(np.load(loadnamemovementspeed,allow_pickle=True)[wormnumber][w.get()])
    Movementspeedtext.configure(text=currentmovementspeed)

    Batch_parameters.save(file,3)
    print("Results saved")





Calculateparams = Button(tab2,text="Calculate parameters",command=paramsclick)
Calculateparams.place(x=1033,y=28)

currentcurl = "No parameters calculated!"
Curlingtext = Label(tab2,text=currentcurl)
Curlingtext.place(x=1030,y=65)


currentkappa = "No parameters calculated!"
Kappatext = Label(tab2,text=currentkappa)
Kappatext.place(x=1030,y=85)

currenttp = "No parameters calculated!"
Tptext = Label(tab2,text=currenttp)
Tptext.place(x=1030,y=105)

currentwavenumber = "No parameters calculated!"
Wavenumbertext = Label(tab2,text=currentwavenumber)
Wavenumbertext.place(x=1030,y=125)

currentasymmetry = "No parameters calculated!"
Asymmetrytext = Label(tab2,text=currentasymmetry)
Asymmetrytext.place(x=1030,y=145)

currentbend = "No parameters calculated!"
Bendtext = Label(tab2,text=currentbend)
Bendtext.place(x=1030,y=165)

currentstretch = "No parameters calculated!"
Stretchtext = Label(tab2,text=currentstretch)
Stretchtext.place(x=1030,y=185)


currentactivity = "No parameters calculated!"
Activitytext = Label(tab2,text=currentactivity)
Activitytext.place(x=1030,y=205)

currentmovement = "No parameters calculated!"
Movementtext = Label(tab2,text=currentmovement)
Movementtext.place(x=1030,y=225)

currentmovementdistance = "No parameters calculated!"
Movementdistancetext = Label(tab2,text=currentmovementdistance)
Movementdistancetext.place(x=1030,y=245)

currentmovementspeed = "No parameters calculated!"
Movementspeedtext = Label(tab2,text=currentmovementspeed)
Movementspeedtext.place(x=1030,y=265)

###Event Loop
root.mainloop()

