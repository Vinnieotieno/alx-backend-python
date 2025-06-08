query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("[CACHE] Returning cached result.")
            return query_cache[query]
        result = func(conn, query)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

users = fetch_users_with_cache(query="SELECT * FROM users")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
