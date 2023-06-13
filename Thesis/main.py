import os
import tkinter as tk
import random
import csv
from PIL import Image, ImageTk

class DifficultySelection:
    def __init__(self, master):
        self.master = master
        self.master.title("Select Difficulty")
        self.master.geometry("300x150")

        self.difficulty = tk.StringVar()
        self.difficulty.set("easy")

        easy_button = tk.Radiobutton(self.master, text="Easy", variable=self.difficulty, value="easy")
        easy_button.pack(pady=5)

        medium_button = tk.Radiobutton(self.master, text="Medium", variable=self.difficulty, value="medium")
        medium_button.pack(pady=5)

        hard_button = tk.Radiobutton(self.master, text="Hard", variable=self.difficulty, value="hard")
        hard_button.pack(pady=5)

        start_button = tk.Button(self.master, text="Start", command=self.start_quiz)
        start_button.pack(pady=10)

    def start_quiz(self):
        self.master.destroy()
        root = tk.Tk()
        app = GUIFigure(root, self.difficulty.get())
        root.mainloop()

class GUIFigure:
    def __init__(self, master, difficulty):
        self.master = master
        self.master.title("Image Quiz")
        self.master.geometry("500x500")
        self.difficulty = difficulty

        # Get the file path of the current script and the root folder path
        current_file_path = os.path.abspath(__file__)
        root_folder_path = os.path.dirname(os.path.dirname(current_file_path))

        # Get the path to the Images folder and the CSV file
        images_folder_path = os.path.join(root_folder_path, 'Thesis', 'Images')
        csv_file_path = os.path.join(images_folder_path, 'file.csv')

        # Create the CSV file if it doesn't exist and save image information to it
        if not os.path.exists(csv_file_path):
            with open(csv_file_path, 'w') as f:
                f.write('Header1,Header2,Header3\n')
        save_image_info_to_csv(csv_file_path)

        # Load image data from CSV file
        self.image_data = []
        with open(csv_file_path, "r") as f:
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
        self.image_path = ""
        self.image_name = ""
        self.num_questions = 0
        self.difficulty = difficulty
        self.next_question()

    def next_question(self):
        # Select a random image from the CSV file
        self.image_path, category = random.choice(self.image_data)
        self.image_name = os.path.basename(self.image_path)

        # Load image and display on question label
        image = Image.open(self.image_path)
        image = image.resize((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.question_label.configure(image=photo)
        self.question_label.image = photo

        # Generate answer options
        correct_option = self.image_name
        category_images = [row[0] for row in self.image_data if row[1] == category]
        image_name_options = list(set([os.path.basename(row) for row in category_images if os.path.basename(row) != self.image_name]))
        if len(image_name_options) == 0:
            image_name_options = [os.path.basename(row[0]) for row in self.image_data if row[1] != category and os.path.basename(row[0]) != self.image_name]
        random.shuffle(image_name_options)

        # difficulty Level choice implementation according to the category
        if self.difficulty == "easy":
        # easy: three options are from the different categories
            incorrect_option_1 = os.path.basename(random.choice([row[0] for row in self.image_data if row[1] != category and os.path.basename(row[0]) != self.image_name]))
            incorrect_option_2 = os.path.basename(random.choice([row[0] for row in self.image_data if row[1] != category and os.path.basename(row[0]) != self.image_name]))
        # medium: One of them is from the same category as the image, the other is from a different category
        elif self.difficulty == "medium":
            incorrect_option_1 = image_name_options[0]
            incorrect_option_2 = os.path.basename(random.choice([row[0] for row in self.image_data if row[1] != category and os.path.basename(row[0]) != self.image_name]))
        
        # hard: three options are from the same category
        elif self.difficulty == "hard":
            incorrect_option_1 = image_name_options[0]
            incorrect_option_2 = image_name_options[1]
            
        # Display answer options on buttons
        options = [correct_option, incorrect_option_1, incorrect_option_2]
        random.shuffle(options)
        for i in range(3):
            self.answer_buttons[i].configure(text=options[i])

        # Increment question count
        self.num_questions += 1

    def check_answer(self, index):
        # Update score
        if self.answer_buttons[index].cget("text") == self.image_name:
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

def save_image_info_to_csv(csv_file_path):
    # Get the path to the Images folder
    images_folder_path = os.path.dirname(csv_file_path)

    # Get a list of all image files in the Images folder
    image_files = [os.path.join(images_folder_path, f) for f in os.listdir(images_folder_path) if f.endswith('.jpg')]

    # Shuffle the image files
    random.shuffle(image_files)

    # Save image information to CSV file
    with open(csv_file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        for image_file in image_files:
            category = os.path.basename(os.path.dirname(image_file))
            writer.writerow([image_file, category])

if __name__ == '__main__':
    root = tk.Tk()
    app = DifficultySelection(root)
    root.mainloop()