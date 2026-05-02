# Jennifer Fisher
# May 1
# P4LAB1A
# Use turtle to draw shapes while using for loops

import turtle          
win = turtle.Screen()  
win.bgcolor("lightgray")
t = turtle.Turtle()

# add some display options
t.pensize(7)            # increase pensize (takes integer)
t.pencolor("black")     # set pencolor (takes string)
t.shape("blank")
t.color("purple")

#commands from here to the last line can be replaced
t.right(90)
t.forward(20)
t.left(90)
t.forward(20)
t.left(90)
t.forward(60)
t.penup()
t.right(90)
t.forward(10)
t.pendown()
t.right(90)
t.forward(60)
t.left(90)
t.forward(20)
t.penup()
t.forward(10)
t.pendown()
t.left(90)
t.forward(60)
t.right(90)
t.forward(20)
t.penup()
t.forward(-20)
t.right(90)
t.forward(30)
t.pendown()
t.left(90)
t.forward(10)

# end commands
win.mainloop()             # Wait for user to close window