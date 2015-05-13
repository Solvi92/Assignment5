import tkinter as tk
import random

class Game(tk.Frame):
    buttonArray = [[[-1,0] for x in range(4)]  for x in range(12)]
    mainArray = [-1,-1,-1,-1]
    currentRow = 0
    colorArray = ['yellow','red','green','blue','purple']
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createRows()
        self.submitbutton()
        self.createtMainRow()
        self.master.title('Mastermind 3000')

    def getRandomColorNumber(self):
        color = random.randint(0,len(self.colorArray)-1)
        return color

    def changeColor(self,button,row,col):
        def colorCallback():
            colorNumber = self.buttonArray[row][col][0]
            colorNumber = (colorNumber + 1) % 5
            self.buttonArray[row][col][0] = colorNumber
            color = self.colorArray[colorNumber]
            button.configure(bg = color )
        return colorCallback
    def gameOver(self):
        print('bla')


    def nextRound(self,button):
        def nextRoundCallback():
            canContinue = True
            for x in range(4):
                if self.buttonArray[self.currentRow][x][0] < 0:
                    canContinue = False
            if canContinue:
                self.currentRow += 1
                for x in range(4):
                    if self.buttonArray[self.currentRow][x][0] == self.mainArray[x]:
                        pass
                        #colorNumber = self.mainArray[x]
                        #color = self.colorArray[colorNumber]
                        #paint the button

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

    def createtMainRow(self):
        for row in range(4):
            self.mainArray[row] = self.getRandomColorNumber()
            self.pin = tk.Button(self,bg = 'white')
            self.pin["text"] = str(row)
            self.pin.grid(row=12, column=row,padx=3,pady=3)

root = tk.Tk()
game = Game(master=root)
game.mainloop()