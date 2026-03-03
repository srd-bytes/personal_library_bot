import sqlite3
import config
import os



def initialize_database():
    db_path = config.DB_NAME
    # Ensure database folder exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # TYPE table
    c.execute("""
    CREATE TABLE IF NOT EXISTS type (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # SUBJECT table
    c.execute("""
    CREATE TABLE IF NOT EXISTS subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    type_id INTEGER,
    UNIQUE(name, type_id),
    FOREIGN KEY (type_id) REFERENCES type(id)
    )
    """)

    # TOPIC table
    c.execute("""
    CREATE TABLE IF NOT EXISTS topic (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    subject_id INTEGER,
    UNIQUE(name, subject_id),
    FOREIGN KEY (subject_id) REFERENCES subject(id)
    )
    """)

    # AUTHOR table
    c.execute("""
    CREATE TABLE IF NOT EXISTS author (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    )
    """)

    # BOOKS table
    c.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        path TEXT NOT NULL,
        type_id INTEGER,
        subject_id INTEGER,
        topic_id INTEGER,
        FOREIGN KEY (type_id) REFERENCES type(id),
        FOREIGN KEY (subject_id) REFERENCES subject(id),
        FOREIGN KEY (topic_id) REFERENCES topic(id)
    )
    """)

    # MANY-TO-MANY BOOK ↔ AUTHOR
    c.execute("""
    CREATE TABLE IF NOT EXISTS book_authors (
        book_id INTEGER,
        author_id INTEGER,
        PRIMARY KEY (book_id, author_id),
        FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY (author_id) REFERENCES author(id) ON DELETE CASCADE
    )
    """)

    # Indexes for fast searching
    c.execute("CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_type_name ON type(name)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_subject_name ON subject(name)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_topic_name ON topic(name)")
    c.execute("CREATE INDEX IF NOT EXISTS idx_author_name ON author(name)")

    conn.commit()
    conn.close()

    print("Database initialized successfully.")