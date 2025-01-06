import random
import time
from tkinter import *
import nltk
from nltk.corpus import words

nltk.download("words", quiet=True)

words_list = words.words()

chance = 10


def type_on_keyboard(event) :
	global chance
	answer = event.keysym
	indices = [index for index, char in enumerate(word) if answer == char]
	for index in indices:
		letter_guess[index] = answer
		labels_guess[index].config(text=answer)
		window.update()
	if not indices:
		chance -= 1
		if chance == 5:
			canvas.create_oval(240, 140, 320, 250, width=12)
		elif chance == 4:
			canvas.create_line(280, 250, 280, 390, width=12)
		elif chance == 3:
			canvas.create_line(280, 270, 220, 340, width=12)
		elif chance == 2:
			canvas.create_line(280, 270, 340, 340, width=12)
		elif chance == 1:
			canvas.create_line(280, 390, 220, 450, width=12)
		elif chance == 0:
			canvas.create_line(280, 390, 340, 450, width=12)

	canvas.itemconfig(label_chances, text=f"Chances : {chance}")
	if "".join(letter_guess) == word :
		canvas.create_text(250, 250, text="You won the game", fill="blue", font=("Arial", 20, "bold"))
		window.update()
		time.sleep(4)
		window.destroy()

	elif chance == 0:
		canvas.create_text(250, 250,
		                   text=f"You Loose. the word is {word}",
		                   font=("Arial", 20, "bold"),
		                   fill="white",
		                   width=450
		                   )
		window.update()
		time.sleep(4)
		window.destroy()



window = Tk()
window.title("Hangman")

canvas = Canvas(window, width=500, height=500, bg="green")
canvas.create_line(50,70, 50, 490, width=12)
canvas.create_line(44, 70, 280, 70, width=12)
canvas.create_line(280, 64, 280, 140, width=12)
label_chances = canvas.create_text(440, 20, text=f"Chances : {chance}", font=("Arial", 15), fill="#ECE852")
canvas.pack(padx=20, pady=20)

label = Label(window, text="Enter the letters :", font=("Arial", 24))
label.pack(side=LEFT)

word = random.choice(words_list)
letter_guess = ["_" for i in range(len(word))]

labels_guess = []

for letter in letter_guess :
	label_guess = Label(window, text=letter, font=("Arial", 24))
	label_guess.pack(side=LEFT)
	labels_guess.append(label_guess)


window.bind("<Key>", type_on_keyboard)
window.mainloop()
