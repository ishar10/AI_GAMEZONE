##################################################################################
# FRONTEND
##################################################################################
import scrabble


def quit():
    exit()
import tkinter as tk
from tkinter import messagebox
import sqlite3
from tkinter import messagebox
import cv2
import os
from PIL import Image,ImageTk
import numpy as np
import puzzle
import sudoku
import tictactoe
import c4

def database(d):
    name=fn.get()
    age = ln.get()
    country = var.get()
    gender = radio_var.get()
    if name!="" and age!="" and country!="select country" and gender!="":
        conn=sqlite3.connect("form.db")
        with conn:
            cursor=conn.cursor()
        cursor.execute("SELECT * FROM Gamers")

        rows = cursor.fetchall()
        k=0
        for row in rows:
            if row==(name,age,country,gender):
                k=1
                if d==1:
                    return 1
                else:
                    messagebox.showerror("Registration Failed", "User already exists! Try logging in!")
        if k==0 and d==1:
            messagebox.showerror("Login Failed", "User dont exists! Try Registering!")
            return 0

        if k==0:
            cursor.execute("CREATE TABLE IF NOT EXISTS Gamers (Name TEXT,Age TEXT,Country TEXT,Gender TEXT)")
            cursor.execute("INSERT INTO Gamers(Name,Age,Country,Gender) VALUES(?,?,?,?)",(name,age,country,gender))
            conn.commit()
            secondwin(0)


    else:
        messagebox.showerror("Unable to save details", "One or more fields missing!")

def c():
    import speech_recognition as sr
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("speak anything")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            if text == "play sudoku" or text=="play Sudoku":
                sudoku.sudoku()
            if text== "play puzzle" or text=="play Puzzle":
                puzzle.puzzle1()
            if text=="play Tic Tac Toe":
                tictactoe.tic()
            if text=="play connect 4":
                c4.c4()

        except:
            print("sorry")
