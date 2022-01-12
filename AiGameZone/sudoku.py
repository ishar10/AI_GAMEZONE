def sudoku():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3

    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"], ["9"]]
    # sudoku_keys=[[5,4,0,0,2,0,8,0,6],
    #         [0,1,9,0,0,7,0,0,3],
    #         [0,0,0,3,0,0,2,1,0],
    #         [9,0,0,4,0,5,0,2,0],
    #         [0,0,1,0,0,0,6,0,4],
    #         [6,0,4,0,3,2,0,8,0],
    #         [0,6,0,0,0,0,1,9,0],
    #         [4,0,2,0,0,9,0,0,5],
    #         [0,9,0,0,7,0,4,0,2]]
    sudoku_keys = [[0, 4, 3, 9, 2, 1, 8, 7, 6],
                   [2, 1, 9, 6, 8, 7, 5, 4, 3],
                   [8, 7, 6, 3, 5, 4, 2, 1, 9],
                   [9, 8, 7, 0, 6, 5, 3, 2, 1],
                   [3, 2, 1, 7, 9, 8, 6, 5, 4],
                   [6, 5, 4, 1, 3, 2, 9, 8, 7],
                   [7, 0, 5, 2, 4, 3, 1, 9, 8],
                   [4, 3, 2, 8, 1, 9, 7, 6, 5],
                   [1, 9, 8, 5, 7, 6, 4, 3, 2]]

    result = [[5, 4, 3, 9, 2, 1, 8, 7, 6],
              [2, 1, 9, 6, 8, 7, 5, 4, 3],
              [8, 7, 6, 3, 5, 4, 2, 1, 9],
              [9, 8, 7, 4, 6, 5, 3, 2, 1],
              [3, 2, 1, 7, 9, 8, 6, 5, 4],
              [6, 5, 4, 1, 3, 2, 9, 8, 7],
              [7, 6, 5, 2, 4, 3, 1, 9, 8],
              [4, 3, 2, 8, 1, 9, 7, 6, 5],
              [1, 9, 8, 5, 7, 6, 4, 3, 2]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            cv2.putText(img, button.text, (button.pos[0] + 10, button.pos[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 4)
            if color==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
        return img

    class button():
        def __init__(self, pos, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0], key))
    for i in range(9):
        for j, key in enumerate(sudoku_keys[i]):
            if key != 0:
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))

    placing_text = ""
    ok = 1
    okk = 1
    b = []
    for i in range(9):
        for j, key in enumerate(result[i]):
            if key != 0:
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        color = button.color
                        id = button.id
                        if color == (0, 0, 255):  # red
                            button.text = placing_text
                            button.color = (255, 0, 0)
                            print(sudoku_keys)

                            if placing_text != "":
                                print("placing")
                                sudoku_keys[id[0]][id[1]] = int(placing_text)

                            print(sudoku_keys)
                            print(result)


                        elif color == (255, 0, 255):  # pink
                            placing_text = button.text

                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif color == (255, 0, 0):
                            button.color = (0, 0, 255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations! You solved the game!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Game over! These are the answers!!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def sudoku_color():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3
    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"], ["9"]]
    # sudoku_keys=[[5,4,0,0,2,0,8,0,6],
    #         [0,1,9,0,0,7,0,0,3],
    #         [0,0,0,3,0,0,2,1,0],
    #         [9,0,0,4,0,5,0,2,0],
    #         [0,0,1,0,0,0,6,0,4],
    #         [6,0,4,0,3,2,0,8,0],
    #         [0,6,0,0,0,0,1,9,0],
    #         [4,0,2,0,0,9,0,0,5],
    #         [0,9,0,0,7,0,4,0,2]]
    sudoku_keys = [[0, 4, 3, 9, 2, 1, 8, 7, 6],
                   [2, 1, 9, 6, 8, 7, 5, 4, 3],
                   [8, 7, 6, 3, 5, 4, 2, 1, 9],
                   [9, 8, 7, 0, 6, 5, 3, 2, 1],
                   [3, 2, 1, 7, 9, 8, 6, 5, 4],
                   [6, 5, 4, 1, 3, 2, 9, 8, 7],
                   [7, 0, 5, 2, 4, 3, 1, 9, 8],
                   [4, 3, 2, 8, 1, 9, 7, 6, 5],
                   [1, 9, 8, 5, 7, 6, 4, 3, 2]]

    result = [[5, 4, 3, 9, 2, 1, 8, 7, 6],
              [2, 1, 9, 6, 8, 7, 5, 4, 3],
              [8, 7, 6, 3, 5, 4, 2, 1, 9],
              [9, 8, 7, 4, 6, 5, 3, 2, 1],
              [3, 2, 1, 7, 9, 8, 6, 5, 4],
              [6, 5, 4, 1, 3, 2, 9, 8, 7],
              [7, 6, 5, 2, 4, 3, 1, 9, 8],
              [4, 3, 2, 8, 1, 9, 7, 6, 5],
              [1, 9, 8, 5, 7, 6, 4, 3, 2]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            if button.identification==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
            #cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        #(255, 255, 255), 4)
        return img

    class button():
        def __init__(self, pos,identification, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id
            self.identification=identification

    buttonlist = []
    colourlist=[(0,0,255),(0,128,255),(255,255,0),(255,0,127),(153,0,153),(0,255,255),(0,102,102),(102,0,0),(160,160,160)]
    pp=0
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0],color=colourlist[pp], text=key,identification=(255,0,255))) #pink
            pp+=1
    for i in range(9):
        for j, key in enumerate(sudoku_keys[i]):
            if key != 0:
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=colourlist[key-1], id=[i, j],identification=(0,255,0))) #green
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(255,255,255), id=[i, j],identification=(255,255,255))) #white

    placing_text = ""
    cc=(255,255,255)
    ok = 1
    okk = 1
    b = []
    for i in range(9):
        for j, key in enumerate(result[i]):
            if key != 0:
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=colourlist[key-1], id=[i, j],identification=(0,0,0)))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j],identification=(0,0,0)))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    #cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    #cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                #(255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        identification = button.identification
                        id = button.id
                        if identification == (255, 255, 255):  # red
                            button.text = placing_text
                            button.color = cc
                            button.identification=(255, 0, 0)

                            print(sudoku_keys)

                            if placing_text != "":
                                print("placing")
                                sudoku_keys[id[0]][id[1]] = int(placing_text)

                            print(sudoku_keys)
                            print(result)


                        elif identification == (255, 0, 255):  # pink
                            placing_text = button.text
                            cc=button.color
                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif identification == (255, 0, 0):
                            button.color = (255, 255, 255)
                            button.identification=(255,255,255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations! You solved the game!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Game over! These are the answers!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def sudoku_word():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3

    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["R", "D"], ["K", "A"], ["O", "S"], ["U", "N"], ["E"]]
    # sudoku_keys=[["","","","","","","","U","N"],
    #                    ["","U","S","E","","D","A","R",""],
    #                    ["","E","","","A","","","",""],
    #                    ["","S","","","","U","","D","O"],
    #                    ["","","","","","","","K","U"],
    #                    ["","D","","","S","","R","",""],
    #                    ["N","","","","D","K","","",""],
    #                    ["","K","E","","","","","",""],
    #                    ["","","","O","E","","K","A",""]]
    sudoku_keys = [["","A","D","K","O","S","E","U","N"],
                   ["O","U","S","E","N","D","A","R","K"],
                   ["K","E","N","U","A","R","D","O","S"],
                   ["E","S","R","A","K","U","N","D","O"],
                   ["A","N","O","D","R","E","S","K","U"],
                   ["U","D","K","N","S","O","R","E","A"],
                   ["N","O","","R","D","K","U","S","E"],
                   ["D","K","E","S","U","A","O","N","R"],
                   ["S","R","U","O","E","N","K","A","D"]]

    result = [["R","A","D","K","O","S","E","U","N"],
                   ["O","U","S","E","N","D","A","R","K"],
                   ["K","E","N","U","A","R","D","O","S"],
                   ["E","S","R","A","K","U","N","D","O"],
                   ["A","N","O","D","R","E","S","K","U"],
                   ["U","D","K","N","S","O","R","E","A"],
                   ["N","O","A","R","D","K","U","S","E"],
                   ["D","K","E","S","U","A","O","N","R"],
                   ["S","R","U","O","E","N","K","A","D"]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            cv2.putText(img, button.text, (button.pos[0] + 10, button.pos[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 4)
            if color==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
        return img

    class button():
        def __init__(self, pos, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0], key))
    for i in range(9):
        for j, key in enumerate(sudoku_keys[i]):
            if key != "":
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=key, size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))

    placing_text = ""
    ok = 1
    okk = 1
    b = []
    for i in range(9):
        for j, key in enumerate(result[i]):
            if key != "":
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=key, size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                #print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        color = button.color
                        id = button.id
                        if color == (0, 0, 255):  # red
                            button.text = placing_text
                            button.color = (255, 0, 0)
                            print(sudoku_keys)

                            if placing_text != "":
                                #print("placing")
                                sudoku_keys[id[0]][id[1]] = placing_text

                            print(sudoku_keys)
                            print(result)


                        elif color == (255, 0, 255):  # pink
                            placing_text = button.text

                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif color == (255, 0, 0):
                            button.color = (0, 0, 255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations! You solved the game"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Game over! These are the answers!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def sudoku_2():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3

    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["1", "2"], ["3", "4"]]
    # sudoku_keys=[[0,0,0,2],
    #         [0,3,0,0],
    #         [4,0,0,0],
    #         [0,0,2,0]]
    sudoku_keys = [[1,0,3,2],[2,3,4,1],[4,2,1,0],[3,1,2,4]]

    result = [[1,4,3,2],[2,3,4,1],[4,2,1,3],[3,1,2,4]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            cv2.putText(img, button.text, (button.pos[0] + 10, button.pos[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 4)
            if color==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
        return img

    class button():
        def __init__(self, pos, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0], key))
    for i in range(4):
        for j, key in enumerate(sudoku_keys[i]):
            if key != 0:
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))

    placing_text = ""
    ok = 1
    okk = 1
    b = []
    for i in range(4):
        for j, key in enumerate(result[i]):
            if key != 0:
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 10, button.pos[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        color = button.color
                        id = button.id
                        if color == (0, 0, 255):  # red
                            button.text = placing_text
                            button.color = (255, 0, 0)
                            print(sudoku_keys)

                            if placing_text != "":
                                print("placing")
                                sudoku_keys[id[0]][id[1]] = int(placing_text)

                            print(sudoku_keys)
                            print(result)


                        elif color == (255, 0, 255):  # pink
                            placing_text = button.text

                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif color == (255, 0, 0):
                            button.color = (0, 0, 255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations! You solved the game!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0

        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Game over! These are the answers!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def sudoku_word_2():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3

    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["A", "B"], ["C", "D"]]
    # sudoku_keys=[["","","B",""],
    #              ["","C","",""],
    #              ["","","",""],
    #               ["","","D",""]]
    sudoku_keys =[["A","D","B","C"],
                 ["B","","A","D"],
                 ["D","B","C",""],
                  ["C","A","D","B"]]

    result = [["A","D","B","C"],
                 ["B","C","A","D"],
                 ["D","B","C","A"],
                  ["C","A","D","B"]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            cv2.putText(img, button.text, (button.pos[0] + 10, button.pos[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 4)
            if color==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
        return img

    class button():
        def __init__(self, pos, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0], key))
    for i in range(4):
        for j, key in enumerate(sudoku_keys[i]):
            if key != "":
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=key, size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))

    placing_text = ""
    ok = 1
    okk = 1
    b = []
    for i in range(4):
        for j, key in enumerate(result[i]):
            if key != "":
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=key, size=[40, 40], color=(0, 255, 0), id=[i, j]))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j]))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                #print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        color = button.color
                        id = button.id
                        if color == (0, 0, 255):  # red
                            button.text = placing_text
                            button.color = (255, 0, 0)
                            print(sudoku_keys)

                            if placing_text != "":
                                #print("placing")
                                sudoku_keys[id[0]][id[1]] = placing_text

                            print(sudoku_keys)
                            print(result)


                        elif color == (255, 0, 255):  # pink
                            placing_text = button.text

                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif color == (255, 0, 0):
                            button.color = (0, 0, 255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations! You solved the game!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh==1:
                text = "Game over! These are the answers!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
def sudoku_color_2():
    import cv2
    import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3
    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # 1.4.1 8.7.1

    def issafe(sudoku, x, y, i):
        for j in range(0, 9):
            if sudoku[j][y] == i:
                return False
        for j in range(0, 9):
            if sudoku[x][j] == i:
                return False
        x1 = 0
        y1 = 0
        if x >= 0 and x <= 2:
            if y >= 0 and y <= 2:
                x1 = 0
                y1 = 0

            if y >= 3 and y <= 5:
                x1 = 0
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 0
                y1 = 6
        elif x >= 3 and x <= 5:
            if y >= 0 and y <= 2:
                x1 = 3
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 3
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 3
                y1 = 6
        else:
            if y >= 0 and y <= 2:
                x1 = 6
                y1 = 0
            if y >= 3 and y <= 5:
                x1 = 6
                y1 = 3
            if y >= 6 and y <= 8:
                x1 = 6
                y1 = 6
        for j in range(x1, x1 + 3):
            for k in range(y1, y1 + 3):
                if sudoku[j][k] == i:
                    return False
        return True

    def check(sudoku, x, y):
        if x == 9:
            print(sudoku)
            return sudoku

        if sudoku[x][y] == 0:
            for i in range(1, 10):
                if issafe(sudoku, x, y, i):
                    sudoku[x][y] = i
                    if y == 8:
                        check(sudoku, x + 1, 0)
                    else:
                        check(sudoku, x, y + 1)
            sudoku[x][y] = 0
            return
        else:
            if y == 8:
                check(sudoku, x + 1, 0)
            else:
                check(sudoku, x, y + 1)

    detector = HandDetector(detectionCon=0.8)
    keys = [["1", "2"], ["3", "4"]]
    # sudoku_keys=[[0,0,0,2],
    #         [0,3,0,0],
    #         [4,0,0,0],
    #         [0,0,2,0]]
    sudoku_keys = [[1, 0, 3, 2], [2, 3, 4, 1], [4, 2, 1, 0], [3, 1, 2, 4]]

    result = [[1, 4, 3, 2], [2, 3, 4, 1], [4, 2, 1, 3], [3, 1, 2, 4]]

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            if button.identification==(0,255,0):
                cv2.rectangle(img,button.pos,(x+w,y+h),(0,0,0),4)
            #cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        #(255, 255, 255), 4)
        return img

    class button():
        def __init__(self, pos,identification, text="", size=[60, 60], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id
            self.identification=identification

    buttonlist = []
    colourlist=[(0,0,255),(0,128,255),(255,255,0),(255,0,127)]
    pp=0
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 100, 100 * i + 0],color=colourlist[pp], text=key,identification=(255,0,255))) #pink
            pp+=1
    for i in range(4):
        for j, key in enumerate(sudoku_keys[i]):
            if key != 0:
                buttonlist.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=colourlist[key-1], id=[i, j],identification=(0,255,0))) #green
            else:
                buttonlist.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(255,255,255), id=[i, j],identification=(255,255,255))) #white

    placing_text = ""
    cc=(255,255,255)
    ok = 1
    okk = 1
    b = []
    for i in range(4):
        for j, key in enumerate(result[i]):
            if key != 0:
                b.append(
                    button([100 * j + 350, 60 * i + 0], text=str(key), size=[40, 40], color=colourlist[key-1], id=[i, j],identification=(0,0,0)))
            else:
                b.append(button([100 * j + 350, 60 * i + 0], size=[40, 40], color=(0, 0, 255), id=[i, j],identification=(0,0,0)))
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        if okk == 1:
            img = drawall(img, buttonlist)
            cv2.rectangle(img, (190, 400), (290, 500), (125, 126, 0), cv2.FILLED)
            cv2.putText(img, "Quit", (210, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4)

        if lmlist and ok == 1:
            if sudoku_keys == result:
                print("sudoku solved")
                ok = 0
            l1, _, _ = detector.findDistance(8, 12, img, draw=False)
            if 190 < lmlist[8][0] < 290 and 400 < lmlist[8][1] < 500 and l1 < 10:
                ok = 0
                okk = 0

            for button in buttonlist:
                x, y = button.pos
                w, h = button.size

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    #cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    #cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                #(255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:

                        x, y = button.pos
                        w, h = button.size
                        identification = button.identification
                        id = button.id
                        if identification == (255, 255, 255):  # red
                            button.text = placing_text
                            button.color = cc
                            button.identification=(255, 0, 0)

                            print(sudoku_keys)

                            if placing_text != "":
                                print("placing")
                                sudoku_keys[id[0]][id[1]] = int(placing_text)

                            print(sudoku_keys)
                            print(result)


                        elif identification == (255, 0, 255):  # pink
                            placing_text = button.text
                            cc=button.color
                            # cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            #
                            # cv2.putText(img, button.text, placing_pos, cv2.FONT_HERSHEY_PLAIN, 2,
                            #         (255, 255, 255), 4)
                            # print("green button pressed",placing_pos)


                        elif identification == (255, 0, 0):
                            button.color = (255, 255, 255)
                            button.identification=(255,255,255)
                            button.text = ""
                            # sudoku_keys[id[0]][id[1]]=0
                            # button.id=[-1,-1]

                        # finaltext+=button.text
                        sleep(0.20)
        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        if ok == 0 and okk == 1:
            # print("ok,solved")
            cv2.putText(img, "Solved!", (200, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Congratulations, you solved the game!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        if okk == 0:
            drawall(img, b)
            cv2.putText(img, "Game over! These are the answers!", (180, 600), cv2.FONT_ITALIC, 2, (175, 230, 120), 4)
            if chh == 1:
                text = "Game over! These are the answers!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0
        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
if __name__ == "__main__":
    sudoku_color_2()


