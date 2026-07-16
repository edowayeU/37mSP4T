from urllib.request import urlopen


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
            PTE_Return = b"Invalid Command!"

    # Catch an exception if URL is incorrect (incorrect IP or disconnected)
    except:
        print ("Error, no response from device; check IP address and connections.")
        PTE_Return = b"No Response!"
        

    # Return the response
    return PTE_Return

def getState(switch):
    cmd = "SP4T"+switch+":STATE:?"
    currentState = Get_HTTP_command(cmd).decode()
    if currentState == '1':
        currentState = "W Band"        
    elif currentState == '2':
        currentState = "Q Band"      
    elif currentState == '3':
        currentState = "K Band"        
    else:
        currentState = "No Reciever Connected"

    return currentState

while True:
        switchA = getState("A")
        switchB = getState("B")
        print(f"Switch A: {switchA} \nSwitch B: {switchB} \n")

        print("Select Switch (A/B)")
        switch = input().upper()
        if switch != "A" and switch  != "B":
            print("Invalid input. Valid inputs: 'A' or 'B'")
        else:
            print("Select Reciever (W/Q/K/disconnect): ")
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