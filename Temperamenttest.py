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


# Function to determine temperament based on answers
def temperament_test():
    print("Welcome to the temperament test!")
    name = input("Enter your name: ")

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

    return name, temperament


# Function to save the result to the database
def save_to_database(name, temperament):
    connection = connect_to_db()
    cursor = connection.cursor()

    query = "INSERT INTO test_results (user_name, temperament) VALUES (%s, %s)"
    cursor.execute(query, (user_name, temperament))

    connection.commit()
    print(f"Result for {user_name} has been saved to the database.")

    cursor.close()
    connection.close()


# Main function
if __name__ == "__main__":
    user_name, user_temperament = temperament_test()
    save_to_database(user_name, user_temperament)


