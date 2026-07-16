from urllib.request import urlopen
from urllib.error import URLError
import tkinter as tk
from tkinter import messagebox
import datetime
from tkinter import *
from PIL import ImageTk, Image
import threading
from tkinter import ttk
import time

#State 1 = W #State 2 = Q #State 3 = K

class loadGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reciever Selector")
        self.root.geometry("800x1600")
        self.how = 1
        self.how2 = 1

        size =300

    

        #self.label = tk.Label(self.root, text=f"Current Reciever: K-Band", font=('Arial',18))
        #self.label.pack()
        #when switch is connected change that line to this:

        self.titleA = tk.Label(self.root, text="Switch A", font=("Arial", 24, "bold"))
        self.titleA.pack()
        
        self.label = tk.Label(self.root, text=f"Current Reciever: ", font=('Arial',18))
        self.label.pack()

        self.WImage = Image.open("WBand.drawio.png").resize((size,size))
        self.WImage = ImageTk.PhotoImage(self.WImage)

        self.QImage = Image.open("QBand.drawio.png").resize((size,size))
        self.QImage = ImageTk.PhotoImage(self.QImage)

        self.KImage = Image.open("KBand.drawio.png").resize((size,size))
        self.KImage = ImageTk.PhotoImage(self.KImage)

        self.unselectedImage = Image.open("noneConnected.drawio.png").resize((size,size))
        self.unselectedImage = ImageTk.PhotoImage(self.unselectedImage)

        self.noImage = Image.open("none.drawio.png").resize((size,size))
        self.noImage = ImageTk.PhotoImage(self.noImage)

        self.panel = Label(self.root, image = self.unselectedImage)
        self.panel.pack(fill = "x", expand = "yes" ,pady= 20)
        



        recieverFrame = tk.Frame(self.root)
        recieverFrame.columnconfigure(0,weight=1)
        recieverFrame.columnconfigure(1,weight=1)
        recieverFrame.columnconfigure(2,weight=1)

        self.WButton = tk.Button(recieverFrame, text = "W-Band", font=('Arial',16), command=lambda: self.selectW("A"))
        self.WButton.grid(row=0,column=0, padx=20, pady=20)

        self.QButton = tk.Button(recieverFrame, text = "Q-Band", font=('Arial',16), command=lambda: self.selectQ("A"))
        self.QButton.grid(row=0,column=1, padx=20, pady=20)

        self.KButton = tk.Button(recieverFrame, text = "K-Band", font=('Arial',16), command=lambda: self.selectK("A"))
        self.KButton.grid(row=0,column=2, padx=20, pady=20)

        self.orig_color = self.KButton.cget("background")
        
        recieverFrame.pack()

        disconnectButton = tk.Button(self.root, text="DISCONNECT current reciever", command=lambda: self.disconnect("A"))
        disconnectButton.pack(anchor="w", padx=10, pady=10)

        separator = ttk.Separator(self.root,orient='horizontal')
        separator.pack(fill="x",padx=2)


        self.titleB = tk.Label(self.root, text="Switch B", font=("Arial", 24, "bold"))
        self.titleB.pack()

        self.label2 = tk.Label(self.root, text=f"Current Reciever: ", font=('Arial',18))
        self.label2.pack()

        self.panel2 = Label(self.root, image = self.unselectedImage)
        self.panel2.pack(fill = "x", expand = "yes" ,pady= 20)

        recieverFrame2 = tk.Frame(self.root)
        recieverFrame2.columnconfigure(0,weight=1)
        recieverFrame2.columnconfigure(1,weight=1)
        recieverFrame2.columnconfigure(2,weight=1)

        self.WButton2 = tk.Button(recieverFrame2, text = "W-Band", font=('Arial',16), command=lambda: self.selectW("B"))
        self.WButton2.grid(row=0,column=0, padx=20, pady=20)

        self.QButton2 = tk.Button(recieverFrame2, text = "Q-Band", font=('Arial',16), command=lambda: self.selectQ("B"))
        self.QButton2.grid(row=0,column=1, padx=20, pady=20)

        self.KButton2 = tk.Button(recieverFrame2, text = "K-Band", font=('Arial',16), command=lambda: self.selectK("B"))
        self.KButton2.grid(row=0,column=2, padx=20, pady=20)

        recieverFrame2.pack()

        disconnectButton2 = tk.Button(self.root, text="DISCONNECT current reciever", command=lambda: self.disconnect("B"))
        disconnectButton2.pack(side="bottom", anchor="w", padx=10, pady=10)


        currentStateA=self.getState("A")
        self.label.config(text=f"Current Reciever: {currentStateA}", font=('Arial',18))
        self.label.pack()

        currentStateB=self.getState("B")
        self.label2.config(text=f"Current Reciever: {currentStateB}", font=('Arial',18))
        self.label2.pack()

        threading.Thread(target=self.constantCheck).start()


        self.root.mainloop()

    def disconnect(self,switch):
        if messagebox.askyesno(title="Disconnect", message="Do you want to disconnect the reciever?"):
            if switch == "A":
                send = "SP4TA:STATE:0"
            elif switch == "B":
                send = "SP4TB:STATE:0"

            currentState = self.getState(switch)
            if currentState == 'No Reciever Connected':
                messagebox.showinfo(title="Error",message=f"Reciever already disconnected.")
            else:
                self.Get_HTTP_command(send)
                messagebox.showinfo(title="Success", message="Reciever Disconnected")
            self.updateLable(switch)
            if switch == "A":
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 
            elif switch == "B":
                self.WButton2.config(bg=self.orig_color)
                self.QButton2.config(bg=self.orig_color)
                self.KButton2.config(bg=self.orig_color) 
        
    def constantCheck(self):
        waiting4Input = True
        while waiting4Input:
            time.sleep(1)
            try:
                self.root.after(0,self.getState,"A")
            except Exception as e:
                print(e)
            try:
                self.root.after(0,self.getState,"B")
            except Exception as e:
                print(e)

    def getState(self, switch):
        try:
            if switch == "A":
                cmd = "SP4TA:STATE?"
            else:
                cmd = "SP4TB:STATE?"
            currentState = self.Get_HTTP_command(cmd).decode()

            if currentState == '1':
                currentState = "W Band"
                if switch == "A":
                    self.WButton.config(bg='green')
                    self.QButton.config(bg=self.orig_color)
                    self.KButton.config(bg=self.orig_color) 
                    self.panel.config(image=self.WImage)
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how = 2
                elif switch == "B":
                    self.WButton2.config(bg='green')
                    self.QButton2.config(bg=self.orig_color)
                    self.KButton2.config(bg=self.orig_color) 
                    self.panel2.config(image=self.WImage) 
                    self.label2.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how2 = 2
            elif currentState == '2':
                currentState = "Q Band"
                if switch == "A":
                    self.QButton.config(bg='green')
                    self.WButton.config(bg=self.orig_color)
                    self.KButton.config(bg=self.orig_color) 
                    self.panel.config(image=self.QImage) 
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how = 2
                elif switch == "B":
                    self.QButton2.config(bg='green')
                    self.WButton2.config(bg=self.orig_color)
                    self.KButton2.config(bg=self.orig_color) 
                    self.panel2.config(image=self.QImage) 
                    self.label2.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how2 = 2
            elif currentState == '3':
                currentState = "K Band"
                if switch == "A":
                    self.KButton.config(bg='green')
                    self.WButton.config(bg=self.orig_color)
                    self.QButton.config(bg=self.orig_color) 
                    self.panel.config(image=self.KImage) 
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how = 2
                elif switch == "B":
                    self.KButton2.config(bg='green')
                    self.QButton2.config(bg=self.orig_color)
                    self.WButton2.config(bg=self.orig_color) 
                    self.panel2.config(image=self.KImage) 
                    self.label2.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how2 = 2
            else:
                currentState = "No Reciever Connected"
                if switch == "A":
                    self.WButton.config(bg=self.orig_color)
                    self.QButton.config(bg=self.orig_color)
                    self.KButton.config(bg=self.orig_color) 
                    self.panel.config(image=self.unselectedImage) 
                    self.how = 2
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                elif switch == "B":
                    self.WButton2.config(bg=self.orig_color)
                    self.QButton2.config(bg=self.orig_color)
                    self.KButton2.config(bg=self.orig_color) 
                    self.panel2.config(image=self.unselectedImage) 
                    self.how2 = 2
                    self.label2.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
            return currentState
        except:
            print ("Error, no response from device; check IP address, connections, and that device is on.")
            if switch == "A":
                self.label.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
                self.panel.config(image=self.noImage) 
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 
            if switch == "B":
                self.label2.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
                self.panel2.config(image=self.noImage) 
                self.WButton2.config(bg=self.orig_color)
                self.QButton2.config(bg=self.orig_color)
                self.KButton2.config(bg=self.orig_color)
            currentState = "No Response"
            

    def invalidCommand(self, CmdToSend, type):
        if type == 1:
            messagebox.showinfo(title="Error",message=f"Command not found: {CmdToSend}")
        if type == 2:
            if self.how ==2 and self.how2 == 2:
                self.panel.config(image=self.noImage) 
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 
                self.panel2.config(image=self.noImage) 
                self.WButton2.config(bg=self.orig_color)
                self.QButton2.config(bg=self.orig_color)
                self.KButton2.config(bg=self.orig_color) 
                messagebox.showinfo(title="Error",message=f"Error, no response from device; check IP address and connections.")
                self.how = 1
                self.how2 = 1

    def Get_HTTP_command(self, CmdToSend):
    #ip address of the switch
        CmdToSend = "http://172.30.14.12/:" + CmdToSend

    #send the http command and read the result
        try:
            HTTP_Result = urlopen(CmdToSend, timeout=5)
            PTE_Return = HTTP_Result.read()

            if len(PTE_Return) > 100:
                self.invalidCommand(CmdToSend, 1)
                PTE_Return = b"Invalid Command!"
        except:
            self.label.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
            currentState = "No Response"
            self.invalidCommand(CmdToSend, 2)
            PTE_Return = b"No Response!"
            

        return PTE_Return

    def selectW(self,switch):
        if switch == "A":
            cmdSent = "SP4TA:STATE:1"
            currentState = self.getState("A")
        elif switch == "B":
            cmdSent = "SP4TB:STATE:1"
            currentState = self.getState("B")
        
        if currentState == 'W Band':
            messagebox.showinfo(title="Error",message=f"W Reciever already selected.")
        else:
            self.Get_HTTP_command(cmdSent)
            if switch == "A":
                self.WButton.config(bg='green')
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color)
            elif switch == "B":
                self.WButton2.config(bg='green')
                self.QButton2.config(bg=self.orig_color)
                self.KButton2.config(bg=self.orig_color)
            self.updateLable(switch)

    def selectQ(self,switch):
        if switch == "A":
            cmdSent = "SP4TA:STATE:2"
            currentState = self.getState("A")
        elif switch == "B":
            cmdSent = "SP4TB:STATE:2"
            currentState = self.getState("B")
        
        if currentState == 'Q Band':
            messagebox.showinfo(title="Error",message=f"Q Reciever already selected.")
        else:
            self.Get_HTTP_command(cmdSent)
            if switch == "A":
                self.QButton.config(bg='green')
                self.WButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color)
            elif switch == "B":
                self.QButton2.config(bg='green')
                self.WButton2.config(bg=self.orig_color)
                self.KButton2.config(bg=self.orig_color)
            self.updateLable(switch)

    def selectK(self,switch):
        if switch == "A":
            cmdSent = "SP4TA:STATE:3"
            currentState = self.getState("A")
        elif switch == "B":
            cmdSent = "SP4TB:STATE:3"
            currentState = self.getState("B")
        
        if currentState == 'K Band':
            messagebox.showinfo(title="Error",message=f"K Reciever already selected.")
        else:
            self.Get_HTTP_command(cmdSent)
            if switch == "A":
                self.KButton.config(bg='green')
                self.QButton.config(bg=self.orig_color)
                self.WButton.config(bg=self.orig_color)
            elif switch == "B":
                self.KButton2.config(bg='green')
                self.QButton2.config(bg=self.orig_color)
                self.WButton2.config(bg=self.orig_color)
            self.updateLable(switch)

    def updateLable(self, switch):
        currentState=self.getState(switch)
        if switch == "A":
            self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
        if switch == "B":
            self.label2.config(text=f"Current Reciever: {currentState}", font=('Arial',18))


