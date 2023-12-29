from random_word import RandomWords
from art import stages, logo
import random

print(logo)
end_the_program = False

while not end_the_program:
	game=True
	word=RandomWords()
	chosen_word=word.get_random_word()
	lives=6
	already_guessed_letter=[]
	displayed_word=[]
	for i in range(len(chosen_word)):
	    displayed_word.append("_")

	print(f"The word has {len(chosen_word)} letters.")

	while game:
		guess = input("Guess a letter: ").lower()
		while not guess.isalpha():
			guess = input("Invalid guess. Please guess again:")
		if guess in already_guessed_letter:
			print("You already guessed this letter.")
		elif guess not in chosen_word:
			print(f"{guess} is not in the word.")
			lives-=1 
			already_guessed_letter.append(guess)
		else:
		    for position in range(len(chosen_word)):
		        letter = chosen_word[position]
		        if letter == guess:
		            displayed_word[position] = letter
		    already_guessed_letter.append(guess)

		print(f"{' '.join(displayed_word)}")

		if "_" not in displayed_word:
			game = False
			print(f"The word is {chosen_word}")
			print("You won!")
		elif lives == 0:
			print(stages[lives])
			game = False
			print(f"You lost! The word is {chosen_word.upper()}")	
		else:
			print(stages[lives])
	if input("Do you want to play again? (Y/N)").upper() != "Y":
		end_the_program = True
		print("Bye")