# Jennifer Fisher
# April 17, 2026 sorry I'm late!
# P2LAB2
# Project to display values defined in dictionary.

car_mpg = {'Camaro':18.21,'Prius':52.36,'Model S':110,'Silverado':26}
car_mileage = car_mpg.keys()
print (car_mileage)
model = input ("Enter a vehicle name listed above to display it's fuel usage per mile: ")
print (f"The {model} gets {car_mpg[model]} mpg.")
drive_distance = float (input (f"How many miles will you drive the {model}?"))
fuel_needed = drive_distance / car_mpg[model]
print (f"{fuel_needed:.2f} gallon(s) of gas are needed to drive the {model} {drive_distance:.2f} miles.")
