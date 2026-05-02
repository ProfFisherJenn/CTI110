# Jennifer Fisher
# May 1
# P4LAB2
# Use turtle to draw shapes while using for loops

run_again = "yes"  # seed the while loop condition so it runs at least once

while run_again == "yes":

    multiplier = int(input("Enter an integer: "))

    if multiplier < 0:
        print("Cannot accept negative values.")

    else:
        # for loop counts 1 through 12
        for i in range(1, 13):          # range(1, 13) gives you 1, 2, 3 ... 12
            result = multiplier * i
            print(f"{multiplier} x {i} = {result}")

    run_again = input("Would you like to mulitple another number? (y/n): ")

print("Exiting Program ...")