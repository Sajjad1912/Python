import random

# Function to get the c
def get_computer_choice():
    choices = ["Snake", "Water", "Gun"]
    return random.choice(choices)

# Function to get the user's choice
def get_user_choice():
    choice = input("Enter your choice (Snake, Water, Gun): ").capitalize()
    while choice not in ["Snake", "Water", "Gun"]:
        print("Invalid choice! Please choose Snake, Water, or Gun.")
        choice = input("Enter your choice (Snake, Water, Gun): ").capitalize()
    return choice

# Mapping of choices
youDict = {"Snake": 1, "Water": -1, "Gun": 0}
reversDist = {1: "Snake", -1: "Water", 0: "Gun"}

computer_choice = get_computer_choice()
you_string = get_user_choice()

# Map user and computer choices to numeric values
you = youDict[you_string]
computer = youDict[computer_choice]

print(f"You chose {you_string} \nComputer chose {reversDist[computer]}")

# Determine the result
if computer == you:
    print("It's a draw.")
else:
    if computer == -1 and you == 1:
        print("You win and computer lose.")
    elif computer == -1 and you == 0:
        print("Computer wins and you lose.")
    elif computer == 1 and you == -1:
        print("Computer wins and you lose.")
    elif computer == 1 and you == 0:
        print("You win and computer lose.")
    elif computer == 0 and you == -1:
        print("You win and computer lose.")
    elif computer == 0 and you == 1:
        print("Computer wins and you lose.")
    else:
        print("It's a tie.")
