"""
Module 3 Project: Library Management System
crud.py — Create, Read, Update, Delete operations

Your job: Implement every function below.
Import your models and engine from models.py.
"""

from models import engine, Book, Author, Member, Borrowing, Genre
from sqlalchemy.orm import Session
from datetime import date, timedelta


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────

def add_book(title: str, isbn: str, year_published: int = None,
             available_copies: int = 1):
    """Add a new book to the database. Returns the created Book object."""
    # TODO: open a Session, create a Book, add + commit, return it
    with Session(engine) as session: 
        new_book = Book(title=title, isbn=isbn, year_published=year_published, available_copies=available_copies)
        
        session.add(new_book)
        session.commit()
        session.refresh(new_book)
        print(f" Created: {new_book}")
        return new_book
            



def add_author(name: str, bio: str = None):
    """Add a new author. Returns the created Author object."""
    # TODO: implement
    with Session(engine) as session: 
        new_author = Author(name=name, bio=bio)
        
        session.add(new_author)
        session.commit()
        session.refresh(new_author)
        print(f" Added: {new_author}")
        return new_author
        


def add_member(name: str, email: str):
    """
    Register a new member with today's date as membership_date.
    Returns the created Member object.
    """
    # TODO: implement
    with Session(engine) as session: 
        new_member = Member(name=name, email=email, membership_date=date.today())
        
        session.add(new_member)
        session.commit()
        session.refresh(new_member)
        print(f" Added: {new_member}")
        return new_member
        


def checkout_book(book_id: int, member_id: int, checkout_date: date=None):
    """
    Check out a book to a member.
    Decrements available_copies by 1 and sets checkout_date to today.
    Raises ValueError if available_copies == 0.
    Returns the created Borrowing object.
    """
    checkout_date = checkout_date or date.today()
    with Session(engine) as session: 
        book = session.get(Book, book_id)
        if book is None:
            raise ValueError(f"No book with id {book_id}")
        member = session.get(Member, member_id)
        if member is None:
            raise ValueError(f"No member with id {member_id}")
        if book.available_copies == 0:
            raise ValueError(f"'{book.title}' has no available copies")
        
        book.available_copies -= 1
        new_borrowing = Borrowing(book_id=book_id, member_id=member_id,checkout_date=checkout_date)
        session.add(new_borrowing)
        session.commit()
        session.refresh(new_borrowing)
        print(f"'{book.title}' has been checked out. (Borrowing ID: {new_borrowing.id})")
        return new_borrowing



# ──────────────────────────────────────────
# READ
# ──────────────────────────────────────────

def list_books():
    """Return a list of all Book objects."""
    # TODO: implement
    with Session(engine) as session: 
        return session.query(Book).all()


def search_books_by_title(title: str):
    """Return books whose title contains the given string (case-insensitive)."""
    # TODO: implement
    with Session(engine) as session: 
        return session.query(Book).filter(Book.title.ilike(f"%{title}%")).all()


def find_books_by_author(author_name: str):
    """Return all books associated with an author whose name contains author_name."""
    # TODO: implement
    with Session(engine) as session: 
        return (
            session.query(Book)
            .join(Book.authors)
            .filter(Author.name.ilike(f"%{author_name}%"))
            .all()       
        )


def list_member_borrowings(member_id: int):
    """Return all active (unreturned) Borrowing objects for the given member."""
    # TODO: implement
    with Session(engine) as session: 
        return (
            session.query(Borrowing)
            .filter_by(member_id=member_id, return_date=None)
            .all()       
        )

def add_genre(name: str):
    """Add a new genre. Returns the created Genre object."""
    with Session(engine) as session:
        new_genre = Genre(name=name)
        session.add(new_genre)
        session.commit()
        session.refresh(new_genre)
        print(f" Added: {new_genre}")
        return new_genre

def add_genre_to_book(book_id: int, genre_name: str):
    """
    Link a book to a genre by genre name (creating the genre if it
    doesn't exist yet). Returns the updated Book object.
    """
    with Session(engine) as session:
        book = session.get(Book, book_id)
        if book is None:
            raise ValueError(f"No book with id {book_id}")
        
        genre = session.query(Genre).filter_by(name=genre_name).first()
        if genre is None:
            genre = Genre(name=genre_name)
            session.add(genre)

        if genre not in book.genres:
            book.genres.append(genre)
        session.commit()
        session.refresh(book)
        print(f" '{book.title}' tagged with genre '{genre_name}'")
        return book


def list_overdue_books(days: int = 14):
    """
    Return Borrowing objects where return_date is NULL and
    checkout_date is more than `days` days ago.
    """
    # TODO: implement 
    cutoff = date.today() - timedelta(days=days)
    with Session(engine) as session: 
        return (
            session.query(Borrowing)
            .filter(Borrowing.return_date.is_(None), Borrowing.checkout_date < cutoff)
            .all()       
        )


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────

def return_book(borrowing_id: int, return_date = None):
    """
    Mark a borrowing as returned.
    Sets return_date to today and increments book.available_copies by 1.
    Raises ValueError if the borrowing is not found or already returned.
    """
    # TODO: implement
    return_date = return_date or date.today()
    with Session(engine) as session: 
        borrowing = session.get(Borrowing, borrowing_id)
        if borrowing is None:
            raise ValueError(f"No borrowing with id {borrowing_id}")
        if borrowing.return_date is not None:
            raise ValueError(f"This book was already returned")
        
        borrowing.return_date = return_date
        borrowing.book.available_copies += 1
        session.commit()
        session.refresh(borrowing)
        print(f" Returned: {borrowing}")
        return borrowing
        



def update_member_email(member_id: int, new_email: str):
    """Update the email address for a member. Returns the updated Member object."""
    # TODO: implement
    with Session(engine) as session: 
        member = session.get(Member, member_id)
        if member is None:
            print(f" Member not found")
            return None
        
        old = member.email
        member.email = new_email
        session.commit()
        session.refresh(member)
        print(f" Updated: {old} -> {new_email}")
        return member
        
        



# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────

def delete_book(book_id: int):
    """
    Delete a book from the database.
    Raises ValueError if the book has any active (unreturned) borrowings.
    """
    # TODO: implement
    with Session(engine) as session: 
        book = session.get(Book, book_id)
        if book is None:
            print("Book not found")
            return
        
        active = session.query(Borrowing).filter_by(book_id=book_id, return_date=None).first()
        if active is not None:
            raise ValueError(F"'{book.title}' has an active borrowing and cannot be deleted.")
        
        title = book.title
        session.delete(book)
        session.commit()
        print(f" The book {title} has been deleted")



def delete_member(member_id: int):
    """
    Delete a member from the database.
    Raises ValueError if the member has any active (unreturned) borrowings.
    """
    # TODO: implement
    with Session(engine) as session: 
        member = session.get(Member, member_id)
        if member is None:
            print("Member not found")
            return
        
        active = session.query(Borrowing).filter_by(member_id=member_id, return_date=None).first()
        if active is not None:
            raise ValueError(F"'{member.name}' has active borrowings and cannot be deleted.")
        
        name = member.name
        session.delete(member)
        session.commit()
        print(f"{name} has been deleted")

