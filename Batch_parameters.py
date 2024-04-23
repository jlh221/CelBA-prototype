import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import glob

outputdirectory = "C:/Users/jhepw/Documents/Project/Processed/"
#Pixel size, total image size/resolution. 0.0125mm is my guess, 10mm/800px
pixelsize = 0.0125
#Frame time, the time taken for one frame to pass. We have 750frames, 30 seconds, each frame = 0.04 seconds
frametime = 0.04

resolution = 1024
wormcount = 5


def checkskeletonorder(table):
    for itimepoint in range(0,len(table)):
        blankread = cv2.imread("blank.jpg")
        blank = cv2.resize(blankread,(resolution,resolution))
        count = 1
        for ipixel in table[itimepoint]:
            imagename = "output/" + str(itimepoint) + "_" + str(count) + ".png"
            image = cv2.circle(blank, ipixel, radius=0, color=(0, 255, 0), thickness=-1)
            plt.imsave(imagename,image)
            print(imagename)
            count = count + 1


def checklengths(folder):
    foldername = str(folder) + "/" + "skeletons/fixed/" + "*skel.npy" 
    for worms in glob.glob(foldername):
        table = np.load(worms, allow_pickle=True)
        lengths = []
        for iframes in range(0,len(table)):
            lengths.append(len(table[iframes]))
        print(sum(i < 25 for i in lengths))



def fixswitching(folder,fixstatus):
    many = 0

    newoutput = ""
    for chars in range(0,len(folder)):
        index = len(folder) - chars - 1
        if folder[index] != "/" and many == 0:
            newoutput = newoutput + folder[index] 
        if folder[index] == "/":
            many = 1
    
    newoutput = newoutput[::-1]
    overalloutput = outputdirectory + str(newoutput)


    foldername = str(overalloutput) + "/" + "skeletons/" + "*table.npy"
    bigtable = []
    for worms in glob.glob(foldername):
        table = np.load(worms, allow_pickle=True)
        bigtable.append(table)
    
    step=0
    for iworms in range(0,len(bigtable)):
        print("Worm number:" + str(iworms))
        newtable = [bigtable[iworms][0]]
        fixed = 0
        unfixable = 0
        correct = 1
        changes = [iworms]
        for frames in range(1,len(bigtable[iworms])):
            pixeldist = math.dist(bigtable[iworms][frames][0],newtable[frames-1][0])
            if pixeldist < 100:
                newtable.append(bigtable[iworms][frames])
                correct = correct + 1
                changes.append(iworms)
            else:
                count = 0
                for otherworms in range(0,len(bigtable)):
                    pixeldist = math.dist(bigtable[otherworms][frames][0],newtable[frames-1][0])
                    if pixeldist < 100:
                        newtable.append(bigtable[otherworms][frames])
                        fixed = fixed + 1
                        count = 1
                        changes.append(otherworms)
                if count == 0:
                    newtable.append(newtable[frames-1])
                    unfixable = unfixable + 1
                    changes.append(iworms)
            fixstatus(step,1,len(glob.glob(foldername))*(len(bigtable[0])))
            step = step + 1
        print(str(correct) + "correct frames, and " + str(fixed) + " fixed frames, and " + str(unfixable) + " unfixable frames")

        
        newtable = np.asanyarray(newtable,dtype=object)
        filename = str(overalloutput) + "/skeletons/" + "fixed/" + str(iworms) + "skel"
        changesfilename = str(overalloutput) + "/skeletons/" + "fixed/" + str(iworms) + "changes" 
        if os.path.isdir(str(overalloutput) + "/skeletons/fixed") == False:
            os.mkdir(str(overalloutput) + "/skeletons/fixed")
        np.save(filename,newtable,allow_pickle=True)
        np.save(changesfilename,changes,allow_pickle=True)
    




    foldername = str(overalloutput) + "/" + "skeletons/" + "*ends.npy"
    bigendstable = []
    for worms in glob.glob(foldername):
        oldendstable = np.load(worms, allow_pickle=True)
        bigendstable.append(oldendstable)
    


    for iworms in range(0,len(bigendstable)):
        correctends = 0
        changedends = 0
        newends = []
        print("Worm number:" + str(iworms))
        changesfilename = str(overalloutput) + "/skeletons/" + "fixed/" + str(iworms) + "changes.npy" 
        changes = np.load(changesfilename,allow_pickle=True)
        for iframes in range(0,len(changes)):
            if changes[iframes] == iworms:
                correctends = correctends + 1
                newends.append(bigendstable[iworms][iframes])
            if changes[iframes] != iworms:
                changedends = changedends + 1
                newends.append(bigendstable[changes[iframes]][iframes])
        print("correct ends = " + str(correctends) + ", and changed ends = " + str(changedends))
        newendsfilename = str(overalloutput) + "/skeletons/" + "fixed/" + str(iworms) + "ends"
        newends = np.asanyarray(newends,dtype=object)
        np.save(newendsfilename,newends,allow_pickle=True)
    


    
    

