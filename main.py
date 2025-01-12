import random
import time
from tkinter import *
import speech_recognition as sr
from tkinter import messagebox
import nltk
from nltk.corpus import words

nltk.download("words", quiet=True)

words_list = words.words()


text = ""


def remainning_chances() :
	global chance
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

	# Update chances label
	canvas.itemconfig(label_chances, text=f"Chances : {chance}")

	win_or_loss()


def win_or_loss():
	global text

	if not window :
		return
	# Check if guessed word matches the target word
	if "".join(letter_guess) == word or text.lower() == word:
		for index, alpha in enumerate(text) :
			letter_guess[index] = alpha
			labels_guess[index].config(text=alpha)
			window.update()


		canvas.create_text(
			250, 250, text="You won the game!", fill="blue", font=("Arial", 20, "bold")
		)
		window.update()
		time.sleep(4)
		window.destroy()

	# Check if the player has no remaining chances
	elif chance == 0:
		canvas.create_text(
			250,
			250,
			text=f"You Lost! The word was '{word}'",
			font=("Arial", 20, "bold"),
			fill="white",
			width=450,
		)
		window.update()
		time.sleep(4)
		window.destroy()


def mic_fun():
	global text
	mic_sr.config(text="Listening...")
	window.update_idletasks()
	r = sr.Recognizer()

	try:
		with sr.Microphone() as source:
			r.adjust_for_ambient_noise(source, duration=2)
			audio_text = r.listen(source, timeout=10, phrase_time_limit=5)
			text = r.recognize_google(audio_text).lower()
	except sr.WaitTimeoutError:
		messagebox.showerror("Timeout", "No speech detected.")
		text = ""  # Reset text
	except sr.UnknownValueError:
		messagebox.showerror("Error", "Sorry, I couldn't understand that.")
		text = ""  # Reset text
	except Exception as e:
		messagebox.showerror("Error", f"An error occurred: {e}")
		text = ""  # Reset text

	mic_sr.config(text="mic")

	if text:
		if text == word:
			win_or_loss()
		else:
			remainning_chances()



chance = 10


def type_on_keyboard(event):
	global chance
	answer = event.keysym.lower()  # Normalize input to lowercase
	indices = [index for index, char in enumerate(word) if answer == char]
	for index in indices:
		letter_guess[index] = answer
		labels_guess[index].config(text=answer)
		window.update()

	# Handle wrong guesses
	if not indices:
		remainning_chances()
	win_or_loss()


# Initialize the game
window = Tk()
window.title("Hangman")

canvas = Canvas(window, width=500, height=500, bg="green")
canvas.create_line(50, 70, 50, 490, width=12)
canvas.create_line(44, 70, 280, 70, width=12)
canvas.create_line(280, 64, 280, 140, width=12)
label_chances = canvas.create_text(
	440, 20, text=f"Chances : {chance}", font=("Arial", 15), fill="#ECE852"
)
canvas.pack(padx=20, pady=20)

label = Label(window, text="Enter the letters :", font=("Arial", 24))
label.pack(side=LEFT)

# Select a random word and initialize guesses
word = random.choice(words_list)
letter_guess = ["_" for _ in range(len(word))]

labels_guess = []

for letter in letter_guess:
	label_guess = Label(window, text=letter, font=("Arial", 24))
	label_guess.pack(side=LEFT)
	labels_guess.append(label_guess)

mic_sr = Button(
		window,
		text="mic",
		command=mic_fun,
		bg="#16C47F",
		font=("Arial", 20),
		width=15,
		activebackground="#16C47F"
	)
mic_sr.pack(padx=10, pady=5)

window.bind("<Key>", type_on_keyboard)
window.mainloop()
