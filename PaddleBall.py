from tkinter import *
from random import choice
from time import clock

fieldSize, goalSize, ballSize = 300, 25, 10

sx, sy, ball, block = 5, 5, None, None

roundCounter = 0

def ballPosition():
    x1, y1, x2, y2 = list(field.coords(ball))
    return [(x1+x2)/2, (y1+y2)/2]

def randomBallPosition():
    return [choice(list(range(fieldSize-ballSize)))
            for n in range(2)]

def startGame():
    global startTime, ball, block, roundCounter, totalTime
    roundCounter += 1
    if roundCounter == 1:
        totalTime = 0
    if ball:
        field.delete(ball)
    if block:
        field.delete(block)
    block = None
    upperLeftX, upperLeftY = randomBallPosition()
    while willScore(upperLeftX, upperLeftY):
        upperLeftX = choice(list(range(fieldSize-ballSize)))
        upperLeftY = choice(list(range(fieldSize-ballSize)))
    ball = field.create_oval(upperLeftX, upperLeftY,
                             upperLeftX+ballSize, upperLeftY+ballSize,
                             fill='blue')
    startTime = clock()
    animate()

def willScore(x, y):
    x += ballSize/2
    y += ballSize/2
    return abs(x-y) > fieldSize - 2*goalSize

def animate():
    global sx, sy, totalTime, roundCounter
    pattern = 'Round {0} - Elapsed time: {1:.1f} seconds - Total: {2:.1f} seconds'
    elapsed = clock()-startTime
    timeDisplay['text'] = pattern.format(roundCounter, elapsed, totalTime+elapsed)
    x, y = ballPosition()
    hitVertical = hitBlock() and blockType == 'vertical'
    if x+sx>fieldSize or x+sx<0 or hitVertical:
        sx *= -1
    hitHorizontal = hitBlock() and blockType == 'horizontal'
    if y+sy>fieldSize or y+sy<0 or hitHorizontal:
        sy*= -1
    field.move(ball, sx, sy)
    if inGoal():
        totalTime += elapsed
        if roundCounter == 5:
            pattern = 'Game Over: Total time {0:.1f} seconds'
            timeDisplay['text'] = pattern.format(totalTime)
            roundCounter = 0
    else:
        root.after(20, animate)

def leftClick(event):
    global block, blockType
    if block:
        field.delete(block)
    block = field.create_rectangle(event.x-20, event.y,
                                   event.x+20, event.y+6,
                                   fill='light green')
    blockType = 'horizontal'

def rightClick(event):
    global block, blockType
    if block:
        field.delete(block)
    block = field.create_rectangle(event.x, event.y-20,
                                   event.x+6, event.y+20,
                                   fill = 'light green')
    blockType = 'vertical'

def hitBlock():
    if not block:
        return False
    ballX, ballY = ballPosition()
    blockX1, blockY1, blockX2, blockY2 = field.coords(block)
    return (blockX1 <= ballX <= blockX2 and blockY1 <= ballY <= blockY2)

def inGoal():
    ballX, ballY = ballPosition()
    return 0 <= ballX <= goalSize and fieldSize-goalSize <= ballY <= fieldSize

root = Tk()

instructions = Label(root, width=fieldSize, wraplength=fieldSize)
instructions.pack()

instructions['text'] = 'Welcome to Paddle Ball! Use your mouse to move the paddle by clicking where you would like it to go. The goal is to get the ball into the red square. Good luck!'

start = Button(root, command=startGame, text='Go')
start.pack()

timeDisplay = Label(root)
timeDisplay.pack()

field = Canvas(root, width=fieldSize, height=fieldSize, bg='light blue')
field.pack()

field.create_rectangle(0, fieldSize-goalSize, goalSize, fieldSize, fill='red')

field.bind('<ButtonPress-1>', leftClick)
field.bind('<ButtonPress-3>', rightClick)

mainloop()