def checkswitching(folder):
    foldername = str(folder) + "/skeletons/fixed/" + "*skel.npy"
    count = 0 
    for worms in glob.glob(foldername):
        table = np.load(worms, allow_pickle=True)
        for itimepoint in range(0,len(table)):
            blankread = cv2.imread("blank.jpg")
            blank = cv2.resize(blankread,(resolution,resolution))
            foldername = str(folder) + "/skeletons/output/" 
            imagename = str(folder) + "/skeletons/" + "output/" + str(count) + "/" + str(itimepoint) + ".png"
            print(foldername)
            if os.path.isdir(foldername) == False:
                os.mkdir(foldername)
            
            if os.path.isdir(str(foldername) + "/" + str(count)) == False:
                os.mkdir(str(foldername) + "/" + str(count))

            for pixels in range(0,len(table[itimepoint])):
                image = cv2.circle(blank, table[itimepoint][pixels], radius=0, color=(0, 255, 0), thickness=-1)
            plt.imsave(imagename,image)
            print(imagename)
        count = count + 1






#Normal curling
    
def count_curling(folder):

    foldername = str(folder) + "/skeletons/" + "*numends.npy"
    count = -1
    frameset = []
    percentset = []
    for worms in glob.glob(foldername):
        thiswormcurl = []
        curledframes = []
        count = count + 1
        ends = np.load(worms,allow_pickle=True)
        curl = 0
        uncurl = 0
        for frames in range(0,len(ends)):
            if len(ends[frames]) == 0:
                curl = curl + 1
                curledframes.append(frames)
                thiscurl=1
            if len(ends[frames]) == 1:
                curl = curl + 1
                curledframes.append(frames)
                thiscurl=1
            if len(ends[frames]) == 2:
                if math.dist(ends[frames][0],ends[frames][1]) < 5:
                    curl = curl + 1
                    curledframes.append(frames)
                    thiscurl=1
                else:
                    uncurl = uncurl + 1
                    thiscurl=0
            if len(ends[frames]) == 3:
                if math.dist(ends[frames][0],ends[frames][1]) < 5 or math.dist(ends[frames][0],ends[frames][2]) < 5 or math.dist(ends[frames][1],ends[frames][2]) < 5:
                    curl = curl + 1
                    curledframes.append(frames)
                    thiscurl=1
                else: 
                    uncurl = uncurl + 1
                    thiscurl=0
            if len(ends[frames]) == 4:
                if math.dist(ends[frames][0],ends[frames][1]) < 5 or math.dist(ends[frames][0],ends[frames][2]) < 5 or math.dist(ends[frames][0],ends[frames][3]) < 5 or math.dist(ends[frames][1],ends[frames][2]) < 5 or math.dist(ends[frames][1],ends[frames][3]) < 5 or math.dist(ends[frames][2],ends[frames][3]) < 5:
                    curl = curl + 1
                    curledframes.append(frames)
                    thiscurl=1
                else: 
                    uncurl = uncurl + 1
                    thiscurl=0
            if len(ends[frames]) > 4:
                uncurl = uncurl + 1
                thiscurl=0
    
            thiswormcurl.append(thiscurl)
            
        percentcurl = round(float(curl/(uncurl+curl)),2)
        frameset.append(thiswormcurl)
        percentset.append(percentcurl)

    print(frameset)
    framesetsave = np.asanyarray(frameset,dtype="object")
    framesetname = str(folder) + "/skeletons/frameset.npy"
    percentsetname = str(folder) + "/skeletons/percentset.npy"
    np.save(framesetname, framesetsave, allow_pickle=True)
    np.save(percentsetname, percentset, allow_pickle=True)
    print("saved!")







