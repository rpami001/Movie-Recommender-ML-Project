import tkinter as tk
from tkinter import *
from Temperamenttest import recommend_movie, register_user, colour_test
from Movie_recommender import recommend_movies_based_on_user_mood
import Movie_recommender

class MovieRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommender")
        self.root.geometry('900x950')
        recommendation_text = 'None'
        self.answers = {}
        self.user_info = {}  # To store user details
        self.temperament = None  # To store calculated temperament
        self.setup_ui()

        self.result_label = Label(self.root, text=f"Your temperament is: {self.temperament}", font=("Helvetica", 14))
        self.recommendation_label = Label(self.root, text=f"Movie Recommendations: \n {recommendation_text}", font=("Helvetica", 14))
        

    def setup_ui(self):
        self.create_title()
        self.create_color_test()  # Add the color test to the UI
        #self.create_temp_test_button()
        #self.create_registration_form()

    def create_registration_form(self):
        # Name Entry
        name_label = Label(self.root, text="Enter your Name:")
        name_label.grid(column=0, row=0, pady=5, sticky='w')
        self.user_info['name'] = StringVar()
        name_entry = Entry(self.root, textvariable=self.user_info['name'])
        name_entry.grid(column=1, row=0, pady=5, padx=5)

        # Password Entry
        password_label = Label(self.root, text="Enter your Password:")
        password_label.grid(column=0, row=1, pady=5, sticky='w')
        self.user_info['password'] = StringVar()
        password_entry = Entry(self.root, textvariable=self.user_info['password'], show="*")
        password_entry.grid(column=1, row=1, pady=5, padx=5)

        # Register Button (Initially Disabled)
        self.register_btn = Button(self.root, text="Register", command=self.register_user, state=DISABLED)
        self.register_btn.grid(column=1, row=2, pady=10)

    def register_user(self):
        name = self.user_info['name'].get()
        password = self.user_info['password'].get()

        if name and password and self.temperament:
            try:
                # Register user in the database
                register_user(name, password, self.temperament)

                # Success message
                success_label = Label(self.root, text=f"User {name} registered successfully!", font=("Helvetica", 12), fg="green")
                success_label.grid(column=0, row=3, columnspan=4, pady=10)
            except Exception as e:
                error_label = Label(self.root, text=f"Error: {e}", font=("Helvetica", 12), fg="red")
                error_label.grid(column=0, row=3, columnspan=4, pady=10)
        else:
            error_label = Label(self.root, text="Complete all fields and finish the temperament test first.", font=("Helvetica", 12), fg="red")
            error_label.grid(column=0, row=3, columnspan=4, pady=10)

    def create_title(self):
        title_label = Label(
            self.root,
            text="Welcome to the Movie Recommender! Take the temperament test to begin!",
            wraplength=600,
            justify="center"
        )
        title_label.grid(column=0, row=4, columnspan=4, pady=20)

    def create_temp_test_button(self):
        temp_btn = Button(self.root, text="Temperament Test", command=self.show_temperament_test)
        temp_btn.grid(column=1, row=5, columnspan=2, pady=10)

    def create_color_test(self):
        # Label for instructions
        self.color_instruction_label = Label(
            self.root, text="Select a color to determine your mood:", font=("Helvetica", 14)
        )
        self.color_instruction_label.grid(column=0, row=6, columnspan=4, pady=10)

        # Colors and their associated moods
        self.colours = {
            "Yellow": "Happy",
            "Red": "Passionate",
            "Black": "Sad",
            "Pink": "Feminine",
            "White": "Pure",
            "Orange": "Excitement",
            "Neutral": "Neutral"
        }

        # Mood display label
        self.mood_label = Label(self.root, text="Mood: None", font=("Helvetica", 14))
        self.mood_label.grid(column=0, row=7, columnspan=4, pady=10)

        # Create a button for each color
        row_num = 8
        for color, mood in self.colours.items():
            Button(
                self.root,
                text=color,
                #bg=color.lower(),
                command=lambda c=color: self.set_mood(c)
            ).grid(column=0, row=row_num, columnspan=4, pady=5, padx=10, sticky='ew')
            row_num += 1

        # Temperament Test Button (Initially Disabled)
        self.calculate_btn = Button(
            self.root, text="Proceed to Temperament Test", command=self.show_temperament_test, state=DISABLED
        )
        self.calculate_btn.grid(column=0, row=row_num+1, columnspan=4, pady=10)

        self.calculate = Button(
            self.root, text="Submit", command=self.calculate_temperament, state=DISABLED
        )
        self.calculate.grid(column=0, row=row_num, columnspan=4, pady=10)

    def set_mood(self, color):
        # Update the mood based on the selected color
        self.mood = self.colours[color]
        self.mood_label.config(text=f"Mood: {self.mood.capitalize()}")

        # If the mood is neutral, enable the temperament test button
        if self.mood == "Neutral":
            self.calculate_btn.config(state=NORMAL)
        else:
            self.calculate_btn.config(state=DISABLED)
            self.calculate.config(state=NORMAL)

    def show_temperament_test(self):
        questions = [
            "Do you enjoy being in social settings? (Yes/No)",
            "Do you often plan and stick to routines? (Yes/No)",
            "Do you easily get stressed under pressure? (Yes/No)",
            "I feel energized when I'm around a lot of people. (Yes/No)",
            "I tend to take charge in group situations. (Yes/No)",
            "I often reflect on my feelings and thoughts. (Yes/No)",
            "I prefer a calm and predictable environment. (Yes/No)",
            "I enjoy trying new things and meeting new people. (Yes/No)",
            "I get frustrated when things don’t go my way. (Yes/No)",
            "I feel deeply affected by the problems of others. (Yes/No)"
        ]

        for idx, question in enumerate(questions):
            self.temp_quest(question, f'q{idx+1}', 6 + idx)

        # Add Submit Button
        submit_btn = Button(self.root, text="Submit Temperament Test", command=self.calculate_temperament)
        submit_btn.grid(column=0, row=18, columnspan=2, pady=10)


    def temp_quest(self, text, question_id, row):
        label = Label(self.root, text=text)
        label.grid(column=5, row=row, pady=5, sticky='w')

        self.answers[question_id] = StringVar()
        radio_btn1 = Radiobutton(self.root, text="Yes", value="Yes", variable=self.answers[question_id])
        radio_btn2 = Radiobutton(self.root, text="No", value="No", variable=self.answers[question_id])
        radio_btn1.grid(column=6, row=row, pady=5)
        radio_btn2.grid(column=7, row=row, pady=5)

    def calculate_temperament(self):
        temperament_scores = {
            'Sanguine': 0,
            'Choleric': 0,
            'Melancholic': 0,
            'Phlegmatic': 0
        }

        for question_id, answer in self.answers.items():
            response = answer.get()
            if response == "Yes":
                if question_id in ['q1', 'q4', 'q8']:
                    temperament_scores['Sanguine'] += 1
                elif question_id in ['q1','q2', 'q5', 'q9']:
                    temperament_scores['Choleric'] += 1
                elif question_id in ['q3', 'q7']:
                    temperament_scores['Melancholic'] += 1
                elif question_id in ['q6', 'q10']:
                    temperament_scores['Phlegmatic'] += 1

        # Determine highest-scoring temperament
        highest_temperament = max(temperament_scores, key=temperament_scores.get)
        if self.mood == 'Neutral':
            self.temperament = highest_temperament

        else:
            self.temperament = self.mood

        print(self.mood)
        print(self.temperament)

        # Enable Registration Button
        self.register_btn.config(state=NORMAL)

        # Display temperament and fetch movie recommendations
        self.result_label.config(text=f"Your temperament is: {self.temperament}")
        self.result_label.grid(column=0, row=19, columnspan=4, pady=10)

        recommendations = recommend_movies_based_on_user_mood(self.temperament, Movie_recommender.df)
        print(recommendations)

        recommendation_text = "\n".join([f"• {movie}" for movie in recommendations])


        self.recommendation_label.config(text=f"Movie Recommendations: \n {recommendation_text}")
        self.recommendation_label.grid(column=0, row=20, columnspan=4, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderApp(root)
    root.mainloop()
