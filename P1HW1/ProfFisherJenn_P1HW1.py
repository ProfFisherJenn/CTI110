# Jennifer Fisher
# April 10, 2026 sorry I'm late!
# P1HW1
# Project to calculate numerical values from inputs

print ("---- Calculating Exponents ----")
base_value = int (input ("Enter an integer as the base value: "))
exponent = int (input ("Enter an integer as the exponent: "))
product = (base_value ** exponent)
print (str(base_value) + " raised to the power of " + str(exponent) + " is " + str(product) + "!!")
print ("----Addition and Subtraction----")
start_number = int(input ("Enter a starting interger: "))
add_number = int(input ("Enter an integer to add: "))
sub_number = int(input( "Enter an integer to subtract: "))
result = (start_number + add_number - sub_number)
print (str(start_number) + " + " + str(add_number) + " - " + str(sub_number) + " is equal to " + str(result))