#Normal kappa
    
def kappa(folder):
    #Points must be ordered here!!!! Need something for circles. Probably also have to confirm direction at t junction in 6 worm
    #This is using numerical integration, so we can get +ve and -ve curvature, other methods only give one sign.
    foldername = str(folder) + "/skeletons/" + "*table.npy"
    totalcurvature = []
    for worms in glob.glob(foldername):
        table = np.load(worms,allow_pickle=True)
        newcurvaturetable = []
        for iframes in range(0,len(table)):
            framecurvature = []
            length = len(table[iframes])
            if length < 20:
                framecurvature = [0,0,0,0,0,0,0,0,0,0]
                print("shortskeleton")
            else:
                stepsize = round((length-1)/12,1)
                step = stepsize
                stepindex = [0]
                for stepgap in range(0,11):
                    step = step + stepsize
                    stepindex.append(step)

                stepindex[11] = length -1

                for chunks in range(0,10):
                    xs0 = table[iframes][int(round(stepindex[chunks]))][1]
                    xs1 = table[iframes][int(round(stepindex[chunks +1]))][1]
                    xs2 = table[iframes][int(round(stepindex[chunks +2]))][1]
                    xs0dash = (xs1-xs0)/(1/12)
                    xs1dash = (xs2-xs1)/(1/12)
                    xs0doubledash = (xs1dash-xs0dash)/(1/12)

                    ys0 = table[iframes][int(round(stepindex[chunks]))][0]
                    ys1 = table[iframes][int(round(stepindex[chunks +1]))][0]
                    ys2 = table[iframes][int(round(stepindex[chunks +2]))][0]
                    ys0dash = (ys1-ys0)/(1/12)
                    ys1dash = (ys2-ys1)/(1/12)
                    ys0doubledash = (ys1dash-ys0dash)/(1/12)

                    #kappa is negative for clockwise, positive for anti?
                    kappa = round(((xs0dash*ys0doubledash)-(xs0doubledash*ys0dash))/((((xs0dash)**2)+((ys0dash)**2))**(3/2)),2)
                    framecurvature.append(kappa)
            newcurvaturetable.append(framecurvature)
        totalcurvature.append(newcurvaturetable)
    totalcurvaturename = str(folder) + "/skeletons/totalcurvature.npy"
    np.save(totalcurvaturename, totalcurvature)



def overlayskeletonfullimage(folder,overlaystatus):
    many = 0

    newoutput = ""
    for chars in range(0,len(folder)):
        index = len(folder) - chars - 1
        if folder[index] != "/" and many == 0:
            newoutput = newoutput + folder[index] 
        if folder[index] == "/":
            many = 1
    
    newoutput = newoutput[::-1]
    overalloutput = outputdirectory + str(newoutput)




    bigfoldername = str(overalloutput) + "/skeletons/" + "*table.npy"
    count = 0 
    step=0
    for worms in glob.glob(bigfoldername):
        table = np.load(worms, allow_pickle=True)
        imagesname = str(folder) + "/*.jpg"
        imageset = glob.glob(imagesname)
        for itimepoint in range(0,len(table)):
            blank = cv2.imread(imageset[itimepoint])
            blank = cv2.resize(blank, (resolution,resolution))
            foldername = str(overalloutput) + "/skeletons/outputoverlay/" 
            imagename = str(overalloutput) + "/skeletons/" + "outputoverlay/" + str(count) + "/" + str(itimepoint) + ".png"
            if os.path.isdir(foldername) == False:
                os.mkdir(foldername)
            
            if os.path.isdir(str(foldername) + "/" + str(count)) == False:
                os.mkdir(str(foldername) + "/" + str(count))

            for pixels in range(0,len(table[itimepoint])):
                pointy = table[itimepoint][pixels][0]
                pointx = table[itimepoint][pixels][1]
                point = [pointx,pointy]
                image = cv2.circle(blank, point, radius=0, color=(255, 0, 0), thickness=2)
            cv2.imwrite(imagename,image)
            overlaystatus(step,1,len(glob.glob(bigfoldername))*len(table))
            step = step + 1
        count = count + 1





