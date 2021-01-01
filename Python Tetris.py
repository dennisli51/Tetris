#################################################
# Created by: Dennis Li (dfli@andrew.cmu.edu)
# Tetris Recreation in Python 
# Use the "a" button to rotate counterclockwise
# Use the "s" button to rotate clockwise
# Use the left and right arrow keys to shift piece
# Use down arrow to speed up piece fall
# Use space to hard drop piece
# Use "r" to restart the game
#################################################
import cs112_f20_week7_linter
import math, copy, random
from cmu_112_graphics import *

def gameDimensions(): #returns game Dimensions (can be edited)
    rows = 15; cols = 10
    cellSize = 20
    margin = 15
    return (rows, cols, cellSize, margin)

def playTetris(): #sets up window of the game based on game dimensions
    rows, cols, cellSize, margin = gameDimensions()
    height = rows * cellSize + 2 * margin
    width = cols * cellSize + 2 * margin
    runApp(width = width, height = height)

def make2dList(rows, cols): #taken from 112 Notes, creates a 2d list
    return [ ([0] * cols) for row in range(rows) ]

def getCellBounds(app, row, col):#taken and modified from 112 notes, 
    #gets the cell bounds of a specific box of a grid
    rows, cols, cellSize, margin = gameDimensions()
    height = rows * cellSize + 2 * margin
    width = cols * cellSize + 2 * margin
    gridWidth  = width - 2*margin
    gridHeight = height - 2*margin
    cellWidth = gridWidth / cols
    cellHeight = gridHeight / rows
    x0 = margin + col * cellWidth
    x1 = margin + (col+1) * cellWidth
    y0 = margin + row * cellHeight
    y1 = margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)

def appStarted(app): #model of MVC, initializes app and its variables
    app.rows, app.cols, app.cellSize, app.margin = gameDimensions()
    app.board = make2dList(app.rows, app.cols)
    app.emptyColor = "blue"
    app.height = app.rows * app.cellSize + 2 * app.margin
    app.width = app.cols * app.cellSize + 2 * app.margin
    for row in range(app.rows): #make the board a 2d list of 'blue' 
        for col in range(app.cols): 
            app.board[row][col] = app.emptyColor 
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    app.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece] 
    app.tetrisPieceColors = [ "red", "yellow", "magenta", "pink", "cyan", 
    "green", "orange" ]
    app.fallingPieceRow = 0
    app.fallingPieceCol = app.cols//2
    app.fallingPiece = 0
    app.fallingPieceColor = ''
    newFallingPiece(app)
    app.timerDelay = 200
    app.gameOver = False
    app.score = 0

def removeFullRows(app): #removes full rows and adds empty blue rows to top
    linesCleared = 0
    nullRow = []
    for i in range (app.cols):
        nullRow += [app.emptyColor]
    for row in app.board:
        currRow = True #is this specific row a full one? Assume yes
        for col in range(app.cols): 
            if row[col] == app.emptyColor: currRow = False
        if currRow: 
            linesCleared += 1
            app.board.remove(row); app.board.insert(0,nullRow) 
    app.score += linesCleared ** 2
    newFallingPiece(app)

def keyPressed(app,event): #event controller for key presses
    if not app.gameOver:
        if event.key == 'Left': moveFallingPiece(app,0,-1)
        elif event.key == 'Right': moveFallingPiece(app,0,1)
        elif event.key == 'Up': moveFallingPiece(app,-1,0)
        elif event.key == 'Down': moveFallingPiece(app,1,0)
        elif event.key == 'Space':
            moveSuccess = True
            while moveSuccess: moveSuccess = moveFallingPiece(app,1,0)
        elif event.key == 'a': #counterclockwise
            rotateFallingPiece(app)
        elif event.key == 's': #clockwise rotation
            rotateFallingPiece(app)
            rotateFallingPiece(app)
            rotateFallingPiece(app)
    elif event.key == 'r': appStarted(app)

def timerFired(app): #event controller for time intervals
    if not app.gameOver:
        moveSuccess = moveFallingPiece(app,1,0)
        if not moveSuccess: 
            placeFallingPiece(app) 
        if not fallingPiecesLegal(app): 
            app.gameOver = True

