# Jennifer Fisher
# April 19, 2026 sorry I'm late!
# P2HW1
# Project to calculate and display travel expenses formatted with space alignments using f strings.

print ("This program calculates and displays travel expenses")
budget = float(input ("Enter Budget: "))
destination = (input ("Enter your travel destination: "))
gas_exp = float(input ("Expected gas/fuel costs: "))
hotel_exp = float(input ("Expected costs for lodging/accomodations: "))
food_exp = float(input("Expected costs for meals and snacks: "))
balance = budget - (gas_exp + hotel_exp + food_exp)
print ("-------Travel Expenses-------")
print (f"{'Location:':<19} {destination}")
print (f"{'Initial Budget:':<19} ${budget:.2f}")
print (f"{'Fuel: ':<19} ${gas_exp:.2f}")
print (f"{'Accomodation: ':<19} ${hotel_exp:.2f}")
print (f"{'Food:':<19} ${food_exp:.2f}")
print ("-----------------------------")
print (f"{'Remaining Balance: ':<19} ${balance:.2f}")