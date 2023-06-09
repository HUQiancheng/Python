import os
import tkinter as tk
import random
import csv
from PIL import Image, ImageTk

def main():
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

    # Create the GUI figure
    root = tk.Tk()
    app = GUIFigure(root, csv_file_path)
    root.mainloop()

def save_image_info_to_csv(csv_file_path):
    # Get the path to the Images folder
    images_folder_path = os.path.join(os.path.dirname(csv_file_path), 'Animals')

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
        self.image_path = ""
        self.image_name = ""
        self.num_questions = 0
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
        image_name_options = list(set([os.path.basename(row[0]) for row in self.image_data if os.path.basename(row[0]) != self.image_name]))
        random.shuffle(image_name_options)
        incorrect_option_1 = image_name_options[0]
        incorrect_option_2 = random.choice([os.path.basename(row[0]) for row in self.image_data if os.path.basename(row[0]) != self.image_name and os.path.basename(row[0]) != incorrect_option_1])

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
if __name__ == '__main__':
    main()