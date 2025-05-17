#!/usr/bin/python3
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields ages of users one by one from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()


def compute_average_age():
    """
    Computes and prints the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():  # First and only loop
        total_age += age
        count += 1

    average_age = total_age / count if count else 0
    print(f"Average age of users: {average_age}")
