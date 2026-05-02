# Jennifer Fisher
# May 2025
# P5LAB
# Simulates a self-checkout machine. Generates a random purchase total,
# accepts cash input from user, and disperses change by denomination.

import random

def disperse_change(change):
    """Breaks a float change amount into dollars, quarters, dimes, nickels, pennies.
    Requires: change (float)
    Returns: nothing (void)
    """
    cents = round(change * 100)      # convert to cents to avoid float precision errors

    dollars  = cents // 100
    cents    = cents % 100
    quarters = cents // 25
    cents    = cents % 25
    dimes    = cents // 10
    cents    = cents % 10
    nickels  = cents // 5
    pennies  = cents % 5

    print(f"\nYour change breakdown:")
    print(f"  Dollars:  {dollars}")
    print(f"  Quarters: {quarters}")
    print(f"  Dimes:    {dimes}")
    print(f"  Nickels:  {nickels}")
    print(f"  Pennies:  {pennies}")


def main():
    """Main logic for self-checkout simulation.
    Generates random total, collects cash from user, calculates and disperses change.
    """
    total_owed = round(random.uniform(0.01, 100.00), 2)
    print(f"Your total is: ${total_owed:.2f}")

    cash_given = float(input("Enter the amount of cash you are inserting: $"))

    while cash_given < total_owed:
        print(f"Insufficient amount. Your total is ${total_owed:.2f}.")
        cash_given = float(input("Enter the amount of cash you are inserting: $"))

    change = round(cash_given - total_owed, 2)
    print(f"Change owed: ${change:.2f}")

    disperse_change(change)


main()