#fftvals = np.fft.fftshift(np.fft.fft2(kappa(testskel[0:32])))
#ifftvals = np.fft.ifft2(np.fft.ifftshift(fftvals))

#def maxvalue(array):
#    currentmax = 0
#    tmax = 0
#    smax = 0 
#
#    for t in range(0,len(array)):
#        for s in range(0,len(array[t])):
#            if abs(array[t][s]) > currentmax:
#                currentmax = abs(array[t][s])
#                tmax = t
#                smax = s
#                print("New maximum found at t = " + str(t) + " and s = " + str(s))
#                print("maxval = " + str(currentmax))
#
#x = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#
#
#y1 = []
#for i in range(0,len(x)):
#    xval = x[i]
#    yval = math.exp(-(xval**2))
#    y1.append(yval)
#
#
#y2 = []
#for i in range(0,len(x)):
#    xval = x[i]
#    yval = math.exp(-((xval**2)/4))
#    y2.append(yval)
#
#y1fft = np.fft.fftshift(np.fft.fft(y1))
#y2fft = np.fft.fftshift(np.fft.fft(y2))
#
#print((y1fft)/math.sqrt(2))
#print((y2fft))

#testskel = np.load("Nino FUS.P525L.HT.1.1\skeletons/fixed/4skel.npy",allow_pickle=True)
#testkappa = kappa(testskel)


















def bend(folder):
    foldername = str(folder) + "/skeletons/totalcurvature.npy"
    totalbend = []
    for worms in range(0,wormcount):
        wormbend = []
        table = np.load(foldername,allow_pickle=True)[worms]
        for iframes in range(0,len(table)):
            thisframewormbend = round(sum(abs(table[iframes])),2)
            if thisframewormbend > 4:
                thisframewormbend = 4
            wormbend.append(thisframewormbend)
        totalbend.append(wormbend)    
    totalbendname = str(folder) + "/skeletons/totalbend.npy"
    np.save(totalbendname, totalbend, allow_pickle=True)
    print("Bend done!")


def stretch(folder):
    foldername = str(folder) + "/skeletons/totalcurvature.npy"
    totalstretch = []
    for worms in range(0,wormcount):
        wormstretch = []
        table = np.load(foldername, allow_pickle=True)[worms]
        for iframes in range(0,len(table)):
            vector = table[iframes]
            absolute = abs(vector)
            max = np.max(absolute)
            min = np.min(absolute)
            stretch = round(max-min,2)
            if stretch >2:
                stretch = 2
            wormstretch.append(stretch)
        totalstretch.append(wormstretch)
    totalstretchname = str(folder) + "/skeletons/totalstretch.npy"
    np.save(totalstretchname,totalstretch,allow_pickle=True)
    print("Stretch done!")
            


