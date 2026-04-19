# Jennifer Fisher
# April 19, 2026
# P2HW2
# Project to display highest, lowest, sum and average of grades entered by user.
#Psuedocode:
#1. Have user enter grades for modules 1-6
#2. Store all grades in a list called module_grades
#3. Display lowest grade using min()
#4. Display highest grade using max()
#5. Display sum of all grades using sum()
#6. Calculate and display average with two decimal places.

m1_grade = float(input("Enter the grade for Module 1: "))
m2_grade = float(input("Enter the grade for Module 2: "))
m3_grade = float(input("Enter the grade for Module 3: "))
m4_grade = float(input("Enter the grade for Module 4: "))
m5_grade = float(input("Enter the grade for Module 5: "))
m6_grade = float(input("Enter the grade for Module 6: "))
module_grades = [m1_grade, m2_grade, m3_grade, m4_grade, m5_grade, m6_grade]
low_grade = min(module_grades)
high_grade = max(module_grades)
sum_grade = sum(module_grades)
avg_grade = sum_grade / 6
print ("----------Results-----------")
print (f"{'Lowest Grade':<17} {low_grade}")
print (f"{'Highest Grade':<17} {high_grade}")
print (f"{'Sum of Grade':<17} {sum_grade}")
print (f"{'Average':<17} {avg_grade:.2f}")
print ("----------------------------")