# Jennifer Fisher
# April 24
# P3HW1
#Practice for debugging code! This should be fun!!


# This program takes a number grade , determines average and displays letter grade for average.

# Enter grades for six modules

mod_1 = float(input("Enter grade for Module 1: "))
mod_2 = float(input("Enter grade for Module 2: "))
mod_3 = float(input("Enter grade for Module 3: "))
mod_4 = float(input("Enter grade for Module 4: "))
mod_5 = float(input("Enter grade for Module 5: "))
mod_6 = float(input("Enter grade for Module 6: "))

# add grades entered to a list

grades = [mod_1, mod_2, mod_3, mod_4, mod_5]
# TO DO: determine lowest, highest , sum and average for grades

low_grade = min(grades)
high_grade = max(grades)
sum_grade = sum(grades)
avg_grade = sum_grade / 6
print ("----------Results-----------")
print (f"{'Lowest Grade':<17} {low_grade}")
print (f"{'Highest Grade':<17} {high_grade}")
print (f"{'Sum of Grade':<17} {sum_grade}")
print (f"{'Average':<17} {avg_grade:.2f}")
print ("----------------------------")
# determine letter grade for average

if avg_grade >= 90:
    print('Your grade is: A')
elif avg_grade >= 80:
    print('Your grade is: B')
elif avg_grade >= 70:
    print('Your grade is: C')
elif avg_grade >= 60:
    print('Your grade is: D')
else:
    print('Your grade is: F') # TO DO: finish this





