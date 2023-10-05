import turtle
import numpy as np
from tqdm import tqdm


def startDrawing():
    myTurtle = turtle.Turtle()
    screen = turtle.Screen()
    screen.colormode(255)
    # myTurtle.ht()
    screen_size = (2000, 2000)
    screen.screensize(screen_size[0], screen_size[1])
    screen.bgcolor("black")
    myTurtle.width(2)
    printInstructions = loadData()
    screen.tracer(len(printInstructions)/100, 0)
    oldx = 0
    oldy = 0
    old_color = (0, 0, 0)
    myTurtle.up()
    scaleFactor = 0.5
    x_offset = -500
    y_offset = 200
    for (x1, y1), (x2, y2), color in tqdm(printInstructions):
        y1 = -y1 * scaleFactor + y_offset
        x1 = x1 * scaleFactor + x_offset
        y2 = -y2 * scaleFactor + y_offset
        x2 = x2 * scaleFactor + x_offset
        if color != old_color:
            myTurtle.pencolor(color)
        # If the distance between the last point and the current point is greater 5, then pick up the pen and move to the new point
        distance_from_last_coord = np.sqrt((x1 - oldx)**2 + (y1 - oldy)**2)
        if distance_from_last_coord > 5:
            myTurtle.width(2)
            myTurtle.up()
            myTurtle.setpos(x1, y1)
            myTurtle.down()
            myTurtle.setpos(x2, y2)
            oldx = x2
            oldy = y2
            old_color = color
            continue
        myTurtle.width(3)
        myTurtle.setpos(x1, y1)
        myTurtle.setpos(x2, y2)
        oldx = x2
        oldy = y2
        old_color = color
    screen.update()
    screen.exitonclick()


def loadData():
    pathToData = 'polygonStorage/polygonalPoints.npy'
    a = np.load(pathToData, allow_pickle=True)
    return a


if __name__ == "__main__":
    startDrawing()
