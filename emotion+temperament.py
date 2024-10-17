import mysql.connector


# Connect to MySQL database
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Use your MySQL root username
        password="1234",  # Replace with your MySQL root password
        database="temperament_test"
    )
    return connection


def get_user_input():
    questions = [
        "1. I feel energized when I'm around a lot of people. (1/2/3/4/5)",
        "2. I tend to take charge in group situations. (1/2/3/4/5)",
        "3. I often reflect on my feelings and thoughts. (1/2/3/4/5)",
        "4. I prefer a calm and predictable environment. (1/2/3/4/5)",
        "5. I enjoy trying new things and meeting new people. (1/2/3/4/5)",
        "6. I get frustrated when things don’t go my way. (1/2/3/4/5)",
        "7. I feel deeply affected by the problems of others. (1/2/3/4/5)",
        "8. I value harmony and dislike conflict. (1/2/3/4/5)",
        "9. I often find myself daydreaming. (1/2/3/4/5)",
        "10. I like to plan things out in detail before starting. (1/2/3/4/5)"
    ]
    
    responses = []
    for question in questions:
        response = input(question + " ")
        responses.append(response.strip().upper())
    
    return responses

def calculate_scores(responses):
    sanguine = 0
    choleric = 0
    melancholic = 0
    phlegmatic = 0
    
    scoring = {
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5
    }

    for i, response in enumerate(responses):
        points = scoring.get(response, 0)
        if i in [0, 4]:  # Questions 1 & 5 for Sanguine
            sanguine += points
        elif i in [1, 5]:  # Questions 2 & 6 for Choleric
            choleric += points
        elif i in [2, 6, 8]:  # Questions 3, 7, 9 for Melancholic
            melancholic += points
        elif i in [3, 7, 9]:  # Questions 4, 8, 10 for Phlegmatic
            phlegmatic += points
    
    return sanguine, choleric, melancholic, phlegmatic

def interpret_results(scores):
    sanguine, choleric, melancholic, phlegmatic = scores
    results = {}

    if sanguine >= 8:
        results['Sanguine'] = "You feel excited and energized in social situations."
    if choleric >= 8:
        results['Choleric'] = "You are driven and assertive, often taking charge."
    if melancholic >= 10:
        results['Melancholic'] = "You are introspective and sensitive, feeling deeply."
    if phlegmatic >= 10:
        results['Phlegmatic'] = "You value peace and stability, seeking harmony."
    
    return results

emotion_color_dict = {
    "Choleric": "yellow",
    "Phlegmatic": "blue",
    "angry": "red",
    "Sanguine": "orange",
    "Melancholic": "green",
    "anxious": "gray",
}

if __name__ == "__main__":
    print("Welcome to the Temperament-Based Personality Test!")
    responses = get_user_input()
    scores = calculate_scores(responses)
    results = interpret_results(scores)
    
    print("\nYour Emotional Temperament Results:")
    for temperament, description in results.items():
        print(f"{temperament}: {description}")

    if temperament in emotion_color_dict:
        color = emotion_color_dict[temperament]
        print(f'Based on your replies the color best associated with your emotion: {temperament} is {color}.')

    else:
        print('It is hard to pinpoint an emotion lets try again.')