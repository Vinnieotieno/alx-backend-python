#!/usr/bin/python3
import mysql.connector

def stream_users():
    try:
        # Connecting to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345", 
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True) 

        # Executing the query
        cursor.execute("SELECT * FROM user_data")

        # Yielding one row at a time
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
