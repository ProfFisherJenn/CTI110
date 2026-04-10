# Jennifer Fisher
# April 10, 2026 sorry I'm late!
# P1HW2
# Project to calculate and display travel expenses
print ("This program calculates and displays travel expenses")
budget = int(input ("Enter Budget: "))
destination = (input ("Enter your travel destination: "))
days = int(input("Number of days you will be traveling: "))
gas_exp = int(input ("Expected gas/fuel costs: "))
hotel_exp = int(input ("Expected costs for lodging/accomodations: "))
food_exp = int(input("Expected costs for meals and snacks: "))
total = int(gas_exp + hotel_exp + food_exp)
day_cost = int(total / days)
balance = budget - (gas_exp + hotel_exp + food_exp)
print ("-------Travel Expenses-------")
print ("Location: " + str(destination))
print ("Initial Budget: " + str(budget))
print ("Fuel: " + str(gas_exp))
print ("Accomodation: " + str(hotel_exp))
print ("Food: " + str(food_exp))
print ("Total Cost: " + str(total))
print ("Average Cost Per Day: " + str(day_cost))
print ("Remaining Balance: " + str(balance))