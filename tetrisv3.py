from Tkinter import *
import random
import serial

ser = serial.Serial("COM3", 9600)
def controls():
    print "Controls: "
    print "r = restart"
    print "x = clockwise rotation"
    print "space = hard drop"
    print "use arrow keys to move piece"

def timerFired():
    if (canvas.data.delay <101):
        canvas.data.delay = 50
    else:
        canvas.data.delay = 700 - canvas.data.level*50
    if (canvas.data.isGameOver == False):
        if (moveFallingPiece(canvas,+1,0) == False):
            placeFallingPiece()        

##    horiz = ser.readline()
##    x = int(horiz)
##    if (x < 20):
##        moveFallingPiece(canvas, 0, -1)
##    if (x > 40):
##        moveFallingPiece(canvas, 0, +1)
##

    canvas.after(canvas.data.delay, timerFired) 
    redrawAll(canvas)

def movingTimer():

    horiz = ser.readline()
    x = int(horiz)
    print x
    if (x < 15):
        moveFallingPiece(canvas, 0, 1)
    if (x > 40):
        moveFallingPiece(canvas, 0, -1)

    canvas.after(100, movingTimer)     
    redrawAll(canvas)

    
def removeFullRows():
    combo = 0
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
           
    for x in xrange(rows):
        for y in xrange(cols):
            drawCell(x,y,canvas,canvas.data.board[x][y])
    canvas.data.fullRows += fullRows
    if (canvas.data.fullRows > 9):
        canvas.data.level = int(canvas.data.fullRows/10) + 1
    canvas.data.score += (fullRows **2) * 1000 * canvas.data.level 
    redrawAll(canvas)

def ghostPiece():
    canvas.data.ghostRow = canvas.data.fallingPieceRow
    canvas.data.ghostCol = canvas.data.fallingPieceCol
    canvas.data.ghost = canvas.data.fallingPiece
    while (dropGhost(canvas, 1) == True):
        dropGhost(canvas, 1)
    drawGhostPiece()
    
def dropGhost(canvas, drow):
    canvas.data.ghostRow = canvas.data.ghostRow + drow

    if (ghostLegal() == False):
        canvas.data.ghostRow = canvas.data.ghostRow - drow
        return False
    return True

def ghostLegal():
    if not((canvas.data.ghostRow >=0
            and canvas.data.ghostRow + len(canvas.data.ghost) <=canvas.data.rows)):
        return False  
    
    for x in xrange(len(canvas.data.ghost)):
        for y in xrange(len(canvas.data.ghost[x])):
            if (canvas.data.ghost[x][y] == True):
                if not((canvas.data.board[x+ canvas.data.ghostRow][y + canvas.data.ghostCol]) == "gray39"):
                    return False
    return True

def drawGhostPiece():
    for x in xrange(len(canvas.data.ghost)):
        for y in xrange(len(canvas.data.ghost[x])):
            if (canvas.data.ghost[x][y] == True):
                drawCell(x+canvas.data.ghostRow,y+canvas.data.ghostCol,canvas,"gray11")

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
                
def holdFallingPiece():
    if(canvas.data.placed == False):
        if (canvas.data.hold == True):
            canvas.data.holdPressed = True
            canvas.data.temp = canvas.data.fallingPiece
            canvas.data.tempColor = canvas.data.fallingPieceColor
            canvas.data.newPiece = canvas.data.holded
            canvas.data.newPieceColor = canvas.data.holdedColor
            canvas.data.holded = canvas.data.temp
            canvas.data.holdedColor = canvas.data.tempColor
            newFallingPiece(canvas)
            
        if (canvas.data.hold == False):
            canvas.data.temp = canvas.data.fallingPiece
            canvas.data.tempColor = canvas.data.fallingPieceColor
            canvas.data.holded = canvas.data.temp
            canvas.data.holdedColor = canvas.data.tempColor
            newFallingPiece1(canvas)
            canvas.data.hold = True       
    canvas.data.placed = True
    
def drawHoldPiece():

    for x in xrange(len(canvas.data.holded)):
        for y in xrange(len(canvas.data.holded[x])):
            if (canvas.data.holded[x][y] == True):
                drawHoldCell(x+5,y+5,canvas,canvas.data.holdedColor)

def drawHoldCell(row, col, canvas, color):
    canvas.create_rectangle(col*30 - 30, row*30 - 100,col*30+2,row*30+30+2- 100, fill="black") #outer   
    canvas.create_rectangle(col*30+2 - 30, row*30+2- 100,col*30,row*30+30- 100, fill=color) #inner
    
def placeFallingPiece():
    canvas.data.placed = False
    for x in xrange(len(canvas.data.fallingPiece)):
        for y in xrange(len(canvas.data.fallingPiece[x])):
            if (canvas.data.fallingPiece[x][y] == True):
                canvas.data.board[canvas.data.fallingPieceRow + x][canvas.data.fallingPieceCol +y] = canvas.data.fallingPieceColor
    rows = canvas.data.rows
    cols = canvas.data.cols
    for x in xrange(rows):
        for y in xrange(cols):
            drawCell(x,y,canvas,canvas.data.board[x][y])
    newFallingPiece(canvas)
    removeFullRows()
    
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
    if (canvas.data.holdPressed == False ):
        piece = random.randint(0,6)
        canvas.data.queue.append(canvas.data.tetrisPieces[piece])
        canvas.data.queueColor.append(canvas.data.tetrisPieceColors[piece])
        canvas.data.fallingPiece = canvas.data.queue.pop(0)
        canvas.data.fallingPieceColor = canvas.data.queueColor.pop(0)
        canvas.data.fallingPieceRow = 0
        canvas.data.fallingPieceCol = canvas.data.cols/2 -2
        drawFallingPiece()
    
    if (canvas.data.holdPressed == True):
        canvas.data.fallingPiece = canvas.data.newPiece
        canvas.data.fallingPieceColor = canvas.data.newPieceColor
        canvas.data.fallingPieceRow = 0
        canvas.data.fallingPieceCol = canvas.data.cols/2 -2
        canvas.data.holdPressed = False
        drawFallingPiece()

