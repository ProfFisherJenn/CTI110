# Jennifer Fisher
# April 25, 2026
# P3HW2
# Project to calculate regular and overtime hours worked to display summary of employee, hours, pay and gross pay.
#Psuedocode:
#1 get user input for employee name, hours worked and pay rate
#2 determine if employee worked more than 40 hours
#3 if employee worked <= 40 hours, multiple hours times rate of pay
#4 else employee worked > 40 hours, subtract 40 from total hours to determine hours over 40
#5 calculate regular hours times pay rate
#6 calculate overtime hours times 1.5 times pay rate
#7 sum pay total for regular hours pay total plus overtime hours pay total to display total pay for all hours
#8 Dislay: employee name, pay rate, muber of hours worked, number of overtime hours, regular pay, overtime pay and gross pay

#Get user input for employee name, hours worked and pay rate
emp_name = input("Enter employee's first and last name: ")
hrs_wrk = float(input("Enter number of hours employee worked this week: "))
pay_rate = float(input("Enter the rate of pay for employee:"))

#Calculate pay based on regular vs overtime hours
if hrs_wrk <= 40:
    gross_pay = hrs_wrk * pay_rate
else:
    ot_hrs = hrs_wrk - 40
    ot_pay = ot_hrs * 1.5 * pay_rate
    rg_pay = 40 * pay_rate
    gross_pay = rg_pay + ot_pay

print ("--------------------------")
print (f"Employee Name: {emp_name}")

print (f"{'Hours Worked':<17} {'Pay Rate':<17} {'Overtime Hours':<17} {'Overtime Pay':<17} {'Regular Pay':<17} {'Gross Pay':<17}")
if hrs_wrk <= 40:
    print (f"{hrs_wrk:<17} {pay_rate:<17} {'0':<17} {'0':<17} ${gross_pay:<17.2f} ${gross_pay:<17.2f}")
else:
    print (f"{hrs_wrk:<17} {pay_rate:<17} {ot_hrs:<17} ${ot_pay:<17.2f} ${rg_pay:<17.2f} ${gross_pay:<17.2f}")
