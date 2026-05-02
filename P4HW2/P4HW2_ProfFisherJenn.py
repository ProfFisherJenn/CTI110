# Jennifer Fisher
# May 2 2025
# P4HW2
# Calculates gross pay for multiple employees including regular and overtime pay.
# Tracks running totals for all employees until user enters "Done".

# --- PSEUDOCODE ---
# 1. Initialize running totals and employee counter to zero
# 2. Ask for first employee name
# 3. While name is not "Done":
#    a. Ask for hourly rate and hours worked
#    b. If hours > 40: overtime = (hours - 40) * rate * 1.5, regular = 40 * rate
#    c. If hours <= 40: overtime = 0, regular = hours * rate
#    d. Calculate gross pay = regular + overtime
#    e. Add to running totals, increment employee count
#    f. Ask for next employee name or "Done"
# 4. Display total regular pay, total overtime pay, total gross pay, employee count

total_regular   = 0.0
total_overtime  = 0.0
total_gross     = 0.0
employee_count  = 0

name = input("Enter employee name (or 'Done' to finish): ")

while name != "Done":

    rate  = float(input(f"Enter hourly rate for {name}: "))
    hours = float(input(f"Enter hours worked for {name}: "))

    if hours > 40:
        regular_pay  = 40 * rate
        overtime_pay = (hours - 40) * rate * 1.5
    else:
        regular_pay  = hours * rate
        overtime_pay = 0.0

    gross_pay = regular_pay + overtime_pay

    total_regular  += regular_pay
    total_overtime += overtime_pay
    total_gross    += gross_pay
    employee_count += 1

    print(f"\n--- {name} ---")
    print(f"Regular pay:  ${regular_pay:.2f}")
    print(f"Overtime pay: ${overtime_pay:.2f}")
    print(f"Gross pay:    ${gross_pay:.2f}\n")

    name = input("Enter employee name (or 'Done' to finish): ")

# After sentinel ends the loop
print("===== PAYROLL SUMMARY =====")
print(f"Number of employees:  {employee_count}")
print(f"Total regular pay:    ${total_regular:.2f}")
print(f"Total overtime pay:   ${total_overtime:.2f}")
print(f"Total gross pay:      ${total_gross:.2f}")