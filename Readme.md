# 📚 Personal Library Bot

A command-line based personal digital library manager built with
**Python + SQLite**.

This tool allows you to organize, search, and open your ebooks locally
using a structured SQL database with tagging support.

------------------------------------------------------------------------

## 🚀 Features

-   Multi-database support
-   Structured tagging: Type / Subject / Topic / Author
-   Many-to-many author mapping
-   Case-insensitive and partial-match search
-   Open PDF directly from search results
-   Delete books using metadata filters
-   Session-based database selection
-   Cross-platform PDF opening (Windows / Mac / Linux)

------------------------------------------------------------------------

## 🗂 Project Structure

    master/
    │
    ├── finder/
    │   ├── library_bot.py
    │   ├── config.py
    │   ├── init_db.py
    │   ├── modify.py
    │   ├── search.py
    │   ├── database/
    │   
    │
    ├── library/
    │   └── example.pdf

------------------------------------------------------------------------

## ⚙ Requirements

-   Python 3.8+
-   SQLite (comes built-in with Python)

No external packages required.

------------------------------------------------------------------------

## ▶ How To Run

Navigate to the finder directory:

``` bash
python ./finder/library_bot.py
```

------------------------------------------------------------------------

## 🗄 Database Selection

At startup:

-   Enter a new database name (e.g., lib.db)
-   Or load an existing one from finder/database/
-   This allows you to make multiple databases for multiple libraries inside  the master directory.

If it does not exist, it is automatically initialized.

------------------------------------------------------------------------

## ➕ Adding a Book

Choose:

    add

Provide:

-   Title
-   Path (e.g., ./library/book.pdf (with respect to master))
-   Type (e.g., book, question_paper etc)
-   Subject (e.g., math, electrical_engineering, finance etc)
-   Topic (e.g., linear_algebra, ordinary_differential_equations, stocashtic_calculus etc)
-   Authors (comma separated)

------------------------------------------------------------------------

## 🔎 Searching Books

Choose:

    search

You can filter by:

-   Type
-   Subject
-   Topic
-   Author
-   Title keyword

Search is case-insensitive and supports partial matches.

------------------------------------------------------------------------

## 📖 Opening Books

After search results appear:

    open 1

You can open multiple books in one session:

    open 1
    open 2
    open 3

Press Enter to exit open mode.

------------------------------------------------------------------------

## 🗑 Deleting Books

Choose:

    delete

Provide metadata filters to remove matching books from the database.

------------------------------------------------------------------------

## 📁 File Storage Strategy

-   PDFs stored in library/
-   Databases stored in finder/database/
-   Relative paths used for portability


------------------------------------------------------------------------

## 👨‍💻 Author

Soumya Ranjan Das\
Electrical Engineering Student\
Personal Knowledge System Builder
