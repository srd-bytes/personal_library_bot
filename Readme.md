# 📚 Personal Library Bot

A Structured Personal Digital Knowledge Management System\
Built with **Python + SQLite**

------------------------------------------------------------------------

# 🧠 Overview

**Personal Library Bot** is a command-line based digital library manager
designed for structured ebook organization.

It allows you to:

-   Organize books hierarchically\
-   Store metadata in a relational database\
-   Search intelligently using guided filtering\
-   Open PDFs and ZIP archives\
-   Maintain multiple independent databases\
-   Run locally or over SSH

This is a lightweight, portable knowledge system designed for structured
personal control.

------------------------------------------------------------------------

# 🏗 Architecture

The system is built using:

-   Python 3
-   SQLite (built-in with Python)
-   Structured relational schema
-   Many-to-many mapping for authors
-   Guided hierarchical filtering for search

------------------------------------------------------------------------

# 🗂 Project Structure

    master/
    │
    ├── finder/
    │   ├── bot.py
    │   ├── config.py
    │   ├── init_db.py
    │   ├── modify.py
    │   ├── search.py
    │   ├── database/
    │
    ├── library/
    │   └── example.pdf

------------------------------------------------------------------------

# ⚙ Requirements

-   Python 3.8+
-   SQLite (comes bundled with Python)
-   No external dependencies

------------------------------------------------------------------------

# ▶ Running the Application

From inside the `master` directory:

    python ./finder/bot.py

------------------------------------------------------------------------

# 🗄 Database Management

At startup you can:

-   Select an existing database from `finder/database/`
-   Or create a new one (e.g., `lib.db`)

If it does not exist, it is automatically initialized.

This allows maintaining multiple independent libraries.

------------------------------------------------------------------------

# 🧩 Database Schema

Tables used:

-   type
-   subject
-   topic
-   author
-   books
-   book_authors (many-to-many mapping)

Hierarchy:

Type → Subject → Topic → Book\
↘ Author(s)

------------------------------------------------------------------------

# ➕ Adding a Book

From the main menu:

    add

Provide:

-   Title
-   Path (relative to master directory, e.g. `./library/book.pdf`)
-   Type
-   Subject
-   Topic
-   Authors (comma separated)

If metadata does not exist, it is automatically created.

------------------------------------------------------------------------

# 🔎 Searching Books

From main menu:

    search

Search is fully guided:

1.  Select Type (or skip)
2.  Select Subject (filtered by Type)
3.  Select Topic (filtered by Type + Subject)
4.  Enter Author manually (optional)
5.  Enter Title keyword (optional)

Search is: - Case-insensitive - Partial match enabled - Hierarchically
filtered

------------------------------------------------------------------------

# 📖 Opening Books

After results:

    open 1
    open 2

You may open multiple books in one session.

If the file is a `.zip`, it opens in file explorer.

Press Enter to exit open mode.

------------------------------------------------------------------------

# 🗑 Deleting Books

From main menu:

    delete

Filter by metadata and confirm deletion.

Foreign key constraints ensure clean removal of mappings.

------------------------------------------------------------------------

# 📁 File Storage Strategy

Recommended:

-   Store PDFs/ZIPs in `library/`
-   Store databases in `finder/database/`
-   Use relative paths for portability

Example:

    ./library/linear_algebra.pdf

------------------------------------------------------------------------

# 🌍 Remote Execution (SSH)

Run remotely:

    ssh user@server_ip
    cd master
    python ./finder/library_bot.py

If running over SSH:

-   GUI file opening will not work
-   The program prints the absolute file path instead

To download from remote server:

    scp your_username@client_ip:/full/path/to/where_to_download/.

Now you dont have to type this. You need to provide path and your username.

    To get your username, run whoami command in your terminal

------------------------------------------------------------------------

# 🛡 Security

-   Fully local SQLite storage
-   No cloud dependency
-   Works offline

------------------------------------------------------------------------
# Message from Author

- Just add the finder folder, library folder and save the pdfs in that library folder using simple names
- Manage an Excel Sheet for tracking and tagging purpose (simple name, real name, author etc)
- switch on the bot and follow process
------------------------------------------------------------------------

# 👨‍💻 Author

Soumya Ranjan Das\
Electrical Engineering Student\
