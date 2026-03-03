# 📚 Personal Library Bot -- Developer Documentation

This document explains the internal architecture, code structure, and
extension points for developers who want to modify or extend the
Personal Library Bot.

------------------------------------------------------------------------

# 🧠 System Architecture

The system follows a modular CLI architecture:

User → library_bot.py → (modify.py / search.py) → SQLite Database

Each module has a clearly defined responsibility.

------------------------------------------------------------------------

# 📁 Module Responsibilities

## config.py

-   Handles runtime database path configuration
-   Builds dynamic DB path under finder/database/
-   `set_database(name)` must be called before any DB operation

## init_db.py

-   Initializes relational schema
-   Enforces foreign key constraints
-   Creates tables:
    -   type
    -   subject (linked to type)
    -   topic (linked to subject)
    -   author
    -   books
    -   book_authors (many-to-many)

## library_bot.py

-   Entry point of the application
-   Handles session start and DB selection
-   Displays CLI menu
-   Routes commands to modify.py and search.py

## modify.py

Contains: - add_book() - delete_book()

Key features: - Hierarchical guided selection (Type → Subject → Topic) -
get_or_create_id() prevents duplicate metadata - Many-to-many author
mapping - Safe deletion with confirmation

## search.py

Contains: - search_books() - open_book()

Features: - Guided hierarchical filtering - Case-insensitive search -
Partial match support - SSH detection for remote execution - SCP file
transfer option when running remotely

------------------------------------------------------------------------

# 🗄 Database Schema Overview

Hierarchy:

Type └── Subject └── Topic └── Book └── Author(s)

Key design patterns: - Foreign key constraints - UNIQUE composite keys -
Junction table for authors - Indexed searchable fields

------------------------------------------------------------------------

# 🔎 Search Logic

Search flow:

1.  Select Type (optional)
2.  Select Subject (filtered by Type)
3.  Select Topic (filtered by Type + Subject)
4.  Enter Author manually (optional)
5.  Enter Title keyword (optional)

SQL query dynamically builds WHERE conditions.

Results are returned as a list of tuples: (id, title, path, type,
subject, topic)

------------------------------------------------------------------------

# 📖 Remote Execution Handling

If running via SSH:

-   GUI open is disabled
-   User can SCP file to local machine
-   Uses SSH_CONNECTION environment variable detection

Developers should ensure: - subprocess module is imported - SCP command
properly formatted - Absolute paths used

------------------------------------------------------------------------