def sudoku_d2():
    window6 = tk.Tk()
    window6.title("SUDOKU GAMEZONE")
    image = Image.open("color.jfif")
    photo = ImageTk.PhotoImage(master=window6, image=image)
    lab = tk.Label(window6, image=photo).place(x=400, y=200)

    image1 = Image.open("word.png")
    photo1 = ImageTk.PhotoImage(master=window6, image=image1)
    lab1 = tk.Label(window6, image=photo1).place(x=750, y=200)

    image2 = Image.open("number.png")
    photo2 = ImageTk.PhotoImage(master=window6, image=image2)
    lab2 = tk.Label(window6, image=photo2).place(x=50, y=200)
    l1 = tk.Label(window6, text="Welcome to SUDOKU GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
    # l1.grid(column=1,row=0)
    b1 = tk.Button(window6, text="NUMBER SUDOKU", font=("arial", 20), bg="orange", fg="green",
                   command=sudoku.sudoku_2).place(
        x=50,
        y=500)
    # b1.grid(column=1,row=1)

    b2 = tk.Button(window6, text="COLOUR SUDOKU", font=("arial", 20), bg="green", fg="yellow",
                   command=sudoku.sudoku_color_2).place(
        x=400,
        y=500)
    # b2.grid(column=2,row=1)

    b3 = tk.Button(window6, text="WORD SUDOKU", font=("arial", 20), bg="yellow", fg="red",
                   command=sudoku.sudoku_word_2).place(
        x=750,
        y=500)
    # b3.grid(column=1,row=3)

    window6.geometry("1000x600")
    window6.mainloop()

def sudoku_d3():
    window5 = tk.Tk()
    window5.title("SUDOKU GAMEZONE")
    image = Image.open("color.jfif")
    photo = ImageTk.PhotoImage(master=window5, image=image)
    lab = tk.Label(window5, image=photo).place(x=400, y=200)

    image1 = Image.open("word.png")
    photo1 = ImageTk.PhotoImage(master=window5, image=image1)
    lab1 = tk.Label(window5, image=photo1).place(x=750, y=200)

    image2 = Image.open("number.png")
    photo2 = ImageTk.PhotoImage(master=window5, image=image2)
    lab2 = tk.Label(window5, image=photo2).place(x=50, y=200)
    l1 = tk.Label(window5, text="Welcome to SUDOKU GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
    # l1.grid(column=1,row=0)
    b1 = tk.Button(window5, text="NUMBER SUDOKU", font=("arial", 20), bg="orange", fg="green", command=sudoku.sudoku).place(
        x=50,
        y=500)
    # b1.grid(column=1,row=1)

    b2 = tk.Button(window5, text="COLOUR SUDOKU", font=("arial", 20), bg="green", fg="yellow", command=sudoku.sudoku_color).place(
        x=400,
        y=500)
    # b2.grid(column=2,row=1)

    b3 = tk.Button(window5, text="WORD SUDOKU", font=("arial", 20), bg="yellow", fg="red", command=sudoku.sudoku_word).place(
        x=750,
        y=500)
    # b3.grid(column=1,row=3)

    window5.geometry("1000x600")
    window5.mainloop()

def sudoku_diff():

        window4 = tk.Tk()
        window4.title("SUDOKU GAMEZONE")
        image1 = Image.open("3x3.jfif")
        photo1 = ImageTk.PhotoImage(master=window4, image=image1)
        lab1 = tk.Label(window4, image=photo1).place(x=700, y=200)

        image2 = Image.open("download (2).jfif")
        photo2 = ImageTk.PhotoImage(master=window4, image=image2)
        lab2 = tk.Label(window4, image=photo2).place(x=200, y=200)
        l1 = tk.Label(window4, text="Welcome to SUDOKU GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
        # l1.grid(column=1,row=0)
        b1 = tk.Button(window4, text="2X2 SUDOKU", font=("arial", 20), bg="orange", fg="green",
                       command=sudoku_d2).place(
            x=200,
            y=500)

        b2 = tk.Button(window4, text="3X3 SUDOKU", font=("arial", 20), bg="green", fg="yellow",
                       command=sudoku_d3).place(x=700,
                                                    y=500)
        window4.geometry("1000x600")
        window4.mainloop()


def ticwindow():

    window3 = tk.Tk()
    window3.title("TIC-TAC-TOE GAMEZONE")
    image1 = Image.open("user.jfif")
    photo1 = ImageTk.PhotoImage(master=window3, image=image1)
    lab1 = tk.Label(window3, image=photo1).place(x=700, y=200)

    image2 = Image.open("computer.jfif")
    photo2 = ImageTk.PhotoImage(master=window3, image=image2)
    lab2 = tk.Label(window3, image=photo2).place(x=100, y=200)
    l1 = tk.Label(window3, text="Welcome to TIC-TAC-TOE GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
    # l1.grid(column=1,row=0)
    b1 = tk.Button(window3, text="Play with Computer", font=("arial", 20), bg="orange", fg="green", command=tictactoe.tic_computer).place(
        x=100,
        y=500)


    b2 = tk.Button(window3, text="2 players", font=("arial", 20), bg="green", fg="yellow", command=tictactoe.tic).place(x=750,
                                                                                                                y=500)





    window3.geometry("1000x600")
    window3.mainloop()
def puzzlewindow():

    window2 = tk.Tk()
    window2.title("PUZZLE GAMEZONE")
    image=Image.open("game.jpg")
    photo=ImageTk.PhotoImage(master=window2,image=image)
    lab=tk.Label(window2,image=photo).place(x=350,y=200)

    image1 = Image.open("game1.jpg")
    photo1 = ImageTk.PhotoImage(master=window2, image=image1)
    lab1 = tk.Label(window2, image=photo1).place(x=700, y=200)

    image2 = Image.open("Screenshot (611).png")
    photo2 = ImageTk.PhotoImage(master=window2, image=image2)
    lab2 = tk.Label(window2, image=photo2).place(x=0, y=200)






    l1 = tk.Label(window2, text="Welcome to PUZZLE GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
    # l1.grid(column=1,row=0)
    b1 = tk.Button(window2, text="Puzzle1", font=("arial", 20), bg="orange", fg="green", command=puzzle.puzzle1).place(
        x=100,
        y=500)
    # b1.grid(column=1,row=1)

    b2 = tk.Button(window2, text="Puzzle2", font=("arial", 20), bg="green", fg="yellow", command=puzzle.puzzle2).place(x=450,
                                                                                                                y=500)
    # b2.grid(column=2,row=1)

    b3 = tk.Button(window2, text="Puzzle3", font=("arial", 20), bg="yellow", fg="red", command=puzzle.puzzle3).place(x=850,
                                                                                                                y=500)
    # b3.grid(column=1,row=3)


    window2.geometry("1000x600")
    window2.mainloop()


def secondwin(d):
    result=1
    if d==1:
        result=database(1)
    if result==1:
        window1 = tk.Tk()
        window1.title("AI GAMEZONE")
        l1 = tk.Label(window1, text="Welcome to AI GAMEZONE", font=("Algerian", 30)).place(x=250, y=40)
        # l1.grid(column=1,row=0)
        b1 = tk.Button(window1, text="AI Puzzle", font=("arial", 20), bg="orange", fg="green", command=puzzlewindow).place(x=150,
                                                                                                                    y=150)
        # b1.grid(column=1,row=1)

        b2 = tk.Button(window1, text="AI sudoku", font=("arial", 20), bg="green", fg="yellow", command=sudoku_diff).place(x=350,
                                                                                                                    y=150)
        # b2.grid(column=2,row=1)
        b8 = tk.Button(window1, text="AI snake game", font=("arial", 20), bg="red", fg="blue", command=sudoku_diff).place(x=550,y=150)

        b3 = tk.Button(window1, text="AI tic-tac-toe", font=("arial", 20), bg="yellow", fg="red", command=ticwindow).place(x=150,
                                                                                                                    y=260)
        # b3.grid(column=1,row=3)

        b4 = tk.Button(window1, text="AI connect-four", font=("arial", 20), bg="pink", fg="blue", command=c4.c4).place(x=350,
                                                                                                                   y=260)
        # b4.grid(column=2,row=3)
        b7 = tk.Button(window1, text="AI scrabble", font=("arial", 20), bg="blue", fg="pink", command=scrabble.scrabble).place(x=600,y=260)
        b5 = tk.Button(window1, text="Quit", font=("arial", 20), bg="purple", fg="white", command=quit).place(x=430, y=370)
        b6 = tk.Button(window1, text="Say", font=("arial", 20), bg="purple", fg="white", command=c).place(x=430, y=450)

        window1.geometry("1000x600")
        window1.mainloop()


window=tk.Tk()
window.geometry("500x500")
window.title("Registration Form")


fn=tk.StringVar()
ln=tk.StringVar()
var= tk.StringVar()
radio_var=tk.StringVar()


list1=["Nepal","India","Canada"]
droplist=tk.OptionMenu(window,var,*list1)
var.set("select country")
droplist.config(width=15)

r1=tk.Radiobutton(window,text="Male",variable=radio_var,value="Male").place(x=300,y=280)
r2=tk.Radiobutton(window,text="Female",variable=radio_var,value="Female").place(x=350,y=280)

label1=tk.Label(window, text="Registration Form",relief="solid",width=20,font=("arial",19,"bold"))
label1.place(x=90,y=53)

label2=tk.Label(window, text="Name",relief="solid",width=20,font=("arial",10,"bold"))
label2.place(x=80,y=130)


label4=tk.Label(window, text="Age",relief="solid",width=20,font=("arial",10,"bold"))
label4.place(x=80,y=180)

label3=tk.Label(window, text="Country",relief="solid",width=20,font=("arial",10,"bold"))
label3.place(x=80,y=230)

label4=tk.Label(window, text="Gender",relief="solid",width=20,font=("arial",10,"bold"))
label4.place(x=80,y=280)

entry1=tk.Entry(window,textvar=fn).place(x=300,y=130)
entry2=tk.Entry(window,textvar=ln).place(x=300,y=180)
droplist.place(x=300,y=230)


b1=tk.Button(window,text="Login",width=12,font=("arial",20),bg="brown",fg="white",command= lambda:[secondwin(1)]).place(x=100,y=330)
b2=tk.Button(window,text="Quit",font=("arial",20),bg="brown",fg="white",command=quit).place(x=350,y=330)
label5=tk.Label(window, text="New user?==>",relief="solid",width=20,font=("arial",10,"bold")).place(x=30,y=450)
b3=tk.Button(window,text="Register",width=12,font=("arial",20),bg="brown",fg="white",command=lambda :[database(0)]).place(x=200,y=430)

img=cv2.imread("images2/image_part_001.jpg")
print(img.shape)
window.mainloop()







