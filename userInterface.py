import tkinter as tk
from tkinter import *

class MovieRecommenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Recommender")
        self.root.geometry('600x800')

        self.answers = {}
        self.setup_ui()

    def setup_ui(self):
        self.create_title()
        self.create_temp_test_button()

    def create_title(self):
        temp_test_label = Label(self.root, text='Welcome to the Movie Recommender! Select the button below and answer the questions to begin!', wraplength=600, justify="center")
        temp_test_label.grid(column=0, row=0, columnspan=4, pady=20)

    def create_temp_test_button(self):
        temp_btn = Button(self.root, text='Temperament Test', command=self.clicked)
        temp_btn.grid(column=1, row=4, columnspan=2, pady=10)

    def temp_quest(self, text, question_id, row):
        label = Label(self.root, text=text)
        label.grid(column=0, row=row, pady=5, sticky='w')
        self.answers[question_id] = StringVar()
        radio_btn1 = Radiobutton(self.root, text='Yes', value='Yes', variable=self.answers[question_id])
        radio_btn2 = Radiobutton(self.root, text='No', value='No', variable=self.answers[question_id])
        radio_btn1.grid(column=1, row=row, pady=5)
        radio_btn2.grid(column=2, row=row, pady=5)

    def clicked(self):
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
            self.temp_quest(question, f'q{idx+1}', 5 + idx)
        
        submit_btn = Button(self.root, text='Submit', command=self.process_answers)
        submit_btn.grid(column=1, row=16, columnspan=2, pady=10)

    def process_answers(self):
        temperament_scores = {
            'Sanguine': 0,
            'Choleric': 0,
            'Melancholic': 0,
            'Phlegmatic': 0
        }

        for question_id, answer in self.answers.items():
            response = answer.get()
            if response == 'Yes':
                if question_id in ['q1', 'q4', 'q8']:
                    temperament_scores['Sanguine'] += 1
                elif question_id in ['q2', 'q5', 'q9']:
                    temperament_scores['Choleric'] += 1
                elif question_id in ['q3', 'q7']:
                    temperament_scores['Melancholic'] += 1
                elif question_id in ['q6', 'q10']:
                    temperament_scores['Phlegmatic'] += 1

        temperament = max(temperament_scores, key=temperament_scores.get)

        # Display the temperament
        temperament_label = Label(self.root, text=f'Your temperament is: {temperament}', font=("Helvetica", 16))
        temperament_label.grid(column=0, row=17, columnspan=4, pady=10)

        # Add statement for movie recommendations
        recommendation_statement = Label(self.root, text=f'Based on your temperament, we recommend these movies:', font=("Helvetica", 14))
        recommendation_statement.grid(column=0, row=18, columnspan=4, pady=10)

        # Call movie recommendations based on temperament
        self.movie_recs(temperament)

    def create_movie_label(self, movie_name, row):
        Label(self.root, text=movie_name).grid(column=0, row=row, pady=5, columnspan=3)

    def movie_recs(self, temperament):
        recommendations = {
            'Sanguine': ['Toy Story', 'Finding Nemo', 'The Incredibles'],
            'Choleric': ['Gladiator', 'Mad Max: Fury Road', '300'],
            'Melancholic': ['The Fault in Our Stars', 'A Walk to Remember', 'Marley & Me'],
            'Phlegmatic': ['The Secret Life of Walter Mitty', 'Amélie', 'Julie & Julia']
        }

        movies = recommendations.get(temperament, [])
        for i, movie in enumerate(movies):
            self.create_movie_label(movie, 19 + i)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieRecommenderApp(root)
    root.mainloop()
