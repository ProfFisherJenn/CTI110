# Jennifer Fisher
# April 17, 2026 sorry I'm late!
# P2LAB1
# Project to calculate the diameter, circumference and area of a circle determined by radius provided by user.

import math
radius = float(input("Enter your desired radius: "))
diameter = radius * 2
circumference = 2 * math.pi * radius
area = math.pi * (radius ** 2)
print (f"What is the radius of the circle? {radius}")
print (f"The diameter of the circle is: {diameter:.1f}")
print (f"The circumference of the circle is: {circumference:.2f}")
print (f"The area of the circle is: {area:.3f}")