import tkinter as tk
import random
import csv
from PIL import Image, ImageTk

class GUIFigure:
    def __init__(self, master, csv_file):
        self.master = master
        self.master.title("Image Quiz")
        self.master.geometry("500x500")

        # Load image data from CSV file
        self.image_data = []
        with open(csv_file, "r") as f:
            reader = csv.reader(f)
            next(reader) # Skip header row
            for row in reader:
                self.image_data.append(row)

        # Create UI components
        self.question_label = tk.Label(self.master, text="Question", font=("Arial", 20))
        self.question_label.pack(pady=20)

        self.answer_frame = tk.Frame(self.master)
        self.answer_frame.pack(pady=20)

        self.answer_buttons = []
        for i in range(3):
            button = tk.Button(self.answer_frame, text="", font=("Arial", 16), command=lambda i=i: self.check_answer(i))
            button.pack(side="left", padx=10)
            self.answer_buttons.append(button)

        self.score_label = tk.Label(self.master, text="Score: 0/0", font=("Arial", 16))
        self.score_label.pack(pady=20)

        # Start quiz
        self.score = [0, 0] # [num_correct, num_total]
        self.num_questions = 0
        self.next_question()

    def next_question(self):
        # Select a random image from the CSV file
        image_path, category = random.choice(self.image_data)
        image_name = image_path.split("\\")[-1]

        # Load image and display on question label
        image = Image.open(image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.question_label.configure(image=photo)
        self.question_label.image = photo

        # Generate answer options
        correct_option = category
        category_options = list(set([row[1] for row in self.image_data if row[1] != category]))
        random.shuffle(category_options)
        incorrect_option_1 = category_options[0]
        incorrect_option_2 = random.choice([row[1] for row in self.image_data if row[1] != category and row[1] != incorrect_option_1])

        # Display answer options on buttons
        options = [correct_option, incorrect_option_1, incorrect_option_2]
        random.shuffle(options)
        for i in range(3):
            self.answer_buttons[i].configure(text=options[i])

        # Increment question count
        self.num_questions += 1

    def check_answer(self, index):
        # Update score
        if self.answer_buttons[index].cget("text") == category:
            self.score[0] += 1
        self.score[1] += 1

        # Update score label
        self.score_label.configure(text="Score: {}/{}".format(self.score[0], self.score[1]))

        # Check if quiz is over
        if self.num_questions == 10:
            for button in self.answer_buttons:
                button.configure(state="disabled")
            return

        # Move on to next question
        self.next_question()
