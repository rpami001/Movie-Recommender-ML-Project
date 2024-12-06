import mysql.connector
import getpass
import hashlib
import Movie_recommender as mr

def connect_to_db():
    #connect to database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Use your MySQL root username
        password="1234",  # Replace with your MySQL root password
        database="temperament_test"
    )
    return connection

def register_user(name, password,temperament):
    connection = connect_to_db()
    cursor = connection.cursor()
     # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # Insert user data into the database
    try:
        insert_query = """
        INSERT INTO test_results (user_name, password, temperament)
        VALUES (%s, %s, %s);
        """
        user_data = (name, hashed_password, temperament)
        cursor.execute(insert_query, user_data)
        connection.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


# Function to determine temperament based on answers
def temperament_test():
    print("Welcome to the temperament test!")
    name = input("Enter your name: ")
    password = getpass.getpass("Create a password:")

    print("Answer the following questions:")
    q1 = input("Do you enjoy being in social settings? (yes/no): ")
    q2 = input("Do you often plan and stick to routines? (yes/no): ")
    q3 = input("Do you easily get stressed under pressure? (yes/no): ")
    q4 = input("Do you prefer calm, quiet environments? (yes/no): ")

    # Determine temperament based on user answers
    score = {"melancholic": 0, "sanguine": 0, "choleric": 0, "phlegmatic": 0}

    if q1.lower() == "yes":
        score["sanguine"] += 1
        score["choleric"] += 1
    if q2.lower() == "yes":
        score["melancholic"] += 1
        score["phlegmatic"] += 1
    if q3.lower() == "yes":
        score["choleric"] += 1
    if q4.lower() == "yes":
        score["melancholic"] += 1
        score["phlegmatic"] += 1

    temperament = max(score, key=score.get)
    print(f"{name}, your temperament is {temperament}.")

    return name, password , temperament

def colour_test():
    print("Heyy how are you feeling today?")

    print("Answer the following questions:")
    colours = {"yellow":"happy","Red":"passionate","Black":"Sad","Blue":"Peaceful","Pink":"Feminine","White":"pure","Orange":"Excited","Neutral":"Neutral"}
    q1 = input(f"Choose a colour {colours.keys()}:")

    # Determine temperament based on user answers
    mood = colours.get(q1, "Unknown")  # Return "Unknown" if colour is not found

    print(f"your mood is {mood}.")

    return  mood

def login_user(name, password):
    connection = connect_to_db()
    cursor = connection.cursor()

    # Retrieve the hashed password for the given username
    query = "SELECT password FROM test_results WHERE user_name = %s;"
    cursor.execute(query, (name,))
    result = cursor.fetchone()

    if result:
        stored_password = result[0]
        # Hash the entered password and compare it with the stored hash
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == stored_password:
            print(f"Welcome back {name}!")
            return True
        else:
            print("Incorrect password.")
            return False
    else:
        print("User not found.")
        return False

    cursor.close()
    connection.close()

# prompt user to signup or login
def collect_user_info():
    p = input ('Do you have an account?: Yes/No ')
    if p.lower() in ["yes", "Yes","YES"]:
         name = input("Enter your name: ")
         password = getpass.getpass("password: ")
         login_user(name, password)
    elif p.lower() in ["No", "no", "NO"]:
         user_name, password , temperament = temperament_test()
         register_user( user_name, password , temperament)

def recommend_movie(mood):
    return mr.recommend_movies_based_on_user_mood(mood, mr.df, 5 )    

# Main function
if __name__ == "__main__":
    user_name,password, user_temperament = temperament_test()
    # print("Welcome to your emotion movie detector!")
    # collect_user_info()
    results = recommend_movie(user_temperament)
    print(results)
    