def fallingPiecesLegal(app): 
    #returns whether the current moving piece's position is legal
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col] == True:
                if (row + app.fallingPieceRow < 0 or row + 
                app.fallingPieceRow >= app.rows):
                    return False 
                elif (col + app.fallingPieceCol < 0 or 
                col + app.fallingPieceCol >= app.cols):
                    return False
                elif (app.board[row + app.fallingPieceRow]
                [col + app.fallingPieceCol] != app.emptyColor):
                    return False
    return True

def placeFallingPiece(app): #fixes the current piece as part of the board and 
    #initializes a newFallingPiece
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]:
                (app.board[app.fallingPieceRow+row][app.fallingPieceCol + col]
                ) = app.fallingPieceColor #changes the board
    newFallingPiece(app)
    removeFullRows(app)

def moveFallingPiece(app,drow,dcol): 
    #moves the falling piece's row and col by drow and dcol if it's possible
    #returns whether its legal to keep moving in direction of drow dcol 
    app.fallingPieceRow += drow
    app.fallingPieceCol += dcol
    if not fallingPiecesLegal(app):
        app.fallingPieceRow -= drow
        app.fallingPieceCol -= dcol
        return False
    else: return True

def rotateFallingPiece(app): #rotates a falling piece counterclockwise
    oldPiece = app.fallingPiece
    newRows = len(oldPiece[0])
    newCols = len(oldPiece) #flip rows and cols for the new piece
    oldRow = app.fallingPieceRow; oldCol = app.fallingPieceCol
    app.fallingPieceRow = app.fallingPieceRow + newCols//2 - newRows//2
    app.fallingPieceCol = app.fallingPieceCol + newRows//2 - newCols//2   
    app.fallingPiece = make2dList(newRows,newCols)
    for row in range (newRows):
        for col in range (newCols):
            app.fallingPiece[row][col] = None   
    for row in range(newRows):
        for col in range(newCols):
            app.fallingPiece[newRows-1 - row][col] = (oldPiece[col][row])
    if not fallingPiecesLegal(app):
        app.fallingPieceRow = oldRow; app.fallingPieceCol = oldCol
        app.fallingPiece = oldPiece; return 
        #if this rotation isn't legal retract it and gtfo out of the function

def newFallingPiece(app): #resets parameters of where the current falling
    #piece is and randomizes color and piece type
    randomIndex = random.randint(0, len(app.tetrisPieces) - 1)
    app.fallingPiece = app.tetrisPieces[randomIndex]
    app.fallingPieceColor = app.tetrisPieceColors[randomIndex]
    app.fallingPieceCol = (app.cols//2 - len(app.fallingPiece[0])//2)
    app.fallingPieceRow = 0

def drawFallingPiece(app,canvas): #draws the current falling piece
    color = app.fallingPieceColor
    for row in range(len(app.fallingPiece)):
        for col in range(len(app.fallingPiece[0])):
            if app.fallingPiece[row][col]:
                drawCell(app,canvas, app.fallingPieceRow + row, 
                app.fallingPieceCol + col ,color)

def drawCell(app, canvas, row, col, color): 
    #draws a cell based on cell bounds and color
    (x0, y0, x1, y1) = getCellBounds(app, row, col)
    if app.board[row][col] == False: 
        color = "blue"
    canvas.create_rectangle(x0, y0, x1, y1, fill= color)

def drawBoard(app, canvas): #draws Board
    for row in range(app.rows): 
        for col in range(app.cols): 
            color = app.board[row][col]
            drawCell(app,canvas,row,col,color)

def redrawAll(app, canvas): #calls all drawing functions, and also
    #handles the score and gameover texts
    canvas.create_rectangle(0, 0, app.width, app.height, fill = "orange")
    drawBoard(app,canvas)
    drawFallingPiece(app,canvas)
    canvas.create_text(app.width/2, app.margin/2, text = f'Score: {app.score}')
    if app.gameOver: canvas.create_text(app.width/2, app.height/2, 
    text = 'Game Over! Press R to Restart', font = 'Arial 10 bold')

def main():
    cs112_f20_week7_linter.lint()
    playTetris()

if __name__ == '__main__':
    main()
