#Add header notes

import turtle          
win = turtle.Screen()  
win.bgcolor("lightpink")
t = turtle.Turtle()

# add some display options
t.pensize(7)            # increase pensize (takes integer)
t.pencolor("purple")     # set pencolor (takes string)
t.shape("blank")
t.color("hotpink")

#commands from here to the last line can be replaced
# square, sides are 360 / 4 = 90 degrees
 
t.left(180)             # this time we'll draw it in a different direction

# draw the square
for i in (1,2,3,4,):
    t.forward(100)
    t.left(90)

# draw the triangle
for i in (1,2,3,):
    t.forward(100)
    t.right(120)

turtle.exitonclick()