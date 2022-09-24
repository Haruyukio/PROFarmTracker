from os import popen
from pathlib import Path
import threading
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import OK
import pyautogui
import mouse
import cv2
import pytesseract
from PIL import Image
import threading
import numpy as np
PosXMax,PosYMax,PosXMin,PosYMin=0,0,0,0
CurrSessionData={}
OneAtATime=True
Stop=True
Counter=0
statu="Not Working"
window = Tk()
window.wm_iconbitmap("pokeball.ico")
window.title("PRO Hunt Tracker")
stat=ttk.Treeview(window)
stat['columns']=("Pokemon","Count","Percentage")

stat.column("#0",width=0,minwidth=0)
stat.column("Pokemon",width=150,anchor=W)
stat.column("Count",width=150,anchor=CENTER)
stat.column("Percentage",width=150,anchor=W)
stat.heading("Pokemon",text="Pokemon",anchor=W)
stat.heading("Count",text="Count",anchor=CENTER)
stat.heading("Percentage",text="Percentage",anchor=W)
def endit():
    global Stop
    global statu
    statu="Not Working"
    Stop=True
    Status.configure(text=statu,fg="Red")
    print("STOP")

def resetit():
    global Stop
    global CurrSessionData
    global statu
    statu="Not Working"
    Status.configure(text=statu,fg="Red")
    Stop=True
    CurrSessionData.clear()
    for record in stat.get_children():
        stat.delete(record)
    
def destroy():
    pop.destroy()
def Inst():
    global pop
    pop=Toplevel(window)
    pop.title("Instructions")
    pop.wm_iconbitmap("pokeball.ico")
    pop.geometry("720x480")
    Ok=Button(pop,text="OK!",command=destroy)
    Line1=Label(pop,text="This tool will help you to stay on track with your hunting current hunting session.",font=("Poppins Regural", 18 * -1))
    How=LabelFrame(pop,text="How to use",font=("Poppins Bold", 22 * -1))
    Line2=Label(pop,text="1. Keep your client's resolution windowed on 1280 x 720.",font=("Poppins Regural", 18 * -1))
    Line3=Label(pop,text="2. Now you will need to set up your coordinates, we will be targeting",font=("Poppins Regural", 18 * -1))
    Line4=Label(pop,text="'Wild X' in your battle window,to do that we will use 2 buttons",font=("Poppins Regural", 18 * -1))
    Line5=Label(pop,text="[Top Left Coord] [Bottom Right Coord] ",font=("Poppins Regural", 18 * -1))
    Line6=Label(pop,text="[Top Left Coord] : Click it and then click on the top area before the",font=("Poppins Regural", 18 * -1))
    Line7=Label(pop,text="'W' in 'Wild',[Bottom Right Coord] same as before but for bottom are after ",font=("Poppins Regural", 18 * -1))
    Line8=Label(pop,text="Pokemon name, after that just click Start!",font=("Poppins Regural", 18 * -1))
    Line9=Label(pop,text="Stop will stop the program and won't count,",font=("Poppins Regural", 18 * -1))
    Line10=Label(pop,text="Reset will remove all enteries and will stop the program.",font=("Poppins Regural", 18 * -1))
    Line11=Label(pop,text="Enjoy hunting :D",font=("Poppins Regural", 22 * -1))

    
    
  
    Line1.pack()
    How.pack()
    Line2.pack()
    Line3.pack()
    Line4.pack()
    Line5.pack()
    Line6.pack()
    Line7.pack()
    Line8.pack()
    Line9.pack()
    Line10.pack()
    Line11.pack()
    Ok.pack()
    
    
def GetTopLeft():
    while True:
        x, y = pyautogui.position()
        if(mouse.is_pressed("left")):
            global PosXMax,PosYMax
            PosXMax=x
            PosYMax=y
            print(PosXMax," ",PosYMax)
            break
def GetBotRight():
    while True:
        x, y = pyautogui.position()
        if(mouse.is_pressed("left")):
            global PosXMin,PosYMin
            PosXMin=x
            PosYMin=y
            break    

def OCR(PosXMax,PosYMax,PosXMin,PosYMin):

    t=""
    sc = pyautogui.screenshot().crop((PosXMax,PosYMax,PosXMin,PosYMin))
    #sc.save("test.png") 
    sc = sc.convert('RGBA') 
    data = np.array(sc)
    r, g, b, t = data.T
    out_areas = r <= 200
    text_areas = r > 200
    data[..., :-1][out_areas.T] = (252, 252, 252)
    data[..., :-1][text_areas.T] = (0, 0, 0)
    sc = Image.fromarray(data)
    #sc.save("After.png") 
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    t = pytesseract.image_to_string(sc)
    if t!="":
        X=t.split()
        t=X[1]
    return t


