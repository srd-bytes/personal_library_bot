import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = None

def set_database(name):
    global DB_NAME
    DB_NAME = os.path.join(BASE_DIR, "database", name)