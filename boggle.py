"""
Final Project
CIS4930
Summer 17
Ryan Winter
rw15e
"""
from Tkinter import *

import threading
import enchant
import math
import random
import time
import pickle 
import os 

diceLayout = [
	['A', 'E', 'A', 'N', 'E', 'G'],   
	['A', 'H', 'S', 'P', 'C', 'O'],
	['A', 'S', 'P', 'F', 'F', 'K'], 
	['O', 'B', 'J', 'O', 'A', 'B'], 
	['I', 'O', 'T', 'M', 'U', 'C'], 
	['R', 'Y', 'V', 'D', 'E', 'L'],  
	['L', 'R', 'E', 'I', 'X', 'D'],  
	['E', 'I', 'U', 'N', 'E', 'S'],  
	['W', 'N', 'G', 'E', 'E', 'H'],
	['L', 'N', 'H', 'N', 'R', 'Z'],    
	['T', 'S', 'T', 'I', 'Y', 'D'],   
	['O', 'W', 'T', 'O', 'A', 'T'],   
	['E', 'R', 'T', 'T', 'Y', 'L'],
	['T', 'O', 'E', 'S', 'S', 'I'],   
	['T', 'E', 'R', 'W', 'H', 'V'],
	['N', 'U', 'I', 'H', 'M', 'Qu']
]

validWords = enchant.Dict("en_US")

class mainGame:
    points = 0

    def __init__(self, master):
        self.master = master
        self.saveGame = {} # holds information needed to save/load game
        self.menuBar() # creates the menu bar and buttons under it 
        self.textBox() # creates box to enter words

        self.gameBoard = Board(self.master) # set up gameboard
        self.Timer()
        self.popup() # ask player if they want to start new game or load game

    def menuBar(self):
        self.menuBar = Menu(self.master)
        self.subMenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label = "Game", menu = self.subMenu)
        self.subMenu.add_command(label = "New", command = self.newGame)
        self.subMenu.add_command(label = "Save", command = self.sGame)
        self.subMenu.add_command(label = "Load", command = self.lGame)
        self.master.config(menu = self.menuBar)

    def textBox(self): 
        self.userWord = StringVar() # constructs string variable
        self.textBox = Entry(self.master, textvariable = self.userWord, width = 25, font = ("TkDefaultFont", 12))
        self.textBox.grid(row = 7, column = 2, columnspan = 8)
        self.textBox.bind("<Return>", self.userInput)

    def popup(self):
        self.playerChoiceScreen = Toplevel()
        self.playerChoiceScreen.focus()
        self.playerChoiceScreen.attributes("-topmost", 1) # moves focus to new popup window
        #self.playerChoiceScreen.attributes("-topmost", 0)
        message = Label(self.playerChoiceScreen, text = "Would you like to start a new game\n or load a saved game?")
        message.grid(row = 0, column = 0, columnspan = 2)
        newGame = Button(self.playerChoiceScreen, text = "Start New Game", command = self.newGame)
        loadGame = Button(self.playerChoiceScreen, text = "Load Game", command = self.lGame)
        newGame.grid(row = 1, column = 0)
        loadGame.grid(row = 1, column = 1)
        self.timer.cancel()
        
    def quit(self):
        self.master.quit()

    def Timer(self):
        self.gameTime = 180 # game timer (3 min)
        self.tStr = StringVar()
        self.tStr.set(self.gameTime)
        self.tLabel = Label(self.master, textvariable = self.tStr, width = 10, font = ("TkDefaultFont", 12))
        self.tLabel.grid(row = 5, column = 7)
        self.restartTimer()

    def restartTimer(self):
        self.timer = threading.Timer(1.0, self.refreshTimer)
        self.timer.start()

    def refreshTimer(self):
        self.gameTime -= 1
        self.tStr.set(self.gameTime)
        if(self.gameTime == 0):
            self.outOfTime = Toplevel()
            self.outOfTime.resizable(0,0) # disallow resizing of window
            message = Label(self.outOfTime, text = "Time\'s Up!\n Score: " + str(self.points) + "\n Would you like to play again?")
            message.grid(row = 0, column = 0, columnspan = 2)
            button1 = Button(self.outOfTime, text = "Yes", command = self.newGame)
            button1.grid(row = 1, column = 0)
            button2 = Button(self.outOfTime, text = "No", command = self.quit)
            button2.grid(row = 1, column = 1)
        else:
            self.restartTimer()

    def loadFromFile(self, event):
        self.playerChoiceScreen.destroy() # close popup
        self.saveGame = pickle.load(open(self.fName.get(self.fName.curselection()[0]), "r")) # open file for reading

        self.textBox.focus_force() # move focus back to text box
        self.gameBoard.boardList = self.saveGame["board"] # board pieces
        self.gameBoard.buildBoard() # redraw board
    
        self.oldWords = usedWords(self.master)
        self.gameBoard.oldWordList = self.saveGame["words"]
        self.oldWords.loadUsedWords(self.saveGame["words"])
        self.loadGameScreen.destroy() # close popup once user selects file


    def lGame(self):
        savedGames = [] # will hold all the saved games in current directory
        self.loadGameScreen = Toplevel()
        self.loadGameScreen.resizable(0,0) # disallow resizing
        message = Label(self.loadGameScreen, text = "Select a saved game to load")
        self.fName = Listbox(self.loadGameScreen)
        self.fName.bind("<Button-1>", self.loadFromFile)
        self.fName.pack() # resize to appropriate size
        dirList = os.listdir(".") # retrieve current working directory
        for i in dirList:
            if(i.endswith(".save")):
                savedGames.append(i)
        for x in savedGames:
            self.fName.insert(0, x) # insert at front of list, already sorting them properly

        self.tStr.set(self.saveGame["seconds"])
        self.timer = threading.Timer(1.0, self.refreshTimer)
        self.timer.start()

    def newGame(self):
        self.textBox.focus_force()
        self.gameBoard.shuffle() 
        self.oldWords = usedWords(self.master)
        self.Timer()
        self.playerChoiceScreen.destroy() # close popup
        self.outOfTime.destroy() # close popup

    def userInput(self, event): # accept input
        score = self.gameBoard.testWord(self.userWord.get())
        self.scoreWords(score)
       
    def scoreWords(self, score): # handles word scoring based on length
        if(score == "s1"):
            self.oldWords.loadBox(self.userWord.get())
            self.points += 1
        elif(score == "s2"):
            self.oldWords.loadBox(self.userWord.get())
            self.points += 2
        elif(score == "s3"):
            self.oldWords.loadBox(self.userWord.get())
            self.points += 3
        elif(score == "s5"):
            self.oldWords.loadBox(self.userWord.get())
            self.points += 5
        elif(score == "s11"):
            self.oldWords.loadBox(self.userWord.get())
            self.points += 11
        self.userWord.set("")

    def sGame(self): # save game info
        self.saveGame["board"] = self.gameBoard.boardList
        self.saveGame["seconds"] = self.gameTime
        self.saveGame["words"] = self.gameBoard.oldWordList
        pickle.dump(self.saveGame, open(time.asctime(time.localtime(time.time())) + ".save", "w")) # write pickle dump to file

