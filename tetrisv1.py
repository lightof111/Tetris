from Tkinter import *
import random

def controls():
    print "Controls: "
    print "r = restart"
    print "x = clockwise rotation"
    print "space = hard drop"
    print "use arrow keys to move piece"

def timerFired():
    delay = 500 
    if (canvas.data.isGameOver == False):
        if (moveFallingPiece(canvas,+1,0) == False):
            placeFallingPiece()        
            newFallingPiece(canvas)
            removeFullRows()
    
    canvas.after(delay, timerFired) 
    redrawAll(canvas)
##
##def removeFullRows():
##    rows = canvas.data.rows
##    cols = canvas.data.cols    
##    oldRows = canvas.data.rows    
##    newRow = canvas.data.rows-1
##    fullRows = 0
##    unfinished = 0
##    cols = canvas.data.cols
##    copy = canvas.data.board
##    for x in xrange(oldRows-1, -1,-1):
##        y = 0        
##        while (y < cols and newRow >=0):
##            if (canvas.data.board[x][y] == "gray39"):
##                copy[newRow] = canvas.data.board[x]
##                newRow = newRow -1
##                unfinished +=1
##                break
##            if (y == cols - 1):
##                fullRows +=1                         
##            y = y+1
##           
##    canvas.data.score += (fullRows **2) * 1000
##    canvas.data.board = copy
##    for x in xrange(rows):
##        for y in xrange(cols):
##            drawCell(x,y,canvas,canvas.data.board[x][y])
##    canvas.data.fullRows += fullRows
##    redrawAll(canvas)

def removeFullRows():
    rows = canvas.data.rows
    cols = canvas.data.cols
    rowremoved = 0
    fullRows = 0
    full = True
    copy = canvas.data.board
    x= rows - 1
    while (x >-1):
        full = True
        for y in xrange(0, cols,1):
            if (canvas.data.board[x][y] == "gray39"):
                full = False
        if(full == True):
            rowremoved = x
            for a in xrange(rows-1, -1,-1):
                for b in xrange(0,cols,1):
                    if (a < rowremoved):
                        copy[a+1][b] = canvas.data.board[a][b]
                    elif (a > rowremoved):
                        copy[a][b] = canvas.data.board[a][b]
            canvas.data.board = copy
            fullRows +=1
            x = x + 1
        x = x-1
           
    canvas.data.score += (fullRows **2) * 1000
    for x in xrange(rows):
        for y in xrange(cols):
            drawCell(x,y,canvas,canvas.data.board[x][y])
    canvas.data.fullRows += fullRows
    redrawAll(canvas)
    
def placeFallingPiece():
    for x in xrange(len(canvas.data.fallingPiece)):
        for y in xrange(len(canvas.data.fallingPiece[x])):
            if (canvas.data.fallingPiece[x][y] == True):
                canvas.data.board[canvas.data.fallingPieceRow + x][canvas.data.fallingPieceCol +y] = canvas.data.fallingPieceColor
    rows = canvas.data.rows
    cols = canvas.data.cols
    for x in xrange(rows):
        for y in xrange(cols):
            drawCell(x,y,canvas,canvas.data.board[x][y])   
    
def moveFallingPiece(canvas, drow, dcol):
    canvas.data.fallingPieceCol = canvas.data.fallingPieceCol + dcol
    canvas.data.fallingPieceRow = canvas.data.fallingPieceRow + drow

    if (fallingPieceIsLegal() == False):
        canvas.data.fallingPieceCol = canvas.data.fallingPieceCol - dcol
        canvas.data.fallingPieceRow = canvas.data.fallingPieceRow - drow
        return False
    drawFallingPiece()
    return True

def fallingPieceIsLegal():
    if not((canvas.data.fallingPieceRow >=0
            and canvas.data.fallingPieceRow + len(canvas.data.fallingPiece) <=canvas.data.rows
            and canvas.data.fallingPieceCol >=0
            and canvas.data.fallingPieceCol + len(canvas.data.fallingPiece[0]) <= canvas.data.cols)):
        return False  
       
    for x in xrange(len(canvas.data.fallingPiece)):
        for y in xrange(len(canvas.data.fallingPiece[x])):
            if (canvas.data.fallingPiece[x][y] == True):
                if not((canvas.data.board[x+ canvas.data.fallingPieceRow][y + canvas.data.fallingPieceCol]) == "gray39"):
                    return False
    return True    