def UpdateCount():
    for record in stat.get_children():
        stat.delete(record)
    
    for i,a in enumerate(CurrSessionData):
        perc=float(CurrSessionData[a]/Counter)
        perc=perc*100
        stat.insert(parent='',index='end',iid=i,values=(a,CurrSessionData[a],perc))
    

    
def StartCount():
        
    while True:
        if not Stop:
            global Counter
            global OneAtATime
            Encounter=OCR(PosXMax,PosYMax,PosXMin,PosYMin) #Reading the Name of the Pokemon
            Hay=np.array(pyautogui.screenshot()) #Full Screen Screenshot converted to np so CV2 can use it
            Hay = Hay[:, :, ::-1].copy() #Fixing Colours
            Needle=cv2.imread("Needle.png") #Our needle will be the VS in battle window, to avoid multiple encounters
            Needle2=cv2.imread("Map.png")#Checks for the map so it break the script when you minimize
            
            result=cv2.matchTemplate(Hay,Needle,cv2.TM_CCOEFF_NORMED) #Finding VS
            bug=cv2.matchTemplate(Hay,Needle2,cv2.TM_CCOEFF_NORMED)
            bugtest=cv2.matchTemplate(Hay,Needle2,cv2.TM_CCOEFF_NORMED)
            min_val2, max_val2, min_loc2, max_loc2 = cv2.minMaxLoc(bugtest)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # print(max_val) #If found will be 99%

            if(max_val2<0.80):
                endit()
                continue
            if(Encounter !=""):
                
                if Encounter in CurrSessionData and OneAtATime==True:  #Adding Data to Dic if Not first encounter
                    CurrSessionData[Encounter]+=1
                    Counter+=1
                
                elif Encounter not in CurrSessionData and OneAtATime==True: #if first add its data
                    CurrSessionData.update({Encounter: 1})
                    Counter+=1
                
            
            
            if(max_val < 0.90 and Encounter=="") : #Checking the VS if its not there the bool will be true, and will freeze the counter above
                OneAtATime=True
                
                    
            elif OneAtATime==True and Encounter !="": #There is a new encounter print it
                print(Encounter.strip(),"Has been seen: ",CurrSessionData[Encounter],"Times",sep=" ")
                print(Counter)
                counter.configure(text=Counter)
                UpdateCount()

                
                #print("Has been seen: ")
                #print(CurrSessionData[Encounter])
                #print("Times")  
                OneAtATime=False   

    
def StartIt():
    global Stop
    global statu
    Stop = False
    
    print("Start")
    statu="Working"
    Status.configure(text=statu,fg="Green")
    
   
threading.Thread(target=StartCount).start() 



Instruction=Button(window,text="Instructions",width=18,command=Inst)
TopL=Button(window,text="Top Left Coord",command=GetTopLeft)
BotR=Button(window,text="Bottom Right Coord",command=GetBotRight)
Total=Label(window,text="Total Encounters",font=("Poppins Regular", 22 * -1))
counter=Label(window,text=str(Counter),font=("Poppins Regular", 20 * -1))
Status=Label(window,text=statu,font=("Poppins Bold", 26 * -1),fg="Red")
counter.grid(row=4,column=0,pady=2,sticky="NSEW")
Start=Button(window,text="Start",width=18,command=StartIt)
Stop=Button(window,text="Stop",width=18,command=endit)
Reset=Button(window,text="Reset",width=18,command=resetit)
rowcnt=0
colcnt=0
 

    


Buttons=[Instruction,TopL,BotR,Total,counter,Start,Stop,Reset,stat,Status]

for button in Buttons:
    Grid.rowconfigure(window,rowcnt,weight=1)
    #Grid.columnconfigure(window,colcnt,weight=1)
    rowcnt+=1
    #colcnt+=1
 
 


    

Instruction.grid(row=0,column=0,pady=2,sticky="NSEW")
TopL.grid(row=1,column=0,pady=2,sticky="NSEW")
BotR.grid(row=2,column=0,pady=2,sticky="NSEW")
Total.grid(row=3,column=0,pady=2,sticky="NSEW")
Status.grid(row=3,column=1,sticky="NSEW")
Start.grid(row=5,column=0,pady=2,sticky="NSEW")
Stop.grid(row=6,column=0,pady=2,sticky="NSEW")
Reset.grid(row=7,column=0,pady=2,sticky="NSEW")
stat.grid(row=0,column=1,pady=2,sticky="NSEW")
window.mainloop() 
