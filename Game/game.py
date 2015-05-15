import tkinter as tk
import random
import socket
import socketserver

gameType = 'onePlayer'
isHost = False
isClient = True
"""
#server
class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        self.request.sendall(self.data.upper())

if isHost:
    server = socketserver.TCPServer(('localhost', 1337), MyTCPHandler)
    server.serve_forever()
else:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 1337))

while True:
    sock.sendall(bytes('smurf\n', 'utf-8'))
    received = str(sock.recv(1024), "utf-8")
# server end
"""
class Menu(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.button = tk.Button(self, text="One Player",
                                command=self.onePlayer)
        self.button.pack(side="top")
        self.host = tk.Button(self, text="Host",
                                command=self.host)
        self.host.pack(side="bottom", fill='both')
        self.client = tk.Button(self, text="Client",
                                command=self.client)
        self.client.pack(side="bottom", fill='both')
        self.gameArray = []
        self.master.geometry("245x150+300+300")
        self.master.title('Mastermind 3000')
        self.pack()

    def onePlayer(self):
        try:
            if self.gameArray:
                self.gameArray.pop().master.destroy()
        except:
            pass
        gameType = 'onePlayer'
        self.gameArray.append(Game(master=tk.Tk()))

    def host(self):
        global isHost
        global isClient
        try:
            if self.gameArray:
                self.gameArray.pop().master.destroy()
        except:
            pass
        isHost = True
        isClient = False
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
        self.mainButtonFound = [0,0,0,0]
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
        print('Game Over, you loose') # needs to be implemented

    def winner(self):
        print('You Win!')

    def nextRound(self,button):
        def nextRoundCallback():
            canContinue = True
            for x in range(4):
                if self.buttonArray[self.currentRow][x][0] < 0:
                    canContinue = False
            if canContinue:
                hasWon = True
                for x in range(4):
                    if self.buttonArray[self.currentRow][x][0] == self.mainColorArray[x][0]:
                        self.mainButtons[x].configure(bg = self.colorArray[self.mainColorArray[x][0]])
                        self.mainButtonFound[x] = 1
                    else:
                        hasWon = False
                    self.buttonArray[self.currentRow][x][1] = 0 # make the row that was just finished inactive
                if hasWon:
                    self.winner()
                self.currentRow += 1
            if self.currentRow >= 12:
                self.gameOver()
            else:
                self.createRows()
        return nextRoundCallback

    def createRows(self):
        for row in range(self.currentRow,self.currentRow + 1):
            for col in range(4):
                buttonColor = self.colorArray[self.buttonArray[row][col][0]]
                if self.buttonArray[row][col][0] == -1:
                    if self.mainButtonFound[col]:
                        #if the button has been found before he keeps his color but you are able to change it if you want
                        buttonColor = self.colorArray[self.mainColorArray[col][0]]
                        self.buttonArray[row][col][0] = self.mainColorArray[col][0]
                    else:
                        buttonColor = 'white'
                if isHost:
                    self.buttonArray[self.currentRow][col][1] = 0
                self.pin = tk.Button(self, bg = buttonColor )
                self.pin["text"] = '     '
                self.pin["command"] = self.changeColor(self.pin, row, col)
                self.pin.grid(row=row,column=col,padx=3,pady=3)

    def hostSubmits(self):
        def callback():
            #check if all pins are selected
            for x in range(4):
                if self.mainColorArray[x][0] < 0:
                    return
            for x in range(4):
                self.mainColorArray[x][1] = 0
            #send client the colors
        return callback

    def submitbutton(self):
        self.submit = tk.Button(self,bg = 'white')
        self.submit['text'] = 'Submit'
        if isHost:
            self.submit["command"] = self.hostSubmits()
        else:
            self.submit["command"] = self.nextRound(self.submit)
        self.submit.grid(row=12, column = 5)

    def changeMainColor(self, button, row):
        #changes the color of the 'button' after a click event is created
        def colorCallback():
            if self.mainColorArray[row][1] == 0:
                return
            colorNumber = self.mainColorArray[row][0]
            colorNumber = (colorNumber + 1) % 5
            self.mainColorArray[row][0] = colorNumber
            color = self.colorArray[colorNumber]
            button.configure(bg = color )
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
