"""
Module 3 Project: Library Management System
main.py — Command-line interface

Your job: Implement each menu handler function below.
The main menu loop is already provided — just fill in the handlers.
"""

from sqlalchemy.exc import IntegrityError

from models import init_db
from crud import (
    add_book, add_author, add_member, checkout_book, return_book,
    list_books, search_books_by_title, find_books_by_author,
    list_member_borrowings, list_overdue_books, delete_book, delete_member, update_member_email, add_genre_to_book
)


def handle_add_book():
    """Prompt for book details and add to the database."""
    title = input("Title: ")
    isbn = input("ISBN: ")
    year = input("Year published(leave blank if unknown): ").strip()
    year_published = int(year) if year else None
    available_copies = int(input("Number of available copies: "))

    new_book = add_book(title, isbn, year_published, available_copies)
    print(f" Added: {new_book}")


def handle_add_member():
    """Prompt for member details and register in the database."""
    name = input("Name: ")
    email = input("Email: ")

    new_member = add_member(name, email)
    print(f" Added: {new_member}")


def handle_add_author():
    """Prompt for author details and add to the database."""
    name = input("Author name: ")
    bio = input("Bio (leave blank if none): ").strip()
    bio = bio if bio else None

    add_author(name, bio)



def handle_search_books():
    """Prompt for a search term and display matching books."""
    title = input("Enter title: ")
    results = search_books_by_title(title)
    if not results:
        print("No books found.")
    else:
        for book in results:
            print(book)



def handle_checkout():
    """Prompt for book ID and member ID, then check out the book."""
    books = list_books()
    for book in books:
        print(book)
    try:
        book_id = int(input("Enter Book ID: "))
        member_id = int(input("Enter Member ID: "))
        checkout_book(book_id, member_id)
    except ValueError as e:
        print(f"Could not check out: {e}")


def handle_return():
    """Prompt for a borrowing ID and return the book."""
    borrowing_id = int(input("Borrowing ID: "))
    try:
        return_book(borrowing_id)
    except ValueError as e:
        print(f"Could not return book: {e}")



def handle_member_borrowings():
    """Display all active borrowings for a member."""
    member_id = int(input("Member ID: "))
    borrowings = list_member_borrowings(member_id)
    if not borrowings:
        print("No active borrowings for this member.")
    else:
        for b in borrowings:
            print(b)


def handle_overdue():
    """Display all overdue borrowings."""
    overdue = list_overdue_books()
    if not overdue:
        print("No overdue books.")
    else:
        for b in overdue:
            print(b)


def handle_find_by_author():
    """Prompt for an author name and display their books."""
    author_name = input("Enter author name: ")
    results = find_books_by_author(author_name)
    if not results:
        print("No books found for that author. ")
    else:
        for b in results:
            print(b)


def handle_list_books():
    """Display all books in the catalog."""
    books = list_books()
    if not books:
        print("No books in the catalog.")
    else:
        for b in books:
            print(b)

def handle_add_genre_to_book():
    """Prompt for a book ID and genre name, and tag the book with that genre."""
    try:
        book_id = int(input("Book ID: "))
    except ValueError:
        print("Book ID must be a number.")
        return
    genre_name = input("Genre name: ")
    try:
        add_genre_to_book(book_id, genre_name)
    except ValueError as e:
        print(f"Could not add genre: {e}")


def handle_delete_book():
    """Prompt for a book ID and delete it, if not currently borrowed."""
    try:
        book_id = int(input("Book ID: "))
        delete_book(book_id)
    except ValueError as e:
        print(f"Could not delete book: {e}")


def handle_delete_member():
    """Prompt for a member ID and delete it, if no active borrowings."""
    try:
        member_id = int(input("Member ID: "))
        delete_member(member_id)
    except ValueError as e:
        print(f"Could not delete member: {e}")


def handle_update_email():
    """Prompt for a member ID and new email, then update it."""
    try: 
        member_id = int(input("Member ID: "))
    except ValueError:
        print("Member ID must be a number. ")
        return
    
    new_email = input("New email: ")
    try:
        update_member_email(member_id, new_email)
    except IntegrityError:
        print(f"That email is already in use by a member. ")
    

def main():
    init_db()

    while True:
        print("\n📚 Library Management System")
        print("1.  Add a book")
        print("2.  Add a member")
        print("3.  Search books")
        print("4.  Check out a book")
        print("5.  Return a book")
        print("6.  View member's borrowings")
        print("7.  View overdue books")
        print("8.  List all books")
        print("9.  Find books by author")
        print("10. Remove a book")
        print("11. Remove a member")
        print("12. Add an author")
        print("13. Update a member's email")
        print("14. Tag a book with a genre")
        print("15. Exit")

        choice = input("\nChoose an option (1-15): ").strip()

        if choice == "1":
            handle_add_book()
        elif choice == "2":
            handle_add_member()
        elif choice == "3":
            handle_search_books()
        elif choice == "4":
            handle_checkout()
        elif choice == "5":
            handle_return()
        elif choice == "6":
            handle_member_borrowings()
        elif choice == "7":
            handle_overdue()
        elif choice == "8":
            handle_list_books()
        elif choice == "9":
            handle_find_by_author()
        elif choice == "10":
            handle_delete_book()
        elif choice == "11":
            handle_delete_member()
        elif choice == "12":
            handle_add_author()
        elif choice == "13":
            handle_update_email()
        elif choice == "14":
            handle_add_genre_to_book()
        elif choice == "15":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-15.")


if __name__ == "__main__":
    main()