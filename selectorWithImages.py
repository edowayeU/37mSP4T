from urllib.request import urlopen
import tkinter as tk
from tkinter import messagebox
import datetime
from tkinter import *
from PIL import ImageTk, Image
import threading
import time

#State 1 = W #State 2 = Q #State 3 = K

class loadGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Reciever Selector")
        self.root.geometry("800x800")
        self.how = 1

        size =300

    

        #self.label = tk.Label(self.root, text=f"Current Reciever: K-Band", font=('Arial',18))
        #self.label.pack()
        #when switch is connected change that line to this:
        
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

        #second polarization

        self.WImage2 = Image.open("WBand.drawio.png").resize((size,size))
        self.WImage2 = ImageTk.PhotoImage(self.WImage2)

        self.QImage2 = Image.open("QBand.drawio.png").resize((size,size))
        self.QImage2 = ImageTk.PhotoImage(self.QImage2)

        self.KImage2 = Image.open("KBand.drawio.png").resize((size,size))
        self.KImage2 = ImageTk.PhotoImage(self.KImage2)

        self.unselectedImage2 = Image.open("noneConnected.drawio.png").resize((size,size))
        self.unselectedImage2 = ImageTk.PhotoImage(self.unselectedImage2)

        self.noImage2 = Image.open("none.drawio.png")
        self.noImage2 = ImageTk.PhotoImage(self.noImage2) 


        self.panel = Label(self.root, image = self.unselectedImage)
        self.panel.pack(fill = "x", expand = "yes" ,pady= 20)
        self.panel2 = Label(self.root, image = self.unselectedImage2)
        self.panel2.pack(fill = "x", expand = "yes" ,pady= 20)



        recieverFrame = tk.Frame(self.root)
        recieverFrame.columnconfigure(0,weight=1)
        recieverFrame.columnconfigure(1,weight=1)
        recieverFrame.columnconfigure(2,weight=1)

        self.WButton = tk.Button(recieverFrame, text = "W-Band", font=('Arial',16), command=self.selectW)
        self.WButton.grid(row=0,column=0, padx=20, pady=20)

        self.QButton = tk.Button(recieverFrame, text = "Q-Band", font=('Arial',16), command=self.selectQ)
        self.QButton.grid(row=0,column=1, padx=20, pady=20)

        self.KButton = tk.Button(recieverFrame, text = "K-Band", font=('Arial',16), command=self.selectK)
        self.KButton.grid(row=0,column=2, padx=20, pady=20)

        self.orig_color = self.KButton.cget("background")
        

        recieverFrame.pack()

        disconnectButton = tk.Button(self.root, text="DISCONNECT current reciever", command=self.disconnect)
        disconnectButton.pack(side="bottom", anchor="w", padx=10, pady=10)


        currentState=self.getState()
        self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
        self.label.pack()

        threading.Thread(target=self.constantCheck).start()

        self.root.mainloop()

    def disconnect(self):
        if messagebox.askyesno(title="Disconnect", message="Do you want to disconnect the reciever?"):
            send = "SP4TA:STATE:0"
            currentState = self.getState()
            if currentState == 'No Reciever Connected':
                messagebox.showinfo(title="Error",message=f"Reciever already disconnected.")
            else:
                self.Get_HTTP_command(send)
                messagebox.showinfo(title="Success", message="Reciever Disconnected")
            self.updateLable(send)
            self.WButton.config(bg=self.orig_color)
            self.QButton.config(bg=self.orig_color)
            self.KButton.config(bg=self.orig_color) 
        
    def constantCheck(self):
        waiting4Input = True
        while waiting4Input:
            try:
                time.sleep(1)
                currentState = self.Get_HTTP_command("SP4TA:STATE?").decode()
                self.getState()
                if currentState== '1':
                    currentState = "W Band"
                    self.WButton.config(bg='green')
                    self.QButton.config(bg='red')
                    self.KButton.config(bg='red')  
                    self.panel.config(image=self.WImage) 
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how = 2
                elif currentState == '2':
                    currentState = "Q Band"
                    self.WButton.config(bg='red')
                    self.QButton.config(bg='green')
                    self.KButton.config(bg='red')
                    self.panel.config(image=self.QImage) 
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
                    self.how = 2
                elif currentState == '3':
                    currentState = "K Band"
                    self.WButton.config(bg='red')
                    self.QButton.config(bg='red')
                    self.KButton.config(bg='green')
                    self.panel.config(image=self.KImage)
                    self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18)) 
                    self.how = 2
                else:
                    currentState = "No Reciever Connected"
                    send = "SP4TA:STATE:0"
                    self.panel.config(image=self.unselectedImage) 
                    self.WButton.config(bg=self.orig_color)
                    self.QButton.config(bg=self.orig_color)
                    self.KButton.config(bg=self.orig_color) 
                    self.updateLable(send)
                    self.how = 2
                
            except:
                self.panel.config(image=self.noImage) 
                if self.how == 2:
                    print ("Error, no response from device; check IP address, connections, and that device is on.")
                    self.label.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
                    self.how = 1
                currentState = "No Response"
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 

        

    def getState(self):
        try:
            currentState = self.Get_HTTP_command("SP4TA:STATE?").decode()
            if currentState== '1':
                currentState = "W Band"
                self.WButton.config(bg='green')
                self.QButton.config(bg='red')
                self.KButton.config(bg='red')  
                self.panel.config(image=self.WImage) 
            elif currentState == '2':
                currentState = "Q Band"
                self.WButton.config(bg='red')
                self.QButton.config(bg='green')
                self.KButton.config(bg='red')
                self.panel.config(image=self.QImage) 
            elif currentState == '3':
                currentState = "K Band"
                self.WButton.config(bg='red')
                self.QButton.config(bg='red')
                self.KButton.config(bg='green')
                self.panel.config(image=self.KImage) 
            else:
                currentState = "No Reciever Connected"
                self.panel.config(image=self.unselectedImage) 
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 
            return currentState
        except:
            print ("Error, no response from device; check IP address, connections, and that device is on.")
            self.label.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
            currentState = "No Response"
            self.panel.config(image=self.noImage) 
            self.WButton.config(bg=self.orig_color)
            self.QButton.config(bg=self.orig_color)
            self.KButton.config(bg=self.orig_color) 

    def invalidCommand(self, CmdToSend, type):
        if type == 1:
            messagebox.showinfo(title="Error",message=f"Command not found: {CmdToSend}")
        if type == 2:
            if self.how ==2:
                self.panel.config(image=self.noImage) 
                self.WButton.config(bg=self.orig_color)
                self.QButton.config(bg=self.orig_color)
                self.KButton.config(bg=self.orig_color) 
                messagebox.showinfo(title="Error",message=f"Error, no response from device; check IP address and connections.")
                self.how = 1

    def Get_HTTP_command(self, CmdToSend):
    #ip address of the switch
        CmdToSend = "http://192.168.100.100/:" + CmdToSend

    #send the http command and read the result
        try:
            HTTP_Result = urlopen(CmdToSend, timeout=5)
            PTE_Return = HTTP_Result.read()

            if len(PTE_Return) > 100:
                self.invalidCommand(CmdToSend, 1)
                PTE_Return = "Invalid Command!"
        except:
            self.label.config(text=f"No response from device; check IP address and connections.", font=('Arial',18)) 
            currentState = "No Response"
            self.invalidCommand(CmdToSend, 2)
            PTE_Return = "No Response!"
            

        return PTE_Return

    def selectW(self):
        cmdSent = "SP4TA:STATE:1"
        currentState = self.getState()
        if currentState == 'W Band':
            messagebox.showinfo(title="Error",message=f"W Reciever already selected.")
        else:
            self.Get_HTTP_command("SP4TA:STATE:1")
        #with open("stateLog.txt", "a") as f: #
            #time = datetime.datetime.now() #
            #time = time.strftime("%m-%d-%Y %H:%M:%S, W-Band Selected. SP4TA:STATE:1 \n")#
        # f.write(time) #
    # self.label.config(text="Current Receiver: W-Band") #
            self.WButton.config(bg='green')
            self.QButton.config(bg='red')
            self.KButton.config(bg='red')
        #WHEN SWITCH IS CONNECTED ADD THIS LINE:
            self.updateLable(cmdSent)
        #AND GET RID OF LINES WITH HASHTAG (#)

    def selectQ(self):
        cmdSent = "SP4TA:STATE:2"
        currentState = self.getState()
        if currentState == 'Q Band':
            messagebox.showinfo(title="Error",message=f"Q Reciever already selected.")
        else:
            self.Get_HTTP_command("SP4TA:STATE:2")
        # with open("stateLog.txt", "a") as f: #
        #  time = datetime.datetime.now() #
        # time = time.strftime("%m-%d-%Y %H:%M:%S, Q-Band Selected. SP4TA:STATE:2 \n")#
            #f.write(time) #
        # self.label.config(text="Current Receiver: Q-Band") #
            self.WButton.config(bg='red')
            self.QButton.config(bg='green')
            self.KButton.config(bg='red')
        #WHEN SWITCH IS CONNECTED ADD THIS LINE:
            self.updateLable(cmdSent)
        #AND GET RID OF LINES WITH HASHTAG (#)

    def selectK(self):
        cmdSent = "SP4TA:STATE:3"
        currentState = self.getState()
        if currentState == 'K Band':
            messagebox.showinfo(title="Error",message=f"K Reciever already selected.")
        else:
            self.Get_HTTP_command("SP4TA:STATE:3")
        # with open("stateLog.txt", "a") as f: #
        #  time = datetime.datetime.now() #
        # time = time.strftime("%m-%d-%Y %H:%M:%S, K-Band Selected. SP4TA:STATE:3 \n")#
            #f.write(time) #
        # self.label.config(text="Current Receiver: K-Band") #
            self.WButton.config(bg='red')
            self.QButton.config(bg='red')
            self.KButton.config(bg='green')
        #WHEN SWITCH IS CONNECTED ADD THIS LINE:
            self.updateLable(cmdSent)
        #AND GET RID OF LINES WITH HASHTAG (#)

    def updateLable(self, cmdSent):
        currentState=self.getState()
        self.label.config(text=f"Current Reciever: {currentState}", font=('Arial',18))
        with open("stateLog.txt", "a") as f:
            time = datetime.datetime.now()
            time = time.strftime("%m-%d-%Y %H:%M:%S")
            if currentState == 'No Reciever Connected':
                f.write(time + ", Reciever Disconnected. Command: " + cmdSent + "\n")
            else:
                f.write(time + ", " + currentState + " selected. Command: " + cmdSent + "\n")

def Get_HTTP_command(CmdToSend):

    # Specify the IP address of the switch box
    CmdToSend = "http://192.168.100.100/:" + CmdToSend

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
        print("Select Reciever (W/Q/K/Disconnect): ")
        cmd = input()
        if cmd == 'w' or cmd == 'W':
            Get_HTTP_command('SP4TA:STATE:1')

        elif cmd == 'q' or cmd == 'Q':
            Get_HTTP_command('SP4TA:STATE:2')

        elif cmd == 'k' or cmd == 'K':
            Get_HTTP_command('SP4TA:STATE:3')

        elif cmd == 'd' or cmd == 'D' or cmd == 'disconnect':
            Get_HTTP_command('SP4TA:STATE:0')

        else:
            print("Invalid input. Valid inputs: 'w','W','q','Q','k','K','d','D','disconnect'")

waiting4Input = True
cmd = 'n/a'
print(cmd)
threading.Thread(target=getInput).start()

loadGUI()