def newFallingPiece(canvas):
    piece = random.randint(0,6)
    
    canvas.data.fallingPiece = canvas.data.tetrisPieces[piece]
    canvas.data.fallingPieceColor = canvas.data.tetrisPieceColors[piece]
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 -2
    drawFallingPiece()
    

def drawFallingPiece():

    for x in xrange(len(canvas.data.fallingPiece)):
        for y in xrange(len(canvas.data.fallingPiece[x])):
            if (canvas.data.fallingPiece[x][y] == True):
                drawCell(x+canvas.data.fallingPieceRow,y+canvas.data.fallingPieceCol,canvas,canvas.data.fallingPieceColor)
                
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
    
    canvas.create_rectangle(0,0,canvasWidth,canvasHeight, fill="orange")

    drawBoard()
    drawFallingPiece()

def gameOver():
    rows = canvas.data.rows
    cols = canvas.data.cols
    canvas.data.isGameOver = False
    
    for y in xrange(cols):
        if not (canvas.data.board[0][y] =="gray39"):
            canvas.data.isGameOver = True
                

def redrawAll(canvas):
    canvas.delete(ALL)  
    drawGame()
    gameOver()

    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2   
    if (canvas.data.isGameOver == True):
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
    canvas.create_text(cx,30, text = "Score: "+ str(canvas.data.score), font=("Helvetica", 20, "bold"))
    canvas.create_text(cx,cy*2 - 30, text = "Lines Cleared: "+ str(canvas.data.fullRows), font=("Helvetica", 20, "bold"))

    
def keyPressed(event):

    if (event.keysym == "Down"):
        moveFallingPiece(canvas, 1, 0)
    elif (event.keysym == "Left"):
        moveFallingPiece(canvas, 0, -1)
    elif (event.keysym == "Right"):
        moveFallingPiece(canvas, 0, 1)
    elif (event.keysym == "c"):
        newFallingPiece(canvas)
    elif (event.keysym == 'space'):
        while (moveFallingPiece(canvas,+1,0) == True):
            moveFallingPiece(canvas, 1,0)
        placeFallingPiece()
    elif (event.keysym == "x"):
        rotateFallingPiece()
        rotateFallingPiece()
        rotateFallingPiece()
    elif (event.keysym == "r"):
        init()
    redrawAll(canvas)
           
def rotateFallingPiece():
    oldRow = len(canvas.data.fallingPiece)
    oldCol = len(canvas.data.fallingPiece[0])
    newPiece = []
    oldPiece = canvas.data.fallingPiece
    oldLocation = []
    oldLocation.append(canvas.data.fallingPieceRow)
    oldLocation.append(canvas.data.fallingPieceCol)
    location = fallingPieceCenter(canvas)
    
    for x in xrange(len(canvas.data.fallingPiece[0])-1,-1,-1):
        
        row = []                
        for y in xrange(len(canvas.data.fallingPiece)):
            row.append(canvas.data.fallingPiece[y][x])
        newPiece.append(row)
        
    canvas.data.fallingPiece = newPiece
    canvas.data.fallingPieceRow = location[0] - len(canvas.data.fallingPiece)
 
    if (fallingPieceIsLegal() == False):
        canvas.data.fallingPiece = oldPiece
        canvas.data.fallingPieceRow = oldLocation[0]
    drawFallingPiece()

def fallingPieceCenter(canvas):
    location = []
    location.append(canvas.data.fallingPieceRow + len(canvas.data.fallingPiece))
    return location

def init():
    iPiece = [
    [ True,  True,  True,  True]
    ]

    jPiece = [
    [ True, False, False ],
    [ True, True,  True]
    ]

    lPiece = [
    [ False, False, True],
    [ True,  True,  True]
    ]

    oPiece = [
    [ True, True],
    [ True, True]
    ]

    sPiece = [
    [ False, True, True],
    [ True,  True, False ]
    ]

    tPiece = [
    [ False, True, False ],
    [ True,  True, True]
    ]

    zPiece = [
    [ True,  True, False ],
    [ False, True, True]
    ]

    tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]
    tetrisPieceColors = [ "cyan", "blue", "orange", "yellow", "green", "magenta", "red" ]
    canvas.data.tetrisPieces = tetrisPieces
    canvas.data.tetrisPieceColors = tetrisPieceColors
    createBoard()
    canvas.data.score = 0
    canvas.data.fullRows = 0 
    newFallingPiece(canvas)
    redrawAll(canvas)

    
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
    root.bind("<Key>", keyPressed)
    timerFired()
    controls()
    root.mainloop()
   
run(20,10)

