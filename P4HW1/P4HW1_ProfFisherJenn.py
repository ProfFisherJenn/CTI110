# Jennifer Fisher
# May 2 2025
# P4HW1
# Collects a user-defined number of scores, validates each entry,
# drops the lowest score, calculates the average, and assigns a letter grade.

# --- PSEUDOCODE ---
# 1. Create empty list to hold scores
# 2. Ask user how many scores to enter
# 3. Loop that many times:
#    a. Ask for a score
#    b. Inner loop: if score is not 0-100, reject and re-ask
#    c. If valid, append to list
# 4. Find and display lowest score
# 5. Remove lowest score from list
# 6. Display modified list
# 7. Calculate average of remaining scores
# 8. Determine letter grade from average
# 9. Display average and letter grade

score_list = []  # empty list ready to collect scores

num_scores = int(input("How many scores would you like to enter? "))

for i in range(num_scores):
    score = int(input(f"Enter score {i + 1}: "))

    while score < 0 or score > 100:           # inner validation loop
        print("Invalid score. Must be between 0 and 100.")
        score = int(input(f"Enter score {i + 1}: "))

    score_list.append(score)                  # only appends after validation passes

lowest = min(score_list)
print(f"\nLowest score: {lowest}")

score_list.remove(lowest)                     # drops first occurrence of lowest value
print(f"Score list after dropping lowest: {score_list}")

average = sum(score_list) / len(score_list)
print(f"Average: {average:.2f}")

# Letter grade determination
if average >= 90:
    grade = "A"
elif average >= 80:
    grade = "B"
elif average >= 70:
    grade = "C"
elif average >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Letter grade: {grade}")