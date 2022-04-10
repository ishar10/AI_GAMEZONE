
def puzzle1():
    import time

    import cv2
    from cvzone.HandTrackingModule import HandDetector
    import cvzone
    import os
    import pyttsx3

    # 1.5.0 8.7.1
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8)
    rectangle_coordinates = []
    ppath1 = "images/image_part_001.jpg"
    ppath2 = "images/image_part_002.jpg"
    ppath3 = "images/image_part_003.jpg"
    ppath4 = "images/image_part_004.jpg"
    ppath5 = "images/image_part_005.jpg"
    ppath6 = "images/image_part_006.jpg"
    ppath7 = "images/image_part_007.jpg"
    ppath8 = "images/image_part_008.jpg"
    ppath9 = "images/image_part_009.jpg"
    ox, oy = 500, 200
    w, h = 100, 100

    class DragImg():
        def __init__(self, path, posOrigin, fl):

            self.posOrigin = posOrigin

            self.path = path
            self.img = cv2.imread(self.path)
            self.fl = fl

            # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)

            self.size = self.img.shape[:2]

        def update(self, cursor, j, dict, flag):
            if flag == 0:
                ox, oy = self.posOrigin
                h, w = self.size
                self.fl = flag

                # Check if in region
                if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                    self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
                    dict[j] = self.posOrigin
                    if dict[0][0] < dict[1][0] < dict[2][0] and dict[3][0] < dict[4][0] < dict[5][0] and dict[6][0] < \
                            dict[7][0] < dict[8][0] and dict[0][1] < dict[3][1] < dict[6][1] and dict[1][1] < dict[4][
                        1] < dict[7][1] and dict[2][1] < dict[5][1] < dict[8][1] and (dict[0][0] + w // 2) > dict[3][
                        0] and (dict[3][0] + w // 2) > dict[6][0] and (dict[6][0] + w // 2) > dict[3][0] and (
                            dict[2][0] + w // 2) < (dict[5][0] + w) and (dict[5][0] + w // 2) < (dict[8][0] + w) and (
                            dict[8][0] + w // 2) < (dict[5][0] + w):
                        return 1
            else:
                self.posOrigin = cursor[0], cursor[1]
                self.fl = 1
            return 0

    imagepath = "images"
    mylist = os.listdir(imagepath)

    listImg = []

    dict = {}
    for x, pathImg in enumerate(mylist):
        if x % 2 == 0:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [300 + x * 110, 200], 0))
            dict[x] = [300 + x * 110, 200]


        else:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [110, x * 70], 0))
            dict[x] = [110, x * 70]

    final = {0: [500, 100], 1: [600, 100], 2: [700, 100], 3: [500, 200], 4: [600, 200], 5: [700, 200], 6: [500, 300],
             7: [600, 300], 8: [700, 300]}
    t = 0
    ok = 1
    count = 0
    count2 = 0
    strr = ""
    minutes=1
    text_speech = pyttsx3.init()
    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        if ok == 1:
            strr = "Time taken- " + str(count) + "secs"
            cv2.putText(img, strr, (100, 50), cv2.FONT_ITALIC, 2, (0, 255, 0), 4)
            if count%60==0 and count>=60:
                print(count)

                text = str(minutes)+"minutes passed!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                minutes+=1
                count+=1
            if count2 > 30:
                count += 1
                count2 = 0
            count2 += 1
        img1 = cv2.imread(ppath1)
        img2 = cv2.imread(ppath2)
        img3 = cv2.imread(ppath3)
        img4 = cv2.imread(ppath4)
        img5 = cv2.imread(ppath5)
        img6 = cv2.imread(ppath6)
        img7 = cv2.imread(ppath7)
        img8 = cv2.imread(ppath8)
        img9 = cv2.imread(ppath9)
        # module 1.5.0 k hissab se
        # hands, img = detector.findHands(img, flipType=False) #
        # if hands:
        #     lmlist=hands[0]['lmList']
        #     length,info,img=detector.findDistance(lmlist[8],lmlist[12],img)
        #     if length<60:
        #         cursor=lmlist[8]
        #         for j,imgObject in enumerate(listImg):
        #             if t==0:
        #                 t=imgObject.update(cursor,j,dict,0)
        #             else:
        #                 imgObject.update(final,j,dict,1)
        #                 ok=0
        img = detector.findHands(img)
        lmlist, _ = detector.findPosition(img)
        if lmlist:

            length, img, _ = detector.findDistance(8, 12, img)
            if length < 60:
                cursor = lmlist[8]
                for j, imgObject in enumerate(listImg):
                    if t == 0:
                        t = imgObject.update(cursor, j, dict, 0)
                    else:
                        imgObject.update(final, j, dict, 1)
                        ok = 0

        if ok == 0:
            img[100:200, 500:600] = img1
            img[100:200, 600:700] = img2
            img[100:200, 700:800] = img3
            img[200:300, 500:600] = img4
            img[200:300, 600:700] = img5
            img[200:300, 700:800] = img6
            img[300:400, 500:600] = img7
            img[300:400, 600:700] = img8
            img[300:400, 700:800] = img9
            cv2.putText(img, "SOLVED!" + " " + strr, (300, 500), cv2.FONT_ITALIC, 2, (0, 255, 255), 4)


        # cv2.rectangle(img,(100,100),(200,200),(0,0,0))
        # cv2.rectangle(img, (300, 100), (200, 200), (0, 0, 0))
        # cv2.rectangle(img,(400,100),(200,200),(0,0,0))
        # cv2.rectangle(img,(100,300),(200,200),(0,0,0))
        # cv2.rectangle(img,(300,300),(200,200),(0,0,0))
        # cv2.rectangle(img, (400, 300), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (100, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (300, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (400, 400), (200, 200), (0, 0, 0))

        try:

            for imgObject in listImg:
                h, w = imgObject.size
                ox, oy = imgObject.posOrigin
                fl = imgObject.fl
                if fl == 0:
                    img[oy:oy + h, ox:ox + w] = imgObject.img

        except:
            pass

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def puzzle2():
    import time

    import cv2
    from cvzone.HandTrackingModule import HandDetector
    import cvzone
    import os
    import pyttsx3

    # 1.5.0 8.7.1
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8)
    rectangle_coordinates = []
    ppath1 = "images1/image_part_001.jpg"
    ppath2 = "images1/image_part_002.jpg"
    ppath3 = "images1/image_part_003.jpg"
    ppath4 = "images1/image_part_004.jpg"
    ppath5 = "images1/image_part_005.jpg"
    ppath6 = "images1/image_part_006.jpg"
    ppath7 = "images1/image_part_007.jpg"
    ppath8 = "images1/image_part_008.jpg"
    ppath9 = "images1/image_part_009.jpg"
    ox, oy = 500, 200
    w, h = 100, 100

    class DragImg():
        def __init__(self, path, posOrigin, fl):

            self.posOrigin = posOrigin

            self.path = path
            self.img = cv2.imread(self.path)
            self.fl = fl

            # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)

            self.size = self.img.shape[:2]

        def update(self, cursor, j, dict, flag):
            if flag == 0:
                ox, oy = self.posOrigin
                h, w = self.size
                self.fl = flag

                # Check if in region
                if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                    self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
                    dict[j] = self.posOrigin
                    if dict[0][0] < dict[1][0] < dict[2][0] and dict[3][0] < dict[4][0] < dict[5][0] and dict[6][0] < \
                            dict[7][0] < dict[8][0] and dict[0][1] < dict[3][1] < dict[6][1] and dict[1][1] < dict[4][
                        1] < dict[7][1] and dict[2][1] < dict[5][1] < dict[8][1] and (dict[0][0] + w // 2) > dict[3][
                        0] and (dict[3][0] + w // 2) > dict[6][0] and (dict[6][0] + w // 2) > dict[3][0] and (
                            dict[2][0] + w // 2) < (dict[5][0] + w) and (dict[5][0] + w // 2) < (dict[8][0] + w) and (
                            dict[8][0] + w // 2) < (dict[5][0] + w):
                        return 1
            else:
                self.posOrigin = cursor[0], cursor[1]
                self.fl = 1
            return 0

    imagepath = "images1"
    mylist = os.listdir(imagepath)

    listImg = []

    dict = {}
    for x, pathImg in enumerate(mylist):
        if x % 2 == 0:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [300 + x * 110, 200], 0))
            dict[x] = [300 + x * 110, 200]


        else:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [110, x * 70], 0))
            dict[x] = [110, x * 70]

    final = {0: [500, 100], 1: [600, 100], 2: [700, 100], 3: [500, 200], 4: [600, 200], 5: [700, 200], 6: [500, 300],
             7: [600, 300], 8: [700, 300]}
    t = 0
    ok = 1
    count = 0
    count2 = 0
    strr = ""
    minutes=1
    text_speech = pyttsx3.init()
    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        if ok == 1:
            strr = "Time taken- " + str(count) + "secs"
            cv2.putText(img, strr, (100, 50), cv2.FONT_ITALIC, 2, (0, 255, 0), 4)
            if count%60==0 and count>=60:
                print(count)

                text = str(minutes)+"minutes passed!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                minutes+=1
                count+=1
            if count2 > 30:
                count += 1
                count2 = 0
            count2 += 1
        img1 = cv2.imread(ppath1)
        img2 = cv2.imread(ppath2)
        img3 = cv2.imread(ppath3)
        img4 = cv2.imread(ppath4)
        img5 = cv2.imread(ppath5)
        img6 = cv2.imread(ppath6)
        img7 = cv2.imread(ppath7)
        img8 = cv2.imread(ppath8)
        img9 = cv2.imread(ppath9)
        # module 1.5.0 k hissab se
        # hands, img = detector.findHands(img, flipType=False) #
        # if hands:
        #     lmlist=hands[0]['lmList']
        #     length,info,img=detector.findDistance(lmlist[8],lmlist[12],img)
        #     if length<60:
        #         cursor=lmlist[8]
        #         for j,imgObject in enumerate(listImg):
        #             if t==0:
        #                 t=imgObject.update(cursor,j,dict,0)
        #             else:
        #                 imgObject.update(final,j,dict,1)
        #                 ok=0
        img = detector.findHands(img)
        lmlist, _ = detector.findPosition(img)
        if lmlist:

            length, img, _ = detector.findDistance(8, 12, img)
            if length < 60:
                cursor = lmlist[8]
                for j, imgObject in enumerate(listImg):
                    if t == 0:
                        t = imgObject.update(cursor, j, dict, 0)
                    else:
                        imgObject.update(final, j, dict, 1)
                        ok = 0

        if ok == 0:
            img[100:200, 500:600] = img1
            img[100:200, 600:700] = img2
            img[100:200, 700:800] = img3
            img[200:300, 500:600] = img4
            img[200:300, 600:700] = img5
            img[200:300, 700:800] = img6
            img[300:400, 500:600] = img7
            img[300:400, 600:700] = img8
            img[300:400, 700:800] = img9
            cv2.putText(img, "SOLVED!" + " " + strr, (300, 500), cv2.FONT_ITALIC, 2, (0, 255, 255), 4)


        # cv2.rectangle(img,(100,100),(200,200),(0,0,0))
        # cv2.rectangle(img, (300, 100), (200, 200), (0, 0, 0))
        # cv2.rectangle(img,(400,100),(200,200),(0,0,0))
        # cv2.rectangle(img,(100,300),(200,200),(0,0,0))
        # cv2.rectangle(img,(300,300),(200,200),(0,0,0))
        # cv2.rectangle(img, (400, 300), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (100, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (300, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (400, 400), (200, 200), (0, 0, 0))

        try:

            for imgObject in listImg:
                h, w = imgObject.size
                ox, oy = imgObject.posOrigin
                fl = imgObject.fl
                if fl == 0:
                    img[oy:oy + h, ox:ox + w] = imgObject.img

        except:
            pass

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def puzzle3():
    import time

    import cv2
    from cvzone.HandTrackingModule import HandDetector
    import cvzone
    import os
    import pyttsx3

    # 1.5.0 8.7.1
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    detector = HandDetector(detectionCon=0.8)
    rectangle_coordinates = []
    ppath1 = "images2/image_part_001.jpg"
    ppath2 = "images2/image_part_002.jpg"
    ppath3 = "images2/image_part_003.jpg"
    ppath4 = "images2/image_part_004.jpg"
    ppath5 = "images2/image_part_005.jpg"
    ppath6 = "images2/image_part_006.jpg"
    ppath7 = "images2/image_part_007.jpg"
    ppath8 = "images2/image_part_008.jpg"
    ppath9 = "images2/image_part_009.jpg"
    ox, oy = 500, 200
    w, h = 100, 100

    class DragImg():
        def __init__(self, path, posOrigin, fl):

            self.posOrigin = posOrigin

            self.path = path
            self.img = cv2.imread(self.path)
            self.fl = fl

            # self.img = cv2.resize(self.img, (0,0),None,0.4,0.4)

            self.size = self.img.shape[:2]

        def update(self, cursor, j, dict, flag):
            if flag == 0:
                ox, oy = self.posOrigin
                h, w = self.size
                self.fl = flag

                # Check if in region
                if ox < cursor[0] < ox + w and oy < cursor[1] < oy + h:
                    self.posOrigin = cursor[0] - w // 2, cursor[1] - h // 2
                    dict[j] = self.posOrigin
                    if dict[0][0] < dict[1][0] < dict[2][0] and dict[3][0] < dict[4][0] < dict[5][0] and dict[6][0] < \
                            dict[7][0] < dict[8][0] and dict[0][1] < dict[3][1] < dict[6][1] and dict[1][1] < dict[4][
                        1] < dict[7][1] and dict[2][1] < dict[5][1] < dict[8][1] and (dict[0][0] + w // 2) > dict[3][
                        0] and (dict[3][0] + w // 2) > dict[6][0] and (dict[6][0] + w // 2) > dict[3][0] and (
                            dict[2][0] + w // 2) < (dict[5][0] + w) and (dict[5][0] + w // 2) < (dict[8][0] + w) and (
                            dict[8][0] + w // 2) < (dict[5][0] + w):
                        return 1
            else:
                self.posOrigin = cursor[0], cursor[1]
                self.fl = 1
            return 0

    imagepath = "images2"
    mylist = os.listdir(imagepath)

    listImg = []

    dict = {}
    for x, pathImg in enumerate(mylist):
        if x % 2 == 0:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [300 + x * 110, 200], 0))
            dict[x] = [300 + x * 110, 200]


        else:
            listImg.append(DragImg(f'{imagepath}/{pathImg}', [110, x * 70], 0))
            dict[x] = [110, x * 70]

    final = {0: [500, 100], 1: [600, 100], 2: [700, 100], 3: [500, 200], 4: [600, 200], 5: [700, 200], 6: [500, 300],
             7: [600, 300], 8: [700, 300]}
    t = 0
    ok = 1
    count = 0
    count2 = 0
    strr = ""
    minutes=1
    text_speech = pyttsx3.init()
    while True:

        success, img = cap.read()
        img = cv2.flip(img, 1)
        if ok == 1:
            strr = "Time taken- " + str(count) + "secs"
            cv2.putText(img, strr, (100, 50), cv2.FONT_ITALIC, 2, (0, 255, 0), 4)
            if count%60==0 and count>=60:
                print(count)

                text = str(minutes)+"minutes passed!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                minutes+=1
                count+=1
            if count2 > 30:
                count += 1
                count2 = 0
            count2 += 1
        img1 = cv2.imread(ppath1)
        img2 = cv2.imread(ppath2)
        img3 = cv2.imread(ppath3)
        img4 = cv2.imread(ppath4)
        img5 = cv2.imread(ppath5)
        img6 = cv2.imread(ppath6)
        img7 = cv2.imread(ppath7)
        img8 = cv2.imread(ppath8)
        img9 = cv2.imread(ppath9)
        # module 1.5.0 k hissab se
        # hands, img = detector.findHands(img, flipType=False) #
        # if hands:
        #     lmlist=hands[0]['lmList']
        #     length,info,img=detector.findDistance(lmlist[8],lmlist[12],img)
        #     if length<60:
        #         cursor=lmlist[8]
        #         for j,imgObject in enumerate(listImg):
        #             if t==0:
        #                 t=imgObject.update(cursor,j,dict,0)
        #             else:
        #                 imgObject.update(final,j,dict,1)
        #                 ok=0
        img = detector.findHands(img)
        lmlist, _ = detector.findPosition(img)
        if lmlist:

            length, img, _ = detector.findDistance(8, 12, img)
            if length < 60:
                cursor = lmlist[8]
                for j, imgObject in enumerate(listImg):
                    if t == 0:
                        t = imgObject.update(cursor, j, dict, 0)
                    else:
                        imgObject.update(final, j, dict, 1)
                        ok = 0

        if ok == 0:
            img[100:186, 500:586] = img1
            img[100:186, 586:673] = img2
            img[100:186, 672:758] = img3
            img[186:273, 500:586] = img4
            img[186:273, 586:673] = img5
            img[186:273, 672:758] = img6
            img[272:358, 500:586] = img7
            img[272:358, 586:673] = img8
            img[272:358, 672:758] = img9
            cv2.putText(img, "SOLVED!" + " " + strr, (300, 500), cv2.FONT_ITALIC, 2, (0, 255, 255), 4)


        # cv2.rectangle(img,(100,100),(200,200),(0,0,0))
        # cv2.rectangle(img, (300, 100), (200, 200), (0, 0, 0))
        # cv2.rectangle(img,(400,100),(200,200),(0,0,0))
        # cv2.rectangle(img,(100,300),(200,200),(0,0,0))
        # cv2.rectangle(img,(300,300),(200,200),(0,0,0))
        # cv2.rectangle(img, (400, 300), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (100, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (300, 400), (200, 200), (0, 0, 0))
        # cv2.rectangle(img, (400, 400), (200, 200), (0, 0, 0))

        try:

            for imgObject in listImg:
                h, w = imgObject.size
                ox, oy = imgObject.posOrigin
                fl = imgObject.fl
                if fl == 0:
                    img[oy:oy + h, ox:ox + w] = imgObject.img

        except:
            pass

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
