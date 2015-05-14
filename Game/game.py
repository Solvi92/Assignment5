import tkinter as tk
import random

class Game(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        # initialize the window
        self.buttonArray = [[[-1,1] for x in range(4)] for x in range(12)] # the game board which is 4x12
        self.mainColorArray = [-1,-1,-1,-1] # This is where the correct colors is displayed or selected
        self.mainButtons = []
        self.currentRow = 0 # turn counter
        self.colorArray = ['yellow','red','green','blue','purple'] # possible colors

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
                return # the button should be inactive
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
                    if self.buttonArray[self.currentRow][x][0] == self.mainColorArray[x]:
                        self.mainButtons[x].configure(bg = self.colorArray[self.mainColorArray[x]])
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
                    buttonColor = 'white'
                self.pin = tk.Button(self, bg = buttonColor )
                self.pin["text"] = str(row) + " " + str(col)
                self.pin["command"] = self.changeColor(self.pin, row, col)
                self.pin.grid(row=row,column=col,padx=3,pady=3)

    def submitbutton(self):
        self.submit = tk.Button(self,bg = 'white')
        self.submit['text'] = 'Submit'
        self.submit["command"] = self.nextRound(self.submit)
        self.submit.grid(row=12, column = 5)

    def createMainRow(self):
        for row in range(4):
            self.mainColorArray[row] = self.getRandomColorNumber()
            self.pin = tk.Button(self,bg = 'white')
            self.pin["text"] = str(row)
            self.pin.grid(row=12, column=row,padx=3,pady=3)
            self.mainButtons.append(self.pin)
            print(self.mainColorArray[row])
root = tk.Tk()
game = Game(master=root)
game.mainloop()