def findturningpoint(kappaframe):
    ###################################### Slightly weird results, fault due to the resolution of kappa? investigate this. 



    tps = []
    for points in range(0,len(kappaframe)-1):
        a = kappaframe[points]
        b = kappaframe[points + 1]
        if a < 0 and b <0:
            tp = 0
        if a == 0 and b <0:
            tp = 1
        if a < 0 and b ==0:
            tp = 1
        if a < 0 and b > 0:
            tp = 1
        if a == 0 and b == 0:
            tp = 0
        if a > 0 and b > 0:
            tp = 0
        if a > 0 and b == 0:
            tp = 0
        if a > 0 and b < 0:
            tp = 1
        if a == 0 and b > 0:
            tp = 0

        tps.append(tp)

    for i in range(0,len(tps)-1):
        if tps[i] == 1:
            tps[i+1] = 0
    return(tps)


def turningpointarray(folder):
    foldername = str(folder) + "/skeletons/totalcurvature.npy"
    totalturningpoints = []
    for worms in range(0,wormcount):
        wormturningpoints = []
        table = np.load(foldername,allow_pickle=True)[worms]
        for iframes in range(0,len(table)):
            wormturningpoints.append(findturningpoint(table[iframes]))
        totalturningpoints.append(wormturningpoints)    
    totalturningpointsname = str(folder) + "/skeletons/totalturningpoints.npy"
    np.save(totalturningpointsname, totalturningpoints, allow_pickle=True)
    print("Turning points done!")



def bodywavenumber(folder):
    foldername = str(folder) + "/skeletons/totalturningpoints.npy"
    totalwavenumber = []
    for worms in range(0,wormcount):
        wormwavenumber = []
        table = np.load(foldername,allow_pickle=True)[worms]
        for iframes in range(0,len(table)):
            thisframewavenumber = sum(table[iframes])
            if thisframewavenumber > 3:
                thisframewavenumber = 4

            wormwavenumber.append(thisframewavenumber)
        totalwavenumber.append(wormwavenumber)    
    totalwavenumbername = str(folder) + "/skeletons/totalwavenumber.npy"
    np.save(totalwavenumbername, totalwavenumber, allow_pickle=True)
    print("Wave number done!")

def asymmetry(folder):
    foldername = str(folder) + "/skeletons/totalcurvature.npy"
    totalasymmetry = []
    for worms in range(0,wormcount):
        wormasymmetry = []
        table = np.load(foldername,allow_pickle=True)[worms]
        for iframes in range(0,len(table)):
            thisframewormasymmetry = abs(round(sum(table[iframes]),2))
            if thisframewormasymmetry > 2:
                thisframewormasymmetry = 2
            wormasymmetry.append(thisframewormasymmetry)
        totalasymmetry.append(wormasymmetry)    
    totalasymmetryname = str(folder) + "/skeletons/totalasymmetry.npy"
    np.save(totalasymmetryname, totalasymmetry, allow_pickle=True)
    print("Asymmetry done!")

def wavepropagation(folder):
    foldername = str(folder) + "/skeletons/totalturningpoints.npy"
    totalwavepropagation = []
    for worms in range(0,wormcount):
        wormwavepropagation = []
        table = np.load(foldername,allow_pickle=True)[worms]
        for iframes in range(0,len(table)-1):
            if (table[iframes] == table[iframes + 1]).all():
                wavemovement = 0
            else:
                wavemovement = 1
            wormwavepropagation.append(wavemovement)
        totalwavepropagation.append(wormwavepropagation)    
    totalwavepropagationname = str(folder) + "/skeletons/totalwavepropagation.npy"
    np.save(totalwavepropagationname, totalwavepropagation, allow_pickle=True)
    print("Wave propagation done!")







#Normal movement

def movement(folder):
    foldername = str(folder) + "/skeletons/*table.npy"
    totalmovement = []
    for worms in range(0,len(glob.glob(foldername))):
        skel = np.load(glob.glob(foldername)[worms],allow_pickle=True)
        thiswormmovement = []
        for frames in range(0,len(skel)-10):
            thisskel = skel[frames]
            thisindex = int(len(thisskel)/2) - 1
            thiscentre = thisskel[thisindex]
            
            nextskel = skel[frames + 10]
            nextindex = int(len(nextskel)/2) - 1
            nextcentre = nextskel[nextindex]

            movement = round(math.dist(thiscentre,nextcentre),2)

            thiswormmovement.append(movement)
        totalmovement.append(thiswormmovement)
    totalmovementname = str(folder) + "/skeletons/totalmovement.npy"
    np.save(totalmovementname,totalmovement,allow_pickle=True)
    print("Movement done!")


