#!/usr/bin/python3


DB_NAME = "ALX_prodev"

# Connect to the MySQL server 
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345"  
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None



# Create the database if it doesn't exist
def create_database(connection):
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")
    finally:
        cursor.close()



# Connect to the ALX_prodev database
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",  
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        return None

# Create the user_data table
def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS user_id_idx ON user_data(user_id);")
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Failed to create table: {err}")
    finally:
        cursor.close()


# Insert data from CSV file into the user_data table
def insert_data(connection, csv_file):
    cursor = connection.cursor()
    try:
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row.get('user_id') or str(uuid.uuid4())
                name = row['name']
                email = row['email']
                age = row['age']

                # Check for existing user_id to avoid duplicates
                cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (user_id,))
                if not cursor.fetchone():
                    cursor.execute("""
                        INSERT INTO user_data (user_id, name, email, age)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, name, email, age))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()
