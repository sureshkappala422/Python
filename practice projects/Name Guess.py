import random
#Start the game
name = input("Enter Your name:- ")
print("Good Luck !", name)

words = ['suresh', 'kavya', 'banana', 'apple', 'grapes'
        'from', 'to', 'speaker', 'radio', 'date', 
        'cricket', 'chess', 'ball', 'bat', 'car']

#choose the choice
word = random.choice(words)
print("Guess the word!. ")

guesses = ''
turns = 15

while turns > 0:
    failed = 0 
    for char in word:
        if char in guesses:
            print(char, end =" ")

        else:
            print("-")
            failed += 1
    if failed == 0:
        print("You Win")
        print("Your word is: ", word)
        break 

    print()
    guess = input("Guess a character:")

    guesses += guess

    if guess not in word:
        turns -= 1
        print("wrong!")
        print("you Have", + turns, 'more guess ')

        if turns == 0:
            print("You Loose")