def movementdistance(folder):
    global pixelsize
    vectorname = str(folder) + "/skeletons/totalmovement.npy"
    vector = np.load(vectorname,allow_pickle=True)
    totalmovementdistance = []
    for worms in range(0,len(vector)):
        thiswormmovementdistance = []
        for frames in range(0,len(vector[worms])):
            value = round(pixelsize*vector[worms][frames],2)
            thiswormmovementdistance.append(value)
        totalmovementdistance.append(thiswormmovementdistance)
    totalmovementdistancename = str(folder) + "/skeletons/totalmovementdistance.npy"
    np.save(totalmovementdistancename,totalmovementdistance,allow_pickle=True)

def movementspeed(folder):
    global pixelsize
    global frametime
    vectorname = str(folder) + "/skeletons/totalmovement.npy"
    vector = np.load(vectorname,allow_pickle=True)
    totalmovementspeed = []
    for worms in range(0,len(vector)):
        thiswormmovementspeed = []
        for frames in range(0,len(vector[worms])):
            value = round((pixelsize*vector[worms][frames])/(frametime*10),2)
            thiswormmovementspeed.append(value)
        totalmovementspeed.append(thiswormmovementspeed)
    totalmovementspeedname = str(folder) + "/skeletons/totalmovementspeed.npy"
    np.save(totalmovementspeedname,totalmovementspeed,allow_pickle=True)



def activity(folder):
#This is a way better measure than anything involving waviness, as this still works if the worms are diseased and not wavey. 
#Maybe need to give this a loading bar? 
    print("hi")
    totalactivity = []
    for worms in range(0,wormcount):
        imagesname = str(folder) + "/" + str(worms) + "/*.png"
        thiswormactivity = []
        for images in range(0,len(glob.glob(imagesname))-4):
            print(images)
            thispic0 = glob.glob(imagesname)[images + 0]
            thispic1 = glob.glob(imagesname)[images + 1]
            thispic2 = glob.glob(imagesname)[images + 2]
            thispic3 = glob.glob(imagesname)[images + 3]
            thispic4 = glob.glob(imagesname)[images + 4]


            newpic0 = cv2.add(cv2.imread(thispic0),cv2.imread(thispic1),cv2.imread(thispic2))
            newpic1 = cv2.add(cv2.imread(thispic3),cv2.imread(thispic4))
            newpic = cv2.add(newpic0,newpic1)


            imgray = cv2.cvtColor(newpic, cv2.COLOR_BGR2GRAY)
            #Looks at image contrast, gives threshold value for contour
            ret, thresh = cv2.threshold(imgray,127,255,0)
            #Lists contours
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


            imgray1 = cv2.cvtColor(cv2.imread(thispic0), cv2.COLOR_BGR2GRAY)
            #Looks at image contrast, gives threshold value for contour
            ret1, thresh1 = cv2.threshold(imgray1,127,255,0)
            #Lists contours
            contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            if cv2.contourArea(contours1[0]) != 0:
                activityindex = round(cv2.contourArea(contours[0])/cv2.contourArea(contours1[0]) - 1,2)

            if cv2.contourArea(contours1[0]) == 0:
                activityindex = 0

            if activityindex > 2:
                activityindex = 2

            thiswormactivity.append(activityindex)
        totalactivity.append(thiswormactivity)
    totalactivityname = str(folder) + "/skeletons/totalactivity.npy"
    np.save(totalactivityname, totalactivity, allow_pickle=True)
    print("Activity done!")


    
