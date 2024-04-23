import cv2 as cv
from matplotlib import pyplot as plt
import glob
import numpy as np
import os
import math

resolution = 1024
outputdirectory = "C:/Users/jhepw/Documents/Project/Processed/"


#Selection for threshold area value
def contourslider(folder,size):
    foldername = str(folder) + "/*.jpg"
    many = 0


    #Creates output folder name
    newoutput = ""
    for chars in range(0,len(folder)):
        index = len(folder) - chars - 1
        if folder[index] != "/" and many == 0:
            newoutput = newoutput + folder[index] 
        if folder[index] == "/":
            many = 1
    
    newoutput = newoutput[::-1]
    overalloutput = outputdirectory + str(newoutput)
    print(overalloutput)

    #Loads images and converts to binary
    imagename = glob.glob(foldername)[0]
    imagebig = cv.imread(imagename)
    image = cv.resize(imagebig,(resolution,resolution))
    imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(imgray,127,255,0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 

    #Creates and sorts worm contours
    large_contour = []
    inside_contour = []

    for contour in contours:
        area = cv.contourArea(contour)
        if area > size:
            large_contour.append(contour)



    for worms in range(0,len(large_contour)):
        blankread = cv.imread("blank.jpg")
        blank = cv.resize(blankread,(resolution,resolution))
        #Draws on blank background filled contour of our largest, outline contours in green
        cv.drawContours(blank,[large_contour[worms]],-1,(0,255,0),thickness=cv.FILLED)            #Draws on this image the smaller, inside contours in black

        #Saves image
        if os.path.isdir("Processed") == False:
            os.mkdir("Processed")


        outputfolder = outputdirectory + str(newoutput) + "/firstcontours/" + str(size)
        outputfolder0 = outputdirectory + str(newoutput) + "/firstcontours"
 
        if os.path.isdir(overalloutput) == False:
            os.mkdir(overalloutput)


        if os.path.isdir(outputfolder0) == False:
            os.mkdir(outputfolder0)

            
        if os.path.isdir(outputfolder) == False:
            os.mkdir(outputfolder)
        
        strname = outputfolder + "/" + str(worms) + ".png"
        print(strname)
        plt.imsave(strname,blank)



#After deciding on threshold values, creates contours for every frame, ensures they are saved to the same worm name. 
def startcontours(folder, size, worms, contourstatus):
    
    #Creating output folder name
    foldername = str(folder) + "/*.jpg"
    progress = 0
    many = 0
    newoutput = ""
    for chars in range(0,len(folder)):
        index = len(folder) - chars - 1
        if folder[index] != "/" and many == 0:
            newoutput = newoutput + folder[index] 
        if folder[index] == "/":
            many = 1
    
    newoutput = newoutput[::-1]
    imagenamegeneral = outputdirectory + str(newoutput) + "/firstcontours/" + str(size) + "/"
    
    #Iterates through worms, frame names, creates contours and matches the closest one
    for worm in range(0,len(worms)):
        imagename = imagenamegeneral + str(worms[worm]) + ".png"
        imagebig = cv.imread(imagename)
        image = cv.resize(imagebig,(resolution,resolution))
        imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(imgray,127,255,0)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 

        firstcontourstart = contours[0][0]
        previouscontourstart = []
        count = -1

        for framename in glob.glob(foldername):
            count = count + 1
            #print(framename)
            framebig = cv.imread(framename)
            frame = cv.resize(framebig,(resolution,resolution))
            framegray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            wormret, wormthresh = cv.threshold(framegray,127,255,0)
            wormcontours, wormhiearchy = cv.findContours(wormthresh,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

            large_contours = []
            for wormcontour in wormcontours:
                area = cv.contourArea(wormcontour)
                if area > size-50:
                    large_contours.append(wormcontour)

            


            if len(previouscontourstart) == 0:
                distances = []
                for large_contour in large_contours:
                    thisdist = math.dist(firstcontourstart[0],large_contour[0][0])
                    distances.append(thisdist)
                smallestdistance = distances.index(min(distances))
                previouscontourstart = large_contours[smallestdistance][0]

                

            if len(previouscontourstart) != 0:
                distances = []
                for large_contour in large_contours:
                    thisdist = math.dist(previouscontourstart[0],large_contour[0][0])
                    distances.append(thisdist)
                smallestdistance = distances.index(min(distances))
                previouscontourstart = large_contours[smallestdistance][0]

            outputfolder = outputdirectory + str(newoutput) + "/" + str(worm)

            if os.path.isdir(outputfolder) == False:
                os.mkdir(outputfolder)
        

            thiscontourarea = cv.contourArea(large_contours[smallestdistance])   

            black_contours = []
            for wormcontour in wormcontours:
                area = cv.contourArea(wormcontour)
                if area < thiscontourarea:
                    black_contours.append(wormcontour)


            blankread = cv.imread("blank.jpg")
            blank = cv.resize(blankread,(resolution,resolution))
            cv.drawContours(blank,[large_contours[smallestdistance]],-1,(0,255,0),thickness=cv.FILLED)
            if len(black_contours) != 0:
                cv.drawContours(blank,black_contours,-1,(0,0,0),thickness=cv.FILLED)
            framename = framename.replace(str(folder) + "\\","")
            framename = framename.replace(".jpg","")
            strname = outputfolder + "/" + str(framename) + ".png"
            print(strname)
            cv.imwrite(strname,blank)

            contourstatus(progress,1,len(glob.glob(foldername))*len(worms))
            progress = progress+1
            



