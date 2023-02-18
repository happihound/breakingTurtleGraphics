import turtle
import numpy as np
from tqdm import tqdm

def startDrawing():
    myTurtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.tracer(100000, 0)
    screen.colormode(255)
    myTurtle.ht()
    screen.screensize(2000, 2000)
    screen.bgcolor("black")
    myTurtle.width(2)
    printInstructions = loadData()
    oldx = 0
    oldy = 0
    scaleFactor = 0.5
    for y1, x1, y2, x2, color in tqdm(printInstructions):
        y1 = y1 * scaleFactor
        x1 = x1 * scaleFactor
        y2 = y2 * scaleFactor
        x2 = x2 * scaleFactor

        myTurtle.pencolor(color)
        if (abs(oldx-x1)+abs(oldy-y1)) > 5:
            myTurtle.up()
            myTurtle.setpos(x1, y1)
            myTurtle.down()
            myTurtle.setpos(x2, y2)
            oldx = x2
            oldy = y2
            continue
        myTurtle.setpos(x1, y1)
        myTurtle.setpos(x2, y2)
        oldx = x2
        oldy = y2
    screen.update()
    screen.exitonclick()


def loadData():
    pathToData = 'polygonStorage/polygonalPoints.npy'
    a = np.load(pathToData, allow_pickle=True)
    return a

