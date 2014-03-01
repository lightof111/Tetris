from Tkinter import *


def createBoard(): 
    rows = canvas.data.rows
    cols = canvas.data.cols
    
    board = []
    for x in xrange(rows):
        row = []
        for y in xrange(cols):
            row.append("gray39")
        board.append(row)
    canvas.data.board = board

def drawBoard():
    rows = canvas.data.rows
    cols = canvas.data.cols
    for x in xrange(rows):
        for y in xrange(cols):
            drawCell(x,y,canvas,canvas.data.board[x][y])

def drawCell(row, col, canvas, color):
    canvas.create_rectangle(col*30+50, row*30+50,col*30+30+50,row*30+30+50, fill="black") #outer   
    canvas.create_rectangle(col*30+52, row*30+52,col*30+30+48,row*30+30+48, fill=color) #inner

def drawGame():
    rows = canvas.data.rows
    cols = canvas.data.cols
    margin = 5
    cellSize = 30
    canvasWidth = (2*margin + cols*cellSize + 90)
    canvasHeight = (2*margin + rows*cellSize+ 90)  
    canvas.create_rectangle(0,0,canvasWidth,canvasHeight, fill="gray")
    drawBoard()

def init():

    createBoard()
    drawGame()
    I = [True, True, True, True]
    J = [[True, True, True] ,[False, False, True]]
    L = [[False, False, True],[True, True, True]]
    O = [[True, True],[True, True]]
    T = [[False, True, False],[True, True, True]]
    Z = [[True, True, False],[False, True, True]]
    S = [[False, True, True], [True, True, False]]

    TetrisPieces = [I, J, L, O, T, Z, S]

    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2

def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = (2*margin + cols*cellSize + 90)
    canvasHeight = (2*margin + rows*cellSize+ 90)

    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    root.resizable(width=0, height=0)
    
    class Struct: pass
    canvas.data = Struct()
    canvas.data.margin = margin
    canvas.data.cellSize = cellSize
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    canvas.data.rows = rows
    canvas.data.cols = cols

    init()
    root.mainloop()

run(20,10)
