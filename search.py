import sqlite3
import config
import os
import sys

def get_distinct(conn, query, params=()):
    c = conn.cursor()
    c.execute(query, params)
    return [row[0] for row in c.fetchall()]


def select_option(title, values):
    if not values:
        print(f"\nNo {title} options found.")
        return None

    print(f"\nSelect {title}:")
    for i, v in enumerate(values, start=1):
        print(f"[{i}] {v}")

    user_input = input("Enter number, type new, or press Enter to skip: ").strip()

    if not user_input:
        return None

    if user_input.isdigit():
        index = int(user_input) - 1
        if 0 <= index < len(values):
            return values[index]
        else:
            print("Invalid selection.")
            return None

    return user_input

def search_books():

    if not config.DB_NAME:
        raise ValueError("Database not set. Start session first.")

    conn = sqlite3.connect(config.DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    c = conn.cursor()

    # ===============================
    # GUIDED FILTER SELECTION
    # ===============================

    print("\nSearch Filters\n")

    # TYPE
    types = get_distinct(conn, "SELECT DISTINCT name FROM type")
    type_name = select_option("Type", types)

    # SUBJECT
    if type_name:
        subjects = get_distinct(conn, """
            SELECT DISTINCT s.name
            FROM subject s
            JOIN books b ON s.id = b.subject_id
            JOIN type t ON b.type_id = t.id
            WHERE LOWER(t.name) = LOWER(?)
        """, (type_name,))
    else:
        subjects = get_distinct(conn, "SELECT DISTINCT name FROM subject")

    subject = select_option("Subject", subjects)

    # TOPIC
    if type_name and subject:
        topics = get_distinct(conn, """
            SELECT DISTINCT tp.name
            FROM topic tp
            JOIN books b ON tp.id = b.topic_id
            JOIN type t ON b.type_id = t.id
            JOIN subject s ON b.subject_id = s.id
            WHERE LOWER(t.name) = LOWER(?)
            AND LOWER(s.name) = LOWER(?)
        """, (type_name, subject))
    else:
        topics = get_distinct(conn, "SELECT DISTINCT name FROM topic")

    topic = select_option("Topic", topics)

    # AUTHOR → manual typing only
    author = input("Author (Enter to skip): ").strip() or None

    # TITLE
    title_keyword = input("Title keyword (Enter to skip): ").strip() or None

    # ===============================
    # YOUR ORIGINAL SEARCH QUERY
    # ===============================

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
        return []

    for idx, (book_id, title, path, type_name, subject, topic) in enumerate(results, start=1):

        c.execute("""
            SELECT a.name
            FROM author a
            JOIN book_authors ba ON a.id = ba.author_id
            WHERE ba.book_id = ?
        """, (book_id,))
        authors = [row[0] for row in c.fetchall()]

        print("--------------------------------------------------")
        print(f"[{idx}] Title   : {title}")
        print(f"    Type    : {type_name}")
        print(f"    Subject : {subject}")
        print(f"    Topic   : {topic}")
        print(f"    Authors : {', '.join(authors) if authors else 'N/A'}")
        print(f"    Path    : {path}")
        print("--------------------------------------------------\n")

    conn.close()
    return results

def open_book(path):

    if not os.path.exists(path):
        print(f"File not found: {path}")
        return

    absolute_path = os.path.abspath(path)

    is_ssh = "SSH_CONNECTION" in os.environ

    if is_ssh:
        print("\n⚠ SSH session detected.")

        choice = input("Download file to your local machine using SCP? (yes/no): ").strip().lower()

        if choice != "yes":
            print("Cancelled.")
            return

        ssh_info = os.environ.get("SSH_CONNECTION")
        client_ip = ssh_info.split()[0]

        username = input("Enter your local machine username: ").strip()
        destination = input("Enter local destination absolute path (e.g. [Linux: /home/...] [Windows: C:/Users/...use forward slash] ): ").strip()

        scp_command = [
            "scp",
            absolute_path,
            f"{username}@{client_ip}:{destination}"
        ]

        try:
            subprocess.run(scp_command, check=True)
            print("File copied successfully.")
        except Exception as e:
            print(f"SCP failed: {e}")

        return

    # Normal GUI open
    try:
        if sys.platform.startswith("win"):
            os.startfile(absolute_path)
        elif sys.platform.startswith("darwin"):
            os.system(f'open "{absolute_path}"')
        else:
            os.system(f'xdg-open "{absolute_path}"')

        print("Opening file...")

    except Exception as e:
        print(f"Failed to open file: {e}")
        print(f"File path: {absolute_path}")
# -------------------Test----------------------
