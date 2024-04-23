import numpy as np
import cv2
import matplotlib.pyplot as plt
import pandas as pd
import os
import math
import glob

resolution = 1024
outputdirectory = "C:/Users/jhepw/Documents/Project/Processed/"

def find_ends(linetrans):
    ends = []
    #Creates empty vector to store the ends of the worm
    for irow in range(0,len(linetrans)):
        samey = linetrans[irow][0]
        samex = linetrans[irow][1]
        plus1y = samey + 1
        minus1y = samey - 1
        plus1x = samex + 1
        minus1x = samex - 1

        #Possible next positions for the skeleton
        a = np.array([samey,plus1x])
        b = np.array([samey,minus1x])
        c = np.array([plus1y,samex])
        d = np.array([plus1y,plus1x])
        e = np.array([plus1y,minus1x])
        f = np.array([minus1y,samex])
        g = np.array([minus1y,plus1x])
        h = np.array([minus1y,minus1x])

        #Counts how many of these next positions are filled
        count = 0
        for istep in (a,b,c,d,e,f,g,h):
            if np.isin(linetrans,istep).all(1).any() == True:
                count = count + 1
        #If only one of these next positions is filled, then we are at the end of the worm
        if count < 2:
            ends.append([samey,samex])


    return(ends)



def ordered_line(lastend, ends, linetrans):
    print(str(len(ends)) + " ends")
    print(ends)

    if len(ends) > 3:
        #Need something here as may be curling and still have 2 ends.
        numends = 4
        
        #Extracts start coordinate from the first end
        if len(lastend) != 0:
            ygap0 = abs(ends[0][0] - lastend[0])
            xgap0 = abs(ends[0][1] - lastend[1])
            ygap1 = abs(ends[1][0] - lastend[0])
            xgap1 = abs(ends[1][1] - lastend[1])
            ygap2 = abs(ends[2][0] - lastend[0])
            xgap2 = abs(ends[2][1] - lastend[1])
            ygap3 = abs(ends[3][0] - lastend[0])
            xgap3 = abs(ends[3][1] - lastend[1])


            gap0 = ygap0 + xgap0
            gap1 = ygap1 + xgap1
            gap2 = ygap2 + xgap2
            gap3 = ygap3 + xgap3

            if gap0 < gap1 and gap0 < gap2 and gap0 < gap3:
                starty = ends[0][0]
                startx = ends[0][1]

            if gap1 < gap0 and gap1 < gap2 and gap1 < gap3:
                starty = ends[1][0]
                startx = ends[1][1]

            if gap2 < gap0 and gap2 < gap1 and gap2 < gap3:
                starty = ends[2][0]
                startx = ends[2][1]  

            if gap3 < gap0 and gap3 < gap1 and gap3 < gap2:
                starty = ends[3][0]
                startx = ends[3][1]

            else:
                starty = ends[0][0]
                startx = ends[0][1]  
    
        else:
            starty = ends[0][0]
            startx = ends[0][1]
    
        startstep = np.array([starty,startx])

        lastend = startstep

        #Creates array, and then dataframe containing all the possible steps that could have been taken, updates later
        donesteps = [startstep]

        #Creates array, and then dataframe containing all the steps that were taken, updates later
        finalsteps = [startstep]

        #For every pixel in the skeleton, computes potential steps
        for irow in range(0,len(linetrans)):
            plus1y = starty + 1
            minus1y = starty - 1
            plus1x = startx + 1
            minus1x = startx - 1

            #Defines potential steps, order of abc etc defines whether we see more diagnoalised or straight pixel jumps.
            #This order uses diagonal jumps first
            h = np.array([starty,plus1x])
            e = np.array([starty,minus1x])
            g = np.array([plus1y,startx])
            a = np.array([plus1y,plus1x])
            b = np.array([plus1y,minus1x])
            f = np.array([minus1y,startx])
            c = np.array([minus1y,plus1x])
            d = np.array([minus1y,minus1x])


            #Count variable to ensure only one step made per pixel
            count = 0
            #For potential steps, checks if it is in the donetable, ensuring no backwards steps
            #If the step is not in the done table, adds it to the finaltable, and updates start position, increases count to 1, move on to next position.
            for istep in (a,b,c,d,e,f,g,h):
                if(linetrans == istep).all(1).any() == True:
                    if(donesteps == istep).all(1).any() == False:
                        donesteps.append(istep) 
                        if count == 0:
                            finalsteps.append(istep)
                            starty = istep[0]
                            startx = istep[1]
                            count = 1


    if len(ends) == 3:
        #Need something here as may be curling and still have 2 ends.
        numends = 3
        
        #Extracts start coordinate from the first end
        if len(lastend) != 0:
            ygap0 = abs(ends[0][0] - lastend[0])
            xgap0 = abs(ends[0][1] - lastend[1])
            ygap1 = abs(ends[1][0] - lastend[0])
            xgap1 = abs(ends[1][1] - lastend[1])
            ygap2 = abs(ends[2][0] - lastend[0])
            xgap2 = abs(ends[2][1] - lastend[1])

            gap0 = ygap0 + xgap0
            gap1 = ygap1 + xgap1
            gap2 = ygap2 + xgap2

            if gap0 < gap1 and gap0 < gap2:
                starty = ends[0][0]
                startx = ends[0][1]

            if gap1 < gap0 and gap1 < gap2:
                starty = ends[1][0]
                startx = ends[1][1]

            if gap2 < gap0 and gap2 < gap1:
                starty = ends[2][0]
                startx = ends[2][1]
            else:
                starty = ends[0][0]
                startx = ends[0][1]
    
        else:
            starty = ends[0][0]
            startx = ends[0][1]
    
        startstep = np.array([starty,startx])

        lastend = startstep

        #Creates array, and then dataframe containing all the possible steps that could have been taken, updates later
        donesteps = [startstep]

        #Creates array, and then dataframe containing all the steps that were taken, updates later
        finalsteps = [startstep]

        #For every pixel in the skeleton, computes potential steps
        for irow in range(0,len(linetrans)):
            plus1y = starty + 1
            minus1y = starty - 1
            plus1x = startx + 1
            minus1x = startx - 1

            #Defines potential steps, order of abc etc defines whether we see more diagnoalised or straight pixel jumps.
            #This order uses diagonal jumps first
            h = np.array([starty,plus1x])
            e = np.array([starty,minus1x])
            g = np.array([plus1y,startx])
            a = np.array([plus1y,plus1x])
            b = np.array([plus1y,minus1x])
            f = np.array([minus1y,startx])
            c = np.array([minus1y,plus1x])
            d = np.array([minus1y,minus1x])


            #Count variable to ensure only one step made per pixel
            count = 0
            #For potential steps, checks if it is in the donetable, ensuring no backwards steps
            #If the step is not in the done table, adds it to the finaltable, and updates start position, increases count to 1, move on to next position.
            for istep in (a,b,c,d,e,f,g,h):
                if(linetrans == istep).all(1).any() == True:
                    if(donesteps == istep).all(1).any() == False:
                        donesteps.append(istep) 
                        if count == 0:
                            finalsteps.append(istep)
                            starty = istep[0]
                            startx = istep[1]
                            count = 1

    if len(ends) == 2:
        #Need something here as may be curling and still have 2 ends.
        numends = 2
        #Extracts start coordinate from the first end
        if len(lastend) != 0:
            ygap0 = abs(ends[0][0] - lastend[0])
            xgap0 = abs(ends[0][1] - lastend[1])
            ygap1 = abs(ends[1][0] - lastend[0])
            xgap1 = abs(ends[1][1] - lastend[1])
            gap0 = ygap0 + xgap0
            gap1 = ygap1 + xgap1

            if gap0 < gap1:
                starty = ends[0][0]
                startx = ends[0][1]

            else:
                starty = ends[1][0]
                startx = ends[1][1]
    
        else:
            starty = ends[0][0]
            startx = ends[0][1]
    
        startstep = np.array([starty,startx])

        lastend = startstep

        #Creates array, and then dataframe containing all the possible steps that could have been taken, updates later
        donesteps = [startstep]

        #Creates array, and then dataframe containing all the steps that were taken, updates later
        finalsteps = [startstep]

        #For every pixel in the skeleton, computes potential steps
        for irow in range(0,len(linetrans)):
            plus1y = starty + 1
            minus1y = starty - 1
            plus1x = startx + 1
            minus1x = startx - 1

            #Defines potential steps, order of abc etc defines whether we see more diagnoalised or straight pixel jumps.
            #This order uses diagonal jumps first
            h = np.array([starty,plus1x])
            e = np.array([starty,minus1x])
            g = np.array([plus1y,startx])
            a = np.array([plus1y,plus1x])
            b = np.array([plus1y,minus1x])
            f = np.array([minus1y,startx])
            c = np.array([minus1y,plus1x])
            d = np.array([minus1y,minus1x])


            #Count variable to ensure only one step made per pixel
            count = 0
            #For potential steps, checks if it is in the donetable, ensuring no backwards steps
            #If the step is not in the done table, adds it to the finaltable, and updates start position, increases count to 1, move on to next position.
            for istep in (a,b,c,d,e,f,g,h):
                if(linetrans == istep).all(1).any() == True:
                    if(donesteps == istep).all(1).any() == False:
                        donesteps.append(istep) 
                        if count == 0:
                            finalsteps.append(istep)
                            starty = istep[0]
                            startx = istep[1]
                            count = 1
    if len(ends) == 1:
        numends = 1
        #Might go the wrong way around the worm in a 6, does this matter? Is there a way to fix it?
        starty = ends[0][0]
        startx = ends[0][1]
    
        startstep = np.array([starty,startx])

        lastend = startstep

        #Creates array, and then dataframe containing all the possible steps that could have been taken, updates later
        donesteps = [startstep]

        #Creates array, and then dataframe containing all the steps that were taken, updates later
        finalsteps = [startstep]

        #For every pixel in the skeleton, computes potential steps
        for irow in range(0,len(linetrans)):
            plus1y = starty + 1
            minus1y = starty - 1
            plus1x = startx + 1
            minus1x = startx - 1

            #Defines potential steps, order of abc etc defines whether we see more diagnoalised or straight pixel jumps.
            #This order uses diagonal jumps first
            h = np.array([starty,plus1x])
            e = np.array([starty,minus1x])
            g = np.array([plus1y,startx])
            a = np.array([plus1y,plus1x])
            b = np.array([plus1y,minus1x])
            f = np.array([minus1y,startx])
            c = np.array([minus1y,plus1x])
            d = np.array([minus1y,minus1x])


            #Count variable to ensure only one step made per pixel
            count = 0
            #For potential steps, checks if it is in the donetable, ensuring no backwards steps
            #If the step is not in the done table, adds it to the finaltable, and updates start position, increases count to 1, move on to next position.
            for istep in (a,b,c,d,e,f,g,h):
                if(linetrans == istep).all(1).any() == True:
                    if(donesteps == istep).all(1).any() == False:
                        donesteps.append(istep) 
                        if count == 0:
                            finalsteps.append(istep)
                            starty = istep[0]
                            startx = istep[1]
                            count = 1
    if len(ends) == 0:
        numends = 0
        #Might go the wrong way around the worm in a 6, does this matter? Is there a way to fix it?
        starty = linetrans[0][0]
        startx = linetrans[0][1]
    
        startstep = np.array([starty,startx])


        lastend = startstep

        #Creates array, and then dataframe containing all the possible steps that could have been taken, updates later
        donesteps = [startstep]

        #Creates array, and then dataframe containing all the steps that were taken, updates later
        finalsteps = [startstep]

        #For every pixel in the skeleton, computes potential steps
        for irow in range(0,len(linetrans)):
            plus1y = starty + 1
            minus1y = starty - 1
            plus1x = startx + 1
            minus1x = startx - 1

            #Defines potential steps, order of abc etc defines whether we see more diagnoalised or straight pixel jumps.
            #This order uses diagonal jumps first
            h = np.array([starty,plus1x])
            e = np.array([starty,minus1x])
            g = np.array([plus1y,startx])
            a = np.array([plus1y,plus1x])
            b = np.array([plus1y,minus1x])
            f = np.array([minus1y,startx])
            c = np.array([minus1y,plus1x])
            d = np.array([minus1y,minus1x])


            #Count variable to ensure only one step made per pixel
            count = 0
            #For potential steps, checks if it is in the donetable, ensuring no backwards steps
            #If the step is not in the done table, adds it to the finaltable, and updates start position, increases count to 1, move on to next position.
            for istep in (a,b,c,d,e,f,g,h):
                if(linetrans == istep).all(1).any() == True:
                    if(donesteps == istep).all(1).any() == False:
                        donesteps.append(istep) 
                        if count == 0:
                            finalsteps.append(istep)
                            starty = istep[0]
                            startx = istep[1]
                            count = 1
    return(lastend,finalsteps)






