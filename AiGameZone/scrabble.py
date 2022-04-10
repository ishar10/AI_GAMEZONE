def scrabble():
    import cv2
    import numpy as np
    import time
    import os
    import pyttsx3
    from cvzone.HandTrackingModule import HandDetector
    import random

    brushthickness=15

    folderpath="header"
    mylist=os.listdir(folderpath)
    # print(mylist)
    overlaylist=[]
    for imagepath in mylist:
        img=cv2.imread(f'{folderpath}/{imagepath}')
        overlaylist.append(img)
    # print(len(overlaylist))
    # print(overlaylist)
    header=overlaylist[0]
    drawcolor=(0,0,255)

    cap=cv2.VideoCapture(0)
    cap.set(3,1275)
    cap.set(4,720)
    detector=HandDetector(detectionCon=0.85)
    xp,yp=0,0

    imgcanvas=np.zeros((720,1280,3),np.uint8)

    t = 0
    ok = 1
    count = 0
    count2 = 0
    strr = ""
    text_speech = pyttsx3.init()
    ok=1
    k=1
    l=["sun","car","doll","house","mountain"]
    ans=random.randint(-1,len(l))
    while True:
        success,img=cap.read()
        img=cv2.flip(img,1)
        if count<30:
            strr = "Time taken- " + str(count) + "secs"
            cv2.putText(img, strr, (100, 250), cv2.FONT_ITALIC, 2, (0, 255, 0), 4)
            if count % 60 == 0 and count >= 60:
                print(count)
                count += 1
            if count2 > 30:
                count += 1
                count2 = 0
            count2 += 1
        elif count>=30:
            if k==1:
                text = "Times up! Game over!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                ok=0
                k=0
            else:
                cv2.putText(img, "The correct ans is "+l[ans], (100, 250), cv2.FONT_ITALIC, 2, (0, 255, 0), 4)


        img=detector.findHands(img)
        lmlist,bbox=detector.findPosition(img,draw=False)
        if len(lmlist)!=0 and ok==1:

            #print(lmlist[8])
            x1,y1=lmlist[8]
            x2,y2=lmlist[12]

            fin=detector.fingersUp()
            #print(fin)
            if fin[1] and fin[2]:
                xp, yp = 0, 0

                if y1<167:
                    if 50<x1<200:
                        header=overlaylist[0]
                        drawcolor=(0,0,255)
                    elif 300<x1<500:
                        header=overlaylist[1]
                        drawcolor=(0,255,0)
                    elif 700<x1<900:
                        header=overlaylist[2]
                        drawcolor = (255, 0, 255)
                    elif 1050<x1<1200:
                        header=overlaylist[3]
                        drawcolor = (0, 0, 0)
                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)
                if count<5:
                    cv2.putText(img, "draw "+l[ans], (200, 425), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

                print("selection mode")
            if fin[1] and fin[2]==False:


                cv2.circle(img,(x1,y1),15,drawcolor,cv2.FILLED)
                print("drawing mode")
                if xp==0 and yp==0:
                    xp,yp=x1,y1
                if drawcolor==(0,0,0):
                    brushthickness=50
                else:
                    brushthickness=15
                cv2.line(img,(xp,yp),(x1,y1),drawcolor,brushthickness)
                cv2.line(imgcanvas, (xp, yp), (x1, y1), drawcolor, brushthickness)
                xp,yp=x1,y1


        img=detector.findHands(img)
        imggray=cv2.cvtColor(imgcanvas,cv2.COLOR_BGR2GRAY)
        _,imginv=cv2.threshold(imggray,50,255,cv2.THRESH_BINARY_INV)
        imginv=cv2.cvtColor(imginv,cv2.COLOR_GRAY2BGR)
        img=cv2.bitwise_and(img,imginv)
        img=cv2.bitwise_or(img,imgcanvas)


        img[0:167,0:1275]=header
        #print(img.shape,imgcanvas.shape)
        img=cv2.addWeighted(img,0.5,imgcanvas,0.5,0)
        cv2.imshow("image",img)
        # cv2.imshow("imagecanvas",imgcanvas)
        cv2.waitKey(1)