def newFallingPiece1(canvas):
    piece = random.randint(0,6)
    canvas.data.queue.append(canvas.data.tetrisPieces[piece])
    canvas.data.queueColor.append(canvas.data.tetrisPieceColors[piece])
    canvas.data.fallingPiece = canvas.data.queue.pop(0)
    canvas.data.fallingPieceColor = canvas.data.queueColor.pop(0)
    canvas.data.fallingPieceRow = 0
    canvas.data.fallingPieceCol = canvas.data.cols/2 -2
    drawFallingPiece()
        
def drawQueue():
    for z in xrange(len(canvas.data.queue)):
        temp = canvas.data.queue[z]
        for x in xrange(len(temp)):
            for y in xrange(len(temp[x])):
                if (temp[x][y] == True):
                    drawQueueCell(z,x+5,y+5,canvas,canvas.data.queueColor[z])

def drawQueueCell(number, row, col, canvas, color):
    canvas.create_rectangle(col*30 - 30 + 500, row*30 - 100 + number*100,col*30+2 + 500,row*30+30+2- 100 + number*100, fill="black") #outer   
    canvas.create_rectangle(col*30+2 - 30 + 500, row*30+2- 100 + number*100,col*30 + 500,row*30+30- 100 + number*100, fill=color) #inner
    
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
    canvas.create_rectangle(col*30+250, row*30+50,col*30+30+250,row*30+30+50, fill="black") #outer   
    canvas.create_rectangle(col*30+252, row*30+52,col*30+30+248,row*30+30+48, fill=color) #inner


def drawGame():
    rows = canvas.data.rows
    cols = canvas.data.cols
    margin = 5
    cellSize = 30
    canvasWidth = (2*margin + cols*cellSize + 500)
    canvasHeight = (2*margin + rows*cellSize+ 90)
    
    canvas.create_rectangle(0,0,canvasWidth,canvasHeight, fill="orange")

    drawBoard()
    ghostPiece()
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
    drawHoldPiece()
    drawQueue()

    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2   
    if (canvas.data.isGameOver == True):
        canvas.create_text(cx, cy, text="Game Over!", font=("Helvetica", 32, "bold"))
    canvas.create_text(cx,30, text = "Score: "+ str(canvas.data.score), font=("Helvetica", 20, "bold"))
    canvas.create_text(cx+100,cy*2 - 30, text = "Level: "+ str(canvas.data.level), font=("Helvetica", 20, "bold"))
    canvas.create_text(cx - 250,30, text = "Hold", font=("Helvetica", 20, "bold"))
    canvas.create_text(cx + 260,30, text = "Next Piece", font=("Helvetica", 20, "bold"))
    canvas.create_text(cx-150,cy*2 - 30, text = "Lines Cleared: "+ str(canvas.data.fullRows), font=("Helvetica", 20, "bold"))
    
def keyPressed(event):

    if (event.keysym == "Down"):
        moveFallingPiece(canvas, 1, 0)
    elif (event.keysym == "Left"):
        moveFallingPiece(canvas, 0, -1)
    elif (event.keysym == "Right"):
        moveFallingPiece(canvas, 0, 1)
    elif (event.keysym == "Up"):
        rotateFallingPiece()
        rotateFallingPiece()
        rotateFallingPiece()
    elif (event.keysym == "c"):
        newFallingPiece(canvas)
    elif (event.keysym == "s"):
        holdFallingPiece()
    elif (event.keysym == "Shift_L"):
        holdFallingPiece()        
    elif (event.keysym == 'space'):
        while (moveFallingPiece(canvas,+1,0) == True):
            moveFallingPiece(canvas, 1,0)
        placeFallingPiece()
    elif (event.keysym == "x"):
        rotateFallingPiece()
        rotateFallingPiece()
        rotateFallingPiece()
    elif (event.keysym == "z"):
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
        if (canvas.data.fallingPieceRow <3):
            canvas.data.fallingPieceRow = 3
        else:
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
    canvas.data.holdPressed = False
    canvas.data.hold = False
    canvas.data.holded = [[]]
    canvas.data.temp = [[]]
    canvas.data.holdedColor = []
    canvas.data.tempColor = []
    canvas.data.newPieceColor = []
    canvas.data.newPiece = [[]]
    canvas.data.placed =  False
    canvas.data.queue = []
    canvas.data.queueColor = []
    for x in xrange (0,5,1):
        piece = random.randint(0,6)
        canvas.data.queue.append(canvas.data.tetrisPieces[piece])
        canvas.data.queueColor.append(canvas.data.tetrisPieceColors[piece])

    canvas.data.ghost = [[]]
    canvas.data.ghostRow = 0
    canvas.data.ghostCol = 0
    canvas.data.level = 1
    canvas.data.delay = 600
    newFallingPiece(canvas)
    redrawAll(canvas)

    
def run(rows, cols):
    global canvas
    root = Tk()
    margin = 5
    cellSize = 30
    canvasWidth = (2*margin + cols*cellSize + 500)
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
    movingTimer()
    controls()
    root.mainloop()
   
run(20,10)

