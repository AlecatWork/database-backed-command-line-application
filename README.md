Library Management System

A command-line library management system built with SQLAlchemy 2.0 ORM and SQLite.
Supports books, authors, members, genres, and full borrowing/return tracking.



RELATIONSHIPS:
- Books ↔ Authors — many-to-many, via the book_authors association table (a book can have multiple authors; an author can write multiple books)
- Books ↔ Genres — many-to-many, via the book_genres association table (same shape as authors)
- Books ↔ Members (Borrowings) — the borrowings table tracks who borrowed what, with checkout_date and a nullable return_date (NULL means the book hasn't been returned yet)

SETUP:
Requirements: Python 3, SQLAlchemy 2.0
pip install sqlalchemy

FILES:
models.py - SQLAlchemy models and database engine setup
crud.py - Create/Read/Update/Delete functions — all database logic lives here
main.py - Interactive command-line menu
seed.py - Populates the database with sample data from sample_data.json
sample_data.json - Sample authors, books, members, and borrowings

TO RUN:
    # First time only — creates library.db and populates it with sample data
    python3 seed.py

    # Then, anytime — launch the interactive menu
    python3 main.py

Running seed.py again is safe — it adds to the existing data rather than replacing it, so avoid re-running it if you don't want duplicate sample records (duplicate ISBNs/emails will raise an error, since those columns are unique).

USAGE:
main.py presents a numbered menu covering every operation:

1.  Add a book               9.  Find books by author
2.  Add a member             10. Remove a book
3.  Search books             11. Remove a member
4.  Check out a book         12. Add an author
5.  Return a book            13. Update a member's email
6.  View member's borrowings 14. Tag a book with a genre
7.  View overdue books       15. Exit
8.  List all books

Each option prompts for the input it needs and prints a confirmation or an error message — invalid input (non-numeric IDs, checking out a book with no copies left, deleting a book/member with active borrowings, etc.) is caught and reported without crashing the program.


NOTES:
- Cascade deletes on borrowing history. Deleting a book or member also deletes their returned (historical) borrowing records — SQLite doesn't automatically null out foreign keys on delete, so without cascade="all, delete-orphan" on Book.borrowings/Member.borrowings, deleting a book with any borrowing history at all (even fully returned) would fail with a constraint error. Active (unreturned) borrowings still block deletion entirely, at the application level, before this ever comes into play.
- checkout_book()/return_book() accept an optional date. Both default to today for normal CLI use, but also accept an explicit checkout_date/return_date — this is what lets seed.py load historically-dated sample borrowings through the same CRUD functions the CLI uses, rather than duplicating that logic with raw session code.
- Member existence is validated at checkout, not just book existence — checking out a book to a nonexistent member ID is rejected with a clear error rather than silently creating an orphaned borrowing record.