def save(folder,switches):
    #Save a file per worm, with all info
    foldername = str(folder) + "/skeletons/"

    curling = np.load(foldername + "frameset.npy",allow_pickle=True)
    wavenumber = np.load(foldername + "totalwavenumber.npy",allow_pickle=True)
    asymmetry = np.load(foldername + "totalasymmetry.npy",allow_pickle=True)
    bend = np.load(foldername + "totalbend.npy",allow_pickle=True)
    stretch = np.load(foldername + "totalstretch.npy",allow_pickle=True)
    activity = np.load(foldername + "totalactivity.npy",allow_pickle=True)
    movement = np.load(foldername + "totalmovement.npy",allow_pickle=True)

    for worms in range(0,wormcount):

        newactivity = activity[worms]
        newactivity = np.append(newactivity,("NA","NA","NA","NA"))

        newmovement = movement[worms]
        remove = 10*switches
        ind = np.argpartition(newmovement, -remove)[-remove:]
        
        newmovement = list(newmovement)

        for i in range(0,len(ind)):
            index = int(ind[i])
            newmovement[index] = "NA"
    
        newmovement = np.append(newmovement,("NA","NA","NA","NA","NA","NA","NA","NA","NA","NA"))



        dataset = pd.DataFrame({'Curling': curling[worms], 'Wavenumber': wavenumber[worms], 'Asymmetry' : asymmetry[worms], 'Bend' : bend[worms], 'Stretch' : stretch[worms], 'Activity' : newactivity, 'Movement' : newmovement}, columns=['Curling', 'Wavenumber', 'Asymmetry','Bend','Stretch','Activity','Movement'])
        
        if os.path.isdir(str(folder) + "/results") == False:
            os.mkdir(str(folder) + "/results")

        savename = str(folder) + "/results/" + str(worms) + ".csv"
        dataset.to_csv(savename)


    #Save a file with all worms, averages for each measure 
        
    
    curlingvector = np.load(foldername + "percentset.npy") 

    wavenumbervector = []
    for worms in range(0,wormcount):
        value = round(sum(wavenumber[worms])/len(wavenumber[worms]),2)
        wavenumbervector.append(value)

    asymmetryvector = []
    for worms in range(0,wormcount):
        value = round(sum(asymmetry[worms])/len(asymmetry[worms]),2)
        asymmetryvector.append(value)

    bendvector = []
    for worms in range(0,wormcount):
        value = round(sum(bend[worms])/len(bend[worms]),2)
        bendvector.append(value)

    maxbendvector = []
    for worms in range(0,wormcount):
        value = round(np.max(bend[worms]),2)
        maxbendvector.append(value)

    stretchvector = []
    for worms in range(0,wormcount):
        value = round(sum(stretch[worms])/len(stretch[worms]),2)
        stretchvector.append(value)

    maxstretchvector = []
    for worms in range(0,wormcount):
        value = round(np.max(stretch[worms]),2)
        print(value)
        maxstretchvector.append(value)


    activityvector = []
    for worms in range(0,wormcount):
        value = round(sum(activity[worms])/len(activity[worms]),2)
        activityvector.append(value)

    movementvector = []
    for worms in range(0,wormcount):
        remove = 10*switches
        ind = np.argpartition(movement[worms], -remove)[-remove:]
        wormmovement = movement[worms]

        for i in range(0,len(ind)):
            index = int(ind[i])
            wormmovement[index] = 0
        value = round(sum(wormmovement)/(len(movement[worms])-len(ind)),2)
        movementvector.append(value)



    totalset = pd.DataFrame({'Curling': curlingvector, 'Wavenumber': wavenumbervector, 'Asymmetry' : asymmetryvector, 'Bend' : bendvector,'Maximum bend' : maxbendvector, 'Stretch' : stretchvector, 'Maximum stretch' : maxstretchvector, 'Activity' : activityvector, 'Movement' : movementvector}, columns=['Curling', 'Wavenumber', 'Asymmetry','Bend','Maximum bend', 'Stretch','Maximum stretch','Activity','Movement'])
    savename2 = str(folder) + "/results/total.csv"
    totalset.to_csv(savename2)
