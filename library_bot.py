import config
import sqlite3
import os
from init_db import initialize_database
from modify import add_book, delete_book
from search import search_books, open_book


def start_session():

    database_dir = os.path.join(os.path.dirname(config.DB_NAME or ""), "database")

    # If config.DB_NAME is None (first run), rebuild base path properly
    if not database_dir or database_dir == "database":
        base_dir = os.path.dirname(os.path.abspath(__file__))
        database_dir = os.path.join(base_dir, "database")

    os.makedirs(database_dir, exist_ok=True)

    # List existing databases
    db_files = [f for f in os.listdir(database_dir) if f.endswith(".db")]

    print("\n====== Available Databases ======\n")

    if db_files:
        for i, db in enumerate(db_files, start=1):
            print(f"[{i}] {db}")
    else:
        print("No databases found.")

    print("\nType number to select database.")
    print("Or type a new database name to create one.\n")

    choice = input("Your choice: ").strip()

    # If user selects existing DB by number
    if choice.isdigit():
        index = int(choice) - 1

        if 0 <= index < len(db_files):
            db_name = db_files[index]
        else:
            print("Invalid selection. Creating new database.")
            db_name = choice
    else:
        db_name = choice

    # Ensure it ends with .db
    if not db_name.endswith(".db"):
        db_name += ".db"

    config.set_database(db_name)

    # Initialize if new
    if not os.path.exists(config.DB_NAME):
        print("\nDatabase not found. Initializing new database...\n")
        initialize_database()
    else:
        print("\nExisting database loaded.\n")

    print(f"Using database: {config.DB_NAME}\n")

def menu():
    print("\n====== Personal Library Bot ======")
    print("add : Add Book")
    print("search : Search Books")
    print("delete : Delete Book")
    print("exit : Exit")

if __name__ == "__main__":
    try:
        start_session()
    except Exception as e:
        print(f"\nError during session start: {e}")
        exit()

    while True:
        menu()
        choice = input("Choose an option: ").strip().lower()

        if choice == "add":
            while True:
                try:
                    print("\nAdd a new book (type 'back' anytime to return)\n")

                    title = input("Title: ")
                    if title.lower() == "back":
                        break

                    path = input("Path: ")
                    if path.lower() == "back":
                        break

                    type_name = input("Type: ")
                    if type_name.lower() == "back":
                        break

                    subject_name = input("Subject: ")
                    if subject_name.lower() == "back":
                        break

                    topic_name = input("Topic: ")
                    if topic_name.lower() == "back":
                        break

                    authors_input = input("Authors (comma separated): ")
                    if authors_input.lower() == "back":
                        break

                    authors = authors_input.split(",")

                    add_book(title, path, type_name, subject_name, topic_name, authors)

                    print("\nBook added successfully.\n")

                except Exception as e:
                    print(f"\nError adding book: {e}\n")

        elif choice == "search":
            while True:
                try:
                    print("\nSearch Library (type 'back' anytime to return)\n")

                    type_name = input("Type (Enter to skip): ").strip()
                    if type_name.lower() == "back":
                        break
                    type_name = type_name or None

                    subject = input("Subject (Enter to skip): ").strip()
                    if subject.lower() == "back":
                        break
                    subject = subject or None

                    topic = input("Topic (Enter to skip): ").strip()
                    if topic.lower() == "back":
                        break
                    topic = topic or None

                    author = input("Author (Enter to skip): ").strip()
                    if author.lower() == "back":
                        break
                    author = author or None

                    title_keyword = input("Title keyword (Enter to skip): ").strip()
                    if title_keyword.lower() == "back":
                        break
                    title_keyword = title_keyword or None

                    results=search_books(type_name, subject, topic, author, title_keyword)
                    
                    if results:
                        while True:
                            action = input(
                                "\nType 'open <number>', 'back' to search again, or press Enter to continue: "
                            ).strip().lower()

                            if action == "":
                                break  # Exit open loop

                            if action == "back":
                                break  # Return to search input

                            if action.startswith("open"):
                                parts = action.split()

                                if len(parts) == 2 and parts[1].isdigit():
                                    index = int(parts[1]) - 1

                                    if 0 <= index < len(results):
                                        path = results[index][2]
                                        open_book(path)
                                    else:
                                        print("Invalid number.")
                                else:
                                    print("Invalid open command format. Use: open <number>")

                            else:
                                print("Unknown command.")

                except Exception as e:
                    print(f"\nSearch error: {e}\n")


        elif choice == "delete":
            while True:
                try:
                    print("\nDelete Book (type 'back' anytime to return)\n")

                    type_name = input("Type: ")
                    if type_name.lower() == "back":
                        break

                    subject = input("Subject: ")
                    if subject.lower() == "back":
                        break

                    topic = input("Topic: ")
                    if topic.lower() == "back":
                        break

                    author = input("Author: ")
                    if author.lower() == "back":
                        break

                    from delete_book import delete_book
                    delete_book(type_name, subject, topic, author)

                except Exception as e:
                    print(f"Delete error: {e}")

        elif choice == "exit":
            print("Goodbye.")
            break

        else:
            print("Invalid option.")