# Jennifer Fisher
# April 19
# P3LAB
# Project to calculate efficient coin demoninations of change in dollar values.

#Get Value from user
change = float(input("Enter an ammount of money: $"))
print(f"Change Amount: ${change}")
#convert value to an integer
change = int(change * 100)
print(f"Change Amount: {change}")
#Determine how many whole dollars are needed
num_dollars = change // 100
change = change - (num_dollars * 100)
#Determine how many whole quarters are needed
num_quarters = change // 25
change = change - (num_quarters * 25)
#Determine how many whole dimes are needed
num_dimes = change // 10
change = change - (num_dimes * 10)
#Determine how many whole nickles are needed
num_nickles = change // 5
change = change - (num_nickles * 5)
#Determine how many whole pennies are needed
num_pennies = change // 1
change = change - (num_pennies * 1)

#If/Else statements to dertermine how values print out:
if num_dollars > 0:
    if num_dollars == 1:
        print(f"{num_dollars} dollar")
    else:
       print(f"{num_dollars} dollars")
if num_quarters > 0:
    if num_quarters == 1:
        print(f"{num_quarters} quarter")
    else:
       print(f"{num_quarters} quarters")
if num_dimes > 0:
    if num_dimes == 1:
        print(f"{num_dimes} dime")
    else:
       print(f"{num_dimes} dimes")
if num_nickles > 0:
    if num_nickles == 1:
        print(f"{num_nickles} nickle")
    else:
       print(f"{num_nickles} nickles")
if num_pennies > 0:
    if num_pennies == 1:
        print(f"{num_pennies} penny")
    else:
       print(f"{num_pennies} pennies")
