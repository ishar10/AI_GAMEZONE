
def c4():
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

    # 1.4.1 8.7.1

    def drawall(img, buttonlist):
        for button in buttonlist:
            x, y = button.pos
            w, h = button.size
            color = button.color
            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x + 35, y + 35), 30, color, cv2.FILLED)
            # cv2.putText(img, button.text, (button.pos[0] + 20, button.pos[1] + 40), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 4)
        return img

    class button():
        def __init__(self, pos, text="", size=[70, 70], color=(0, 0, 0), id=[-1, -1]):
            self.pos = pos
            self.text = text
            self.size = size
            self.color = color
            self.id = id

    buttonlist = []
    keys = [["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""], ["", "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""]]

    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonlist.append(button([100 * j + 320, 100 * i], text=key, id=[i, j]))

    def check(img, keys, placing_text, current_id, point1, point2, w, h):
        c = 0

        #########################################
        for i in range(current_id[1], 7):
            if keys[current_id[0]][i] == placing_text:
                c += 1
                if c == 4:
                    return 0, (point1, point2), (point1 + (c * w), point2)
            else:
                break
        p1 = ()
        p2 = ()

        if c == 1:
            p1 = (point1, point2)
            p2 = (point1 - (4 * w), point2)
        else:
            p1 = (point1 + (c * w), point2)
            p2 = ((point1 + (c * w)) - (4 * w), point2)

        for i in range(current_id[1] - 1, -1, -1):

            if keys[current_id[0]][i] == placing_text:
                print("hello1")
                c += 1

                if c == 4:
                    return 0, p1, p2

            else:
                break
        ############################################
        c = 0
        for i in range(current_id[0], 7):
            if keys[i][current_id[1]] == placing_text:
                c += 1
                if c == 4:
                    print("yes3")
                    return 0, (point1, point2), (point1, point2 + (c * h))
            else:
                break
        p1 = ()
        p2 = ()

        if c == 1:
            p1 = (point1, point2)
            p2 = (point1, point2 - (4 * h))
        else:
            p1 = (point1, point2 + (c * h))
            p2 = (point1, (point2 + (c * h)) - (4 * h))
        for i in range(current_id[0] - 1, -1, -1):
            if keys[i][current_id[1]] == placing_text:
                c += 1
                if c == 4:
                    return 0, p1, p2

            else:
                break
        #################################################
        c = 0
        i = current_id[0]
        j = current_id[1]
        while (i >= 0 and j >= 0):
            if keys[i][j] == placing_text:
                c += 1
                if c == 4:
                    print("yes5")
                    return 0, (point1, point2), (point1 - (c * w), point2 - (c * h))
                i -= 1
                j -= 1
            else:
                break
        p1 = ()
        p2 = ()

        if c == 1:
            p1 = (point1, point2)
            p2 = (point1 + (4 * w), point2 + (4 * h))
        else:
            p1 = (point1 - (c * w), point2 - (c * h))
            p2 = ((point1 - (c * w)) + (5 * w), (point2 - (c * h)) + (5 * h))

        i = current_id[0] + 1
        j = current_id[1] + 1
        while (i < 7 and j < 7):
            if keys[i][j] == placing_text:
                c += 1
                if c == 4:
                    return 0, p1, p2
                i += 1
                j += 1
            else:
                break
        ########################################################
        c = 0

        i = current_id[0]
        j = current_id[1]
        while (i < 7 and j >= 0):
            if keys[i][j] == placing_text:
                c += 1
                if c == 4:
                    print("yes7")
                    return 0, (point1, point2), (point1 - (c * w), point2 + (c * h))
                i += 1
                j -= 1
            else:
                break
        p1 = ()
        p2 = ()

        if c == 1:
            p1 = (point1, point2)
            p2 = (point1 + (4 * w), point2 - (4 * h))
        else:
            p1 = (point1 - (c * w), point2 + (c * h))
            p2 = ((point1 - (c * w)) + (5 * w), (point2 + (c * h)) - (5 * h))

        i = current_id[0] - 1
        j = current_id[1] + 1
        while (i < 7 and j < 7):
            if keys[i][j] == placing_text:
                c += 1
                if c == 4:
                    print("yes8")
                    return 0, p1, p2
                i -= 1
                j += 1
            else:
                break
        c = 0
        for i in keys:
            if "" in i:
                c = 1
                break
        if c == 0:
            return -1
        ######################################################
        return 1, (), ()

    placing_text = "X"
    text = ""
    current_id = [0, 0]
    t = 1
    p1 = ()
    p2 = ()
    t1=1
    text_speech = pyttsx3.init()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        drawall(img, buttonlist)

        if placing_text == "X":
            text = "blue"
        else:
            text = "red"
        if t != 0 and t != -1:
            cv2.putText(img, text + "'s turn", (0, 600), cv2.FONT_ITALIC, 2, (233, 233, 25), 4)

        if lmlist and t != 0 and t != -1:
            for button in buttonlist:
                x, y = button.pos
                w, h = button.size
                id = button.id
                point1 = x + w // 2
                point2 = y + h // 2

                if x < lmlist[8][0] < x + w and y < lmlist[8][1] < y + h:

                    l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    if l < 30:
                        if button.text == "":
                            cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)

                            if placing_text == "X":
                                keys[id[0]][id[1]] = "X"
                                current_id = [id[0], id[1]]
                                button.text = "O"
                                t, p1, p2 = check(img, keys, placing_text, current_id, point1, point2, w, h)
                                print(t)
                                placing_text = "O"
                                button.color = (255, 0, 0)

                            else:
                                keys[id[0]][id[1]] = "O"
                                current_id = [id[0], id[1]]
                                button.text = "X"

                                t, p1, p2 = check(img, keys, placing_text, current_id, point1, point2, w, h)
                                print(t)
                                placing_text = "X"
                                button.color = (0, 0, 255)


        if t == 0:
            if placing_text == "X":
                print("red wins")
                cv2.putText(img, "red wins!!", (0, 600), cv2.FONT_ITALIC, 2, (0, 123, 0), 4)
                cv2.line(img, p1, p2, (255, 255, 255), 20)

                if t1==1:
                    text = "Red wins the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    t1=0

            else:
                print("blue wins")
                cv2.putText(img, "blue wins!!", (0, 600), cv2.FONT_ITALIC, 2, (0, 123, 0), 4)
                cv2.line(img, p1, p2, (255, 255, 255), 20)
                if t1==1:
                    text = "blue wins the game!"
                    text_speech.say(text)
                    text_speech.runAndWait()
                    text_speech.stop()
                    t1=0

        elif t == -1:
            print("No body wins")
            cv2.putText(img, "tie!", (0, 600), cv2.FONT_ITALIC, 2, (255, 255, 0), 4)
            if t1 == 1:
                text = "Its a tie!"
                text_speech.say(text)
                text_speech.runAndWait()
                text_speech.stop()
                t1 = 0

        # cv2.rectangle(img, (200,350), (1000, 450), (0, 0, 0), cv2.FILLED)
        # cv2.putText(img, finaltext, (200 ,425), cv2.FONT_HERSHEY_PLAIN, 5,
        # (255, 255, 255), 5)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break