def Get_HTTP_command(CmdToSend):

    # Specify the IP address of the switch box
    CmdToSend = "http://172.30.14.12/:" + CmdToSend

    # Send the HTTP command and try to read the result
    try:
        HTTP_Result = urlopen(CmdToSend, timeout=1)
        PTE_Return = HTTP_Result.read()

        # The switch displays a web GUI for unrecognised commands
        if len(PTE_Return) > 100:
            print ("Error, command not found:", CmdToSend)
            PTE_Return = "Invalid Command!"

    # Catch an exception if URL is incorrect (incorrect IP or disconnected)
    except:
        print ("Error, no response from device; check IP address and connections.")
        PTE_Return = "No Response!"
        

    # Return the response
    return PTE_Return

def getInput():

    while waiting4Input:
        print("Select Switch (A/B)")
        switch = input().upper()
        if switch != "A" and switch  != "B":
            print("Invalid input. Valid inputs: 'A' or 'B'")
        else:
            print("Select Reciever (W/Q/K/Disconnect): ")
            cmd = input().upper()
            if cmd == 'W':
                send = "SP4T"+switch+":STATE:1"
                Get_HTTP_command(send)

            elif cmd == 'Q':
                send = "SP4T"+switch+":STATE:2"
                Get_HTTP_command(send)

            elif cmd == 'K':
                send = "SP4T"+switch+":STATE:3"
                Get_HTTP_command(send)

            elif cmd == 'DISCONNECT':
                send = "SP4T"+switch+":STATE:0"
                Get_HTTP_command(send)

            else:
                print("Invalid input. Valid inputs: 'W','Q','K','D','disconnect',")

waiting4Input = True
cmd = ''
print(cmd)
threading.Thread(target=getInput).start()

loadGUI()