class usedWords:
    usedWordList = []
    def __init__(self, master):
        self.oldWords = Text(master, width = 24, height = 14, font=("TkDefaultFont", 12))
        self.oldWords.grid(row = 0, column = 4, rowspan = 5) 
 
    def loadUsedWords(self, words):
        if(len(words) >= 1):
            for word in words:
                self.loadBox(word)
       
    def loadBox(self, word):
        self.usedWordList.append(word.upper())
        self.oldWords.insert(INSERT, word)
        self.oldWords.insert(INSERT, "\n")
    
    def isValid(self, word):
        if(validWords.check(word) == True):
            return True
        else:
            return False

class Board:
    def __init__(self, master):
        self.boardMain = Frame(master).grid(row = 0, column = 0)
        self.boardList = []
        self.shuffle()

    def testWord(self, word):
        temp = 0
        temp2 = 0
        wordToFix = list(word.upper())
        if(len(wordToFix) >= 1):
            for i in wordToFix:
                if(i == 'Q'):
                    wordToFix[wordToFix.index(i)] = 'Qu'
                    wordToFix.remove('U')
        
        for x in wordToFix:
            for y in self.boardList:
                if x in y:
                   break
            else:
                temp = 1
        if not self.checkWord(wordToFix, []):  
            temp2 = 1

        if((word.upper() in self.oldWordList) or (len(word) < 3) or (validWords.check(word) == False)): # word has already been used, is too short, or not in dictionary
           return

        if((temp == 0) and (temp2 == 0)):
            self.oldWordList.append(word.upper()) # store valid word
            if len(word) < 5: # 1 pt
                return "s1"
            elif len(word) == 5: # 2 pt
                return "s2" 
            elif len(word) == 6: # 3 pt
                return "s3" 
            elif len(word) == 7: # 5 pt
                return "s5"
            elif len(word) >= 8: # 11 pt
                return "s11"

    def drawBoard(self):
        i = -1
        for j in range(0, 4):
            for k in range(0, 4):
                i += 1
                Label(self.boardMain, text = self.boardList[i], relief = RAISED, width = 2, height = 1, font = ("TkDefaultFont", 30)).grid(row = j, column = k)

    def shuffle(self):
        self.oldWordList = []
        for i in xrange(0, 16):
            self.boardList.append(random.choice(diceLayout[i]))
        random.shuffle(self.boardList)
        self.buildBoard()

    def checkWord(self, word, checked = []):
        if word == []:
            return True
        for j in range(0, 4):
            for k in range(0, 4):
                if word[0] == self.board[j][k] and not [j, k] in checked:
                    if checked == [] or self.nextTo([j, k], checked[-1]):
                         checked.append([j, k])
                    if self.checkWord(word[1:], checked):
                        return True
                    else:
                        checked.pop()
        else:
            return False

    def buildBoard(self):
        self.board = [self.boardList[0] + self.boardList[1] + self.boardList[2] + self.boardList[3], self.boardList[4] + self.boardList[5] + self.boardList[6] + self.boardList[7], self.boardList[8] + self.boardList[9] + self.boardList[10] + self.boardList[11], self.boardList[12] + self.boardList[13] + self.boardList[14] + self.boardList[15]]
        self.drawBoard()

    def nextTo(self, start, finish):
        if((start[0] - finish[0]== -1) or (start[0] - finish[0] == 0) or (start[0] - finish[0] == 1)):
            if((start[1] - finish[1] == -1) or (start[1] - finish[1] == 0) or (start[1] - finish[1] == 1)):
                return True
            else:
                return False

def main():
    root = Tk()
    root.resizable(0,0)			# disallow resizing of game screen
    root.title("Final.py")
    root.geometry("600x350") 		# game screen dimensions in pixels
    start = mainGame(root)
    root.mainloop()

if __name__ == "__main__": 
    main()
