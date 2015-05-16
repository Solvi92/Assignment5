import tkinter as tk
import tkinter.messagebox
import random
import socket
import socketserver
import threading
import time
import ast
from collections import Counter

gameType = 'onePlayer'
isHost = False
isClient = True
serverData = ''
clientData = ''

#server
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global clientData
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes(serverData, 'utf-8')
        self.request.sendall(response)
        print('data:', data)
        clientData = data
        print('response:', response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def serverClient(ip, port, message):
    global serverData
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        print('sending:', message)
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        if not response == 'dummy':
            serverData = response
        print("Received: {}".format(response))
    finally:
        sock.close()

def startServer():
    HOST, PORT = "localhost", 1338

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    #server.shutdown()


class Menu(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title('Mastermind 3000')
        self.background = tk.PhotoImage(file=r"C:\Users\Lenovo\desktop\ble.gif")
        self.background_label = tk.Label(self.master,image=self.background)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.button = tk.Button(self.master, text="One Player",bg='green',
                                command=self.onePlayer).pack(fill='both',pady=(160,0),padx=(100,100))
        self.host = tk.Button(self.master, text="Host",bg='green',
                                command=self.host).pack(side="top", fill='both',padx=(100,100))
        self.client = tk.Button(self.master, text="Client",bg='green',
                                command=self.client).pack(side="top", fill='both',padx=(100,100))
        self.gameArray = []


        self.master.geometry("440x440+20+40")
        self.pack()

    def onePlayer(self):
        try:
            if self.gameArray:
                self.gameArray.pop().master.destroy()
        except:
            print('Something went wrong connecting the client')
        gameType = 'onePlayer'
        self.gameArray.append(Game(master=tk.Tk()))

    def host(self):
        global isHost
        global isClient
        isHost = True
        isClient = False
        try:
            if self.gameArray:
                self.gameArray.pop().master.destroy()
        except:
            print('Something went wrong connecting the host')
        startServer()
        self.gameArray.append(Game(master=tk.Tk()))

    def client(self):
        global isClient
        global isHost
        isClient = True
        isHost = False
        try:
            if self.gameArray:
                self.gameArray.pop().master.destroy()
        except:
            pass
        self.gameArray.append(Game(master=tk.Tk()))

class Game(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # initialize the window
        self.buttonArray = [[[-1,1] for x in range(4)] for x in range(12)] # the game board which is 4x12
        self.mainColorArray = [[-1,1] for x in range(4)] # This is where the correct colors is displayed or selected
        self.mainButtons = []
        self.correctPins = [[[] for x in range(4)] for x in range(12)]
        self.pinManager = [0,0,0,0]
        self.currentRow = 0 # turn counter
        self.colorArray = ['yellow','red','green','blue','purple'] # possible colors
        self.master.geometry("245x420+300+300")

        self.pack()
        self.createMainRow()
        self.createRows()
        self.submitbutton()

        self.master.title('Mastermind 3000')

    def getRandomColorNumber(self):
        color = random.randint(0,len(self.colorArray)-1)
        return color

    def changeColor(self,button,row,col):
        #changes the color of the 'button' after a click event is created
        def colorCallback():
            if self.buttonArray[row][col][1] == 0:
                return # the button is inactive
            colorNumber = self.buttonArray[row][col][0]
            colorNumber = (colorNumber + 1) % 5
            self.buttonArray[row][col][0] = colorNumber
            color = self.colorArray[colorNumber]
            button.configure(bg = color )
        return colorCallback

    def gameOver(self):
        tkinter.messagebox.showinfo('Mastermind','You Lose')
        self.master.destroy()

    def winner(self):
        for x in range(4):
            self.mainButtons[x].configure(bg = self.colorArray[self.mainColorArray[x][0]])
        tkinter.messagebox.showinfo('Mastermind','You Win')
        self.master.destroy()

    def putClientDataInArray(self, data):
        data = ast.literal_eval(data)
        for row in range(self.currentRow,self.currentRow + 1):
            for col in range(4):
                self.buttonArray[row][col][0] = int(data[row][col][0])

    def getCorrectData(self, data):
        return data[:-1], int(data[-1])

    def nextRound(self):
        def nextRoundCallback():
            if isClient:
                serverClient('localhost', 1338, str(self.buttonArray) + str(self.currentRow))
            print('serverData:', serverData)
            if isClient and not serverData == '':
                for x in range(4):
                    self.mainColorArray[x][0] = int(serverData[x])

            canContinue = True
            for x in range(4):
                if self.buttonArray[self.currentRow][x][0] < 0:
                    canContinue = False
            if canContinue:
                hasWon = True
                #Dict for the occurrences of colors in the mainColorArray
                colors = Counter([x[0] for x in self.mainColorArray])
                #Checking for the correct color and position
                print(self.mainColorArray)
                print(self.buttonArray[self.currentRow])
                for x in range(4):
                    if self.buttonArray[self.currentRow][x][0] == self.mainColorArray[x][0] and not colors[self.buttonArray[self.currentRow][x][0]] == 0:
                        self.pinManager[x] = 1
                        colors[self.buttonArray[self.currentRow][x][0]] -= 1
                    else:
                        hasWon = False
                #Checking for correct color but wrong position
                for x in range(4):
                    for i in range(4):
                        if self.buttonArray[self.currentRow][x][0] == self.mainColorArray[i][0]:
                            if not self.pinManager[x] == 1 and not colors[self.buttonArray[self.currentRow][x][0]] == 0:
                                self.pinManager[x] = 2
                                colors[self.buttonArray[self.currentRow][x][0]] -= 1
                    self.buttonArray[self.currentRow][x][1] = 0 # make the row that was just finished inactive
                if hasWon:
                    self.winner()
                    return
                self.currentRow += 1
            if self.currentRow >= 12:
                self.gameOver()
                return
            else:
                print('Next Round')
                self.changeCorrectPins()
                self.createRows()
        return nextRoundCallback

    def changeCorrectPins(self):
        for row in range(self.currentRow - 1,self.currentRow):
            for col in range(4):
                if sorted(self.pinManager,reverse=True)[col] == 1:
                    self.correctPins[row][col][0].configure(bg = 'green')
                elif sorted(self.pinManager,reverse=True)[col] == 2:
                    self.correctPins[row][col][0].configure(bg = 'black')
        self.pinManager = [0,0,0,0]

    def createRows(self):
        for row in range(self.currentRow,self.currentRow + 1):
            for col in range(4):
                buttonColor = self.colorArray[self.buttonArray[row][col][0]]
                if self.buttonArray[row][col][0] == -1:
                        buttonColor = 'white'
                if isHost:
                    self.buttonArray[self.currentRow][col][1] = 0
                #Create the main buttons
                self.pin = tk.Button(self, bg = buttonColor )
                self.pin["text"] = '     '
                self.pin["command"] = self.changeColor(self.pin, row, col)
                self.pin.grid(row=row,column=col,padx=3,pady=3)

                #Create the correct buttons
                self.pinC = tk.Button(self, bg = 'white')
                self.pinC['text'] = ''
                self.pinC.grid(row=row, column=col+4, padx=1, pady=1)
                self.correctPins[row][col].append(self.pinC)

    def hostSubmits(self):
        def callback():
            global serverData
            global clientData
            #check if all pins are selected
            for x in range(4):
                if self.mainColorArray[x][0] < 0:
                    return
            for x in range(4):
                self.mainColorArray[x][1] = 0
                serverData += str(self.mainColorArray[x][0])
            #send client the colors
            serverClient('localhost', 1338, 'dummy')
            print('calling nextRound')
            #get game board from client
            print('waiting for clientData...')
            while clientData == '' or clientData == 'dummy':
                time.sleep(2)
            print('clientData is here:')
            data, self.currentRow = self.getCorrectData(clientData)
            self.putClientDataInArray(data)
            print(data)
            print(self.currentRow)
            self.putClientDataInArray(data)
            self.createRows()
            tmp = self.nextRound()
            tmp()
            clientData = ''

        return callback

    def submitbutton(self):
        self.submit = tk.Button(self,bg = 'white')
        self.submit['text'] = 'Submit'
        if isHost:
            self.submit["command"] = self.hostSubmits()
        else:
            self.submit["command"] = self.nextRound()
        self.submit.grid(row=12, column = 9)

    def changeMainColor(self, button, row):
        #changes the color of the 'button' after a click event is created
        def colorCallback():
            if self.mainColorArray[row][1] == 0:
                return
            colorNumber = self.mainColorArray[row][0]
            colorNumber = (colorNumber + 1) % 5
            self.mainColorArray[row][0] = colorNumber
            color = self.colorArray[colorNumber]
            button.configure(bg = color)
        return colorCallback

    def createMainRow(self):
        for row in range(4):
            if isHost:
                self.pin = tk.Button(self,bg = 'white')
                self.pin["command"] = self.changeMainColor(self.pin, row)
            else:
                self.mainColorArray[row][0] = self.getRandomColorNumber()
                self.pin = tk.Button(self,bg = 'white')
            self.pin["text"] = '     '
            self.pin.grid(row=12, column=row,padx=3,pady=3)
            self.mainButtons.append(self.pin)
            print(self.mainColorArray[row][0])

root = tk.Tk()
menu = Menu(master=root)
menu.mainloop()
