# Jennifer Fisher
# April 17, 2026 sorry I'm late!
# P2LAB1
# Project to calculate the diameter, circumference and area of a circle determined by radius provided by user.

import math
radius = float(input("Enter your desired radius: "))
diameter = radius * 2
circumference = 2 * math.pi * radius
area = math.pi * (radius ** 2)
print ("What is the radius of the circle? " + str(radius))
print ("The diameter or the circle is: " + str(diameter))
print ("The circumference of the circle is: " + str(circumference))
print ("The area of the circle is: " + str(area))