import sqlite3
import config
import os

def search_books(type_name=None, subject=None, topic=None, author=None, title_keyword=None):
    if not config.DB_NAME:
        raise ValueError("Database not set. Start session first.")

    conn = sqlite3.connect(config.DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    query = """
    SELECT 
        b.id,
        b.title,
        b.path,
        t.name AS type_name,
        s.name AS subject,
        tp.name AS topic
    FROM books b
    LEFT JOIN type t ON b.type_id = t.id
    LEFT JOIN subject s ON b.subject_id = s.id
    LEFT JOIN topic tp ON b.topic_id = tp.id
    LEFT JOIN book_authors ba ON b.id = ba.book_id
    LEFT JOIN author a ON ba.author_id = a.id
    WHERE 1=1
    """

    params = []

    if type_name:
        query += " AND LOWER(t.name) LIKE LOWER(?)"
        params.append(f"%{type_name}%")

    if subject:
        query += " AND LOWER(s.name) LIKE LOWER(?)"
        params.append(f"%{subject}%")

    if topic:
        query += " AND LOWER(tp.name) LIKE LOWER(?)"
        params.append(f"%{topic}%")

    if author:
        query += " AND LOWER(a.name) LIKE LOWER(?)"
        params.append(f"%{author}%")

    if title_keyword:
        query += " AND LOWER(b.title) LIKE LOWER(?)"
        params.append(f"%{title_keyword}%")

    query += " GROUP BY b.id"

    c.execute(query, params)
    results = c.fetchall()

    if not results:
        print("\nNo books found.\n")
        conn.close()
        return

    for book_id, title, path, type_name, subject, topic in results:

        # Fetch all authors for this book
        c.execute("""
            SELECT a.name
            FROM author a
            JOIN book_authors ba ON a.id = ba.author_id
            WHERE ba.book_id = ?
        """, (book_id,))
        authors = [row[0] for row in c.fetchall()]

        print("--------------------------------------------------")
        print(f"Title   : {title}")
        print(f"Type    : {type_name}")
        print(f"Subject : {subject}")
        print(f"Topic   : {topic}")
        print(f"Authors : {', '.join(authors) if authors else 'N/A'}")
        print(f"Path    : {path}")
        print("--------------------------------------------------\n")

    conn.close()
    return results

import sys


def open_book(path):

    # Convert to absolute path relative to project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

    absolute_path = os.path.abspath(os.path.join(project_root, path))

    if not os.path.exists(absolute_path):
        print(f"File not found on disk: {absolute_path}")
        return

    try:
        if sys.platform.startswith("win"):
            os.startfile(absolute_path)
        elif sys.platform.startswith("darwin"):
            os.system(f'open "{absolute_path}"')
        else:
            os.system(f'xdg-open "{absolute_path}"')

        print("Opening book...")

    except Exception as e:
        print(f"Failed to open file: {e}")

# -------------------Test----------------------
if __name__ == "__main__":
    print("\nSearch Library\n")

    type_name = input("Type (Enter to skip): ").strip() or None
    subject = input("Subject (Enter to skip): ").strip() or None
    topic = input("Topic (Enter to skip): ").strip() or None
    author = input("Author (Enter to skip): ").strip() or None
    title_keyword = input("Title keyword (Enter to skip): ").strip() or None

    search_books(type_name, subject, topic, author, title_keyword)