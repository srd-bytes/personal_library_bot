import sqlite3
import config


def normalize(text):
    return text.strip().title()


def get_or_create_id(conn, table, name):
    c = conn.cursor()

    c.execute(f"SELECT id FROM {table} WHERE LOWER(name)=LOWER(?)", (name,))
    result = c.fetchone()

    if result:
        return result[0]

    c.execute(f"INSERT INTO {table} (name) VALUES (?)", (name,))
    return c.lastrowid


def add_book(title, path, type_name, subject_name, topic_name, authors):
    if not config.DB_NAME:
        raise ValueError("Database not set. Start session first.")

    conn = sqlite3.connect(config.DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # Normalize main fields
    title = title.strip()
    type_name = normalize(type_name)
    subject_name = normalize(subject_name)
    topic_name = normalize(topic_name)

    # Get or create type, subject, topic
    type_id = get_or_create_id(conn, "type", type_name)
    subject_id = get_or_create_id(conn, "subject", subject_name)
    topic_id = get_or_create_id(conn, "topic", topic_name)

    # Insert book
    c.execute("""
        INSERT INTO books (title, path, type_id, subject_id, topic_id)
        VALUES (?, ?, ?, ?, ?)
    """, (title, path, type_id, subject_id, topic_id))

    book_id = c.lastrowid

    # Handle multiple authors
    for author in authors:
        author = normalize(author)
        if author:
            author_id = get_or_create_id(conn, "author", author)
            c.execute("""
                INSERT OR IGNORE INTO book_authors (book_id, author_id)
                VALUES (?, ?)
            """, (book_id, author_id))

    conn.commit()
    conn.close()

    print("Book inserted successfully.")
    
def delete_book(type_name, subject, topic, author):
    if not config.DB_NAME:
        raise ValueError("Database not set. Start session first.")

    conn = sqlite3.connect(config.DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    query = """
    SELECT b.id, b.title
    FROM books b
    LEFT JOIN type t ON b.type_id = t.id
    LEFT JOIN subject s ON b.subject_id = s.id
    LEFT JOIN topic tp ON b.topic_id = tp.id
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    LEFT JOIN author a ON ba.author_id = a.id
    WHERE LOWER(t.name) = LOWER(?)
      AND LOWER(s.name) = LOWER(?)
      AND LOWER(tp.name) = LOWER(?)
      AND LOWER(a.name) = LOWER(?)
    GROUP BY b.id
    """

    c.execute(query, (type_name, subject, topic, author))
    results = c.fetchall()

    if not results:
        print("No matching book found.")
        conn.close()
        return

    print("\nMatching Books:\n")

    for index, (book_id, title) in enumerate(results, start=1):
        print(f"[{index}] {title}")

    choice = input("\nEnter number to delete (or 'back'): ").strip()

    if choice.lower() == "back":
        conn.close()
        return

    if not choice.isdigit():
        print("Invalid selection.")
        conn.close()
        return

    index = int(choice) - 1

    if index < 0 or index >= len(results):
        print("Invalid number.")
        conn.close()
        return

    book_id = results[index][0]
    confirm = input("Are you sure? (yes/no): ").strip().lower()

    if confirm == "yes":
        c.execute("DELETE FROM books WHERE id = ?", (book_id,))
        conn.commit()
        print("Book deleted successfully.")
    else:
        print("Deletion cancelled.")

    conn.close()
    conn.close()
if __name__ == "__main__":
    print("Add a new book")

    title = input("Title: ")
    path = input("Path: ")
    type_name = input("Type: ")
    subject_name = input("Subject: ")
    topic_name = input("Topic: ")
    authors_input = input("Authors (comma separated if multiple): ")

    authors = authors_input.split(",")

    add_book(title, path, type_name, subject_name, topic_name, authors)