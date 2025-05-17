
"""
- Write a function stream_users_in_batches(batch_size) that fetches rows in batches

- Write a function batch_processing() that processes each batch to filter users over the age of25`

- You must use no more than 3 loops in your code. Your script must use the yield generator
"""

import pymysql
import pymysql.cursors


def stream_users_in_batches(batch_size):
    connection = pymysql.connect(
        host="localhost",
        user="bix",
        password="",
        database="ALX_prodev",
        cursorclass=pymysql.cursors.DictCursor,
    )

    rows = None

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM user_data LIMIT %s", batch_size)
            rows = cursor.fetchall()
            if not rows:
                return None
            yield rows
    finally:
        connection.close()


def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        users_over_25 = (user for user in batch if user["age"] > 25)
        for user in users_over_25:
            yield user
            print(user)


batch_processing(50)