def makeskeletons(folder,worms,skeletonstatus):
    count = 0
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
    for iworm in range(0,int(worms)):
        foldername = overalloutput + "/" + str(iworm) + "/*.png" 
        table = []
        numendstable = []
        lastend = []
        tablename = overalloutput + "/skeletons/" + str(iworm) + "table" + ".npy"
        numendstablename = overalloutput + "/skeletons/" + str(iworm) + "numends" + ".npy"
        for images in glob.glob(foldername):
            print(images)
            image = cv2.imread(images)
            imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(imgray,127,255,0)
            thinned = cv2.ximgproc.thinning(imgray)
            line = np.nonzero(thinned)
            linetrans = np.transpose(line)
            thispicends = find_ends(linetrans)
            lastend, thispictable = ordered_line(lastend, thispicends, linetrans)
            table.append(thispictable)
            numendstable.append(thispicends)
        
            skeletonstatus(count,1,len(glob.glob(foldername))*worms)
            count = count + 1
        
        table = np.asanyarray(table,dtype=object)
        numendstable = np.asanyarray(numendstable, dtype=object)

        if os.path.isdir(str(overalloutput) + "/skeletons") == False:
            os.mkdir(str(overalloutput) + "/skeletons")

        np.save(tablename, table, allow_pickle=True)
        np.save(numendstablename, numendstable, allow_pickle=True)



