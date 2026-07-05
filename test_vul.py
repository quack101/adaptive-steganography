import sqlite3
import os

# Hardcoded credentials - the AI reviewer should flag this immediately
DB_PASSWORD = "admin123"
API_KEY = "sk-test-1234567890abcdefghijklmnop"

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # SQL injection - string formatting directly into the query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchone()

def divide_scores(scores, count):
    # Potential division by zero - no check on count
    average = sum(scores) / count
    return average

def read_user_file(filename):
    # Path traversal - no validation on filename before joining
    filepath = os.path.join("/app/user_uploads/", filename)
    with open(filepath, "r") as f:
        return f.read()

def process_items(items):
    # Off-by-one: loop goes one index too far
    for i in range(len(items) + 1):
        print(items[i])
