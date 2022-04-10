
def tic():
    import cv2
    # import cv2.omnidir
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import pyttsx3

    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8)

    # 1.4.1  8.7.1

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
            cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                        (255, 255, 255), 4)
        return img

    class button():
        def __init__(self, pos, text="", size=[70, 70], color=(255, 0, 255), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []
    keys = [["", "", ""], ["", "", ""], ["", "", ""]]

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 450, 100 * i + 200], text=key, id=[i, j]))

    def check(keys):
        if (keys[0][0] == keys[1][1] == keys[2][2] and keys[0][0] != "" and keys[1][1] != "" and keys[2][2] != "") \
                or (
                keys[0][2] == keys[1][1] == keys[2][0] and keys[0][2] != "" and keys[1][1] != "" and keys[2][0] != "") \
                or (
                keys[0][0] == keys[0][1] == keys[0][2] and keys[0][0] != "" and keys[0][1] != "" and keys[0][2] != "") \
                or (
                keys[1][0] == keys[1][1] == keys[1][2] and keys[1][0] != "" and keys[1][1] != "" and keys[1][2] != "") \
                or (
                keys[2][0] == keys[2][1] == keys[2][2] and keys[2][0] != "" and keys[2][1] != "" and keys[2][2] != "") \
                or (
                keys[0][0] == keys[1][0] == keys[2][0] and keys[0][0] != "" and keys[1][0] != "" and keys[2][0] != "") \
                or (
                keys[0][1] == keys[1][1] == keys[2][1] and keys[0][1] != "" and keys[1][1] != "" and keys[2][1] != "") \
                or (
                keys[0][2] == keys[1][2] == keys[2][2] and keys[0][2] != "" and keys[1][2] != "" and keys[2][2] != ""):
            return 0
        elif keys[0][0] != "" and keys[0][1] != "" and keys[0][2] != "" and keys[1][1] != "" and keys[1][0] != "" and \
                keys[1][2] != "" and keys[2][1] != "" and keys[2][0] != "" and keys[2][2] != "":
            return -1
        else:
            return 1

    placing_text = "X"
    text = ""
    text_speech = pyttsx3.init()
    chh=1
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        drawall(img, buttonlist)
        t = check(keys)
        #print(keys, t)
        cv2.putText(img, "Welcome to tic-tac-toe", (300, 100), cv2.FONT_ITALIC, 2, (126, 25, 25), 4)

        if placing_text == "X":
            text = "O"
        else:
            text = "X"
        if t != 0 and t != -1:
            cv2.putText(img, text + "'s turn", (450, 600), cv2.FONT_ITALIC, 2, (25, 25, 255), 4)

        if lmlist and t != 0 and t != -1:
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                id = button.id
                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                (255, 255, 255), 4)
                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:
                        if button.text == "":
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)

                            cv2.putText(img, placing_text, button.pos, cv2.FONT_HERSHEY_PLAIN, 2,
                                        (255, 255, 255), 4)
                            if placing_text == "X":
                                keys[id[0]][id[1]] = "X"
                                button.text = "O"
                                placing_text = "O"
                                button.color = (255, 0, 0)

                            else:
                                keys[id[0]][id[1]] = "O"
                                button.text = "X"
                                placing_text = "X"
                                button.color = (0, 0, 255)

        if t == 0:
            if placing_text == "X":
                #print("X wins")
                cv2.putText(img, "X wins the game", (350, 600), cv2.FONT_ITALIC, 2, (255, 255, 0), 4)
                if chh==1:
                    text = "X wins the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    chh=0
            else:
                #print("O wins")
                cv2.putText(img, "O wins the game", (350, 600), cv2.FONT_ITALIC, 2, (255, 255, 0), 4)
                if chh==1:
                    text = "O wins the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    chh=0
        elif t == -1:
            #print("No body wins")
            cv2.putText(img, "Nobody wins.Thats a tie!", (300, 600), cv2.FONT_ITALIC, 2, (255, 255, 0), 4)
            if chh == 1:
                text = "Its a tie!!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                chh = 0

        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def tic_computer():
    import cv2
    import pyttsx3
    from cvzone.HandTrackingModule import HandDetector
    from time import sleep
    import random
    import cvzone
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    detector = HandDetector(detectionCon=0.8)

        # 1.4.1  8.7.1

    def drawall(img, buttonlist):
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                color = button.color
                cv2.rectangle(img, button.pos, (x + w, y + h), color, cv2.FILLED)
                cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 255, 255), 4)
            return img

    class button():
            def __init__(self, pos, text="", size=[70, 70], color=(255, 0, 255), id=[-1, -1]):
                self.pos = pos
                self.text = text
                self.size = size
                self.color = color
                self.id = id

    buttonlist = []
    keys = [["", "", ""], ["", "", ""], ["", "", ""]]

    for i in range(len(keys)):
            for j, key in enumerate(keys[i]):
                buttonlist.append(button([100 * j + 450, 100 * i + 200], text=key, id=[i, j]))

    def check(keys):
            if (keys[0][0] == keys[1][1] == keys[2][2] and keys[0][0] != "" and keys[1][1] != "" and keys[2][2] != "") \
                    or (
                    keys[0][2] == keys[1][1] == keys[2][0] and keys[0][2] != "" and keys[1][1] != "" and keys[2][0] != "") \
                    or (
                    keys[0][0] == keys[0][1] == keys[0][2] and keys[0][0] != "" and keys[0][1] != "" and keys[0][2] != "") \
                    or (
                    keys[1][0] == keys[1][1] == keys[1][2] and keys[1][0] != "" and keys[1][1] != "" and keys[1][2] != "") \
                    or (
                    keys[2][0] == keys[2][1] == keys[2][2] and keys[2][0] != "" and keys[2][1] != "" and keys[2][2] != "") \
                    or (
                    keys[0][0] == keys[1][0] == keys[2][0] and keys[0][0] != "" and keys[1][0] != "" and keys[2][0] != "") \
                    or (
                    keys[0][1] == keys[1][1] == keys[2][1] and keys[0][1] != "" and keys[1][1] != "" and keys[2][1] != "") \
                    or (
                    keys[0][2] == keys[1][2] == keys[2][2] and keys[0][2] != "" and keys[1][2] != "" and keys[2][2] != ""):
                return 0
            elif keys[0][0] != "" and keys[0][1] != "" and keys[0][2] != "" and keys[1][1] != "" and keys[1][0] != "" and \
                    keys[1][2] != "" and keys[2][1] != "" and keys[2][0] != "" and keys[2][2] != "":
                return -1
            else:
                return 1

    placing_text = "X"
    text = ""
    choice=[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
    user=0
    com=0
    tie=0
    text_speech = pyttsx3.init()
    chh=1
    while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmlist, bbox = detector.findPosition(img)
            drawall(img, buttonlist)
            t = check(keys)
            #print(keys, t)
            cv2.putText(img, "Welcome to tic-tac-toe", (300, 100), cv2.FONT_ITALIC, 2, (126, 25, 25), 4)



            if lmlist and t != 0 and t != -1:
                for button in buttonlist:
                    x, y = button.pos
                    w, h = button.size
                    id = button.id
                    if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                        cv2.rectangle(img, button.pos, (x + w, y + h), (175, 0, 175), cv2.FILLED)
                        cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2,
                                    (255, 255, 255), 4)
                        l, _, _ = detector.findDistance(8, 12, img, draw=False)
                        if l < 30:
                            if button.text == "":
                                choice.remove((id[0],id[1]))
                                cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)

                                cv2.putText(img, "X", button.pos, cv2.FONT_HERSHEY_PLAIN, 2,
                                            (255, 255, 255), 4)
                                # if placing_text == "X":
                                #
                                #     button.text = "O"
                                #     placing_text = "O"
                                button.color = (255, 0, 0)
                                button.text="O"
                                keys[id[0]][id[1]] = "X"

                                # else:
                                #     keys[id[0]][id[1]] = "O"
                                #     button.text = "X"
                                #     placing_text = "X"
                                #     button.color = (0, 0, 255)
                                t = check(keys)
                                if t==0:
                                    cv2.putText(img, "You won the game", (350, 600), cv2.FONT_ITALIC, 2, (255, 255, 0),
                                                    4)
                                    user=1
                                if t==-1:
                                    # print("No body wins")
                                    cv2.putText(img, "Nobody wins.Thats a tie!", (300, 600), cv2.FONT_ITALIC, 2,
                                                (255, 255, 0), 4)
                                    tie=1

                                if t!=0 and t!=-1:
                                    s = random.choice(choice)
                                    x=0
                                    if s==(0,1):
                                        x=1
                                    elif s==(0,2):
                                        x=2
                                    elif s==(1,0):
                                        x=3
                                    elif s==(1,1):
                                        x=4
                                    elif s==(1,2):
                                        x=5
                                    elif s==(2,0):
                                        x=6
                                    elif s==(2,1):
                                        x=7
                                    elif s==(2,2):
                                        x=8
                                    keys[s[0]][s[1]] = "O"
                                    buttonlist[x].text="X"
                                    buttonlist[x].color=(0, 0, 255)
                                    choice.remove(s)
                                    t=check(keys)
                                    if t == 0:

                                        cv2.putText(img, "Computer won the game", (350, 600), cv2.FONT_ITALIC, 2,
                                                        (255, 255, 0), 4)
                                        com=1

                                    elif t == -1:
                                        # print("No body wins")
                                        cv2.putText(img, "Nobody wins.Thats a tie!", (300, 600), cv2.FONT_ITALIC, 2,
                                                    (255, 255, 0), 4)
                                        tie=1
            if com==1:
                cv2.putText(img, "Computer won the game", (350, 600), cv2.FONT_ITALIC, 2,
                            (255, 255, 0), 4)
                if chh==1:
                    text = "Computer wins the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    chh=0
            elif user==1:
                cv2.putText(img, "You won the game", (350, 600), cv2.FONT_ITALIC, 2,
                            (255, 255, 0), 4)
                if chh==1:
                    text = "you won the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    chh=0
            elif tie==1:
                cv2.putText(img, "Nobody wins.Thats a tie!", (300, 600), cv2.FONT_ITALIC, 2,
                            (255, 255, 0), 4)
                if chh==1:
                    text = "Its a tie!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    chh=0






            # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
            # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
            # (255, 255, 255), 5)

            cv2.imshow("image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break