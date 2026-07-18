"""
Module 3 Project: Library Management System
models.py — SQLAlchemy models and database setup

Your job: Implement the models marked with # TODO.
All models must use SQLAlchemy 2.0 syntax: Mapped and mapped_column.
"""

from sqlalchemy import create_engine, String, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date
from typing import Optional

engine = create_engine("sqlite:///library.db", echo=False)


class Base(DeclarativeBase):
    pass


# Association table for Book <-> Author (many-to-many)
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id",   Integer, ForeignKey("books.id"),   primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)

book_genres = Table(
    "book_genres",
    Base.metadata,
    Column("book_id",   Integer, ForeignKey("books.id"),   primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id"), primary_key=True),
)


# Attributes: id (PK), name (required), bio (optional)
# Relationship: books (many-to-many via book_authors)
class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column()

    # relationship: many-to-many
    books: Mapped[list["Book"]] = relationship( 
        secondary=book_authors, back_populates="authors"
    )

    def __repr__(self):
        return f"Author: {self.name}"


class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    books: Mapped[list["Book"]] = relationship(secondary=book_genres, back_populates="genres")

    def __repr__(self):
        return f"Genre: {self.name}"



# Attributes: id (PK), name (required), email (unique, required), membership_date (date)
# Relationship: borrowings (one-to-many)
class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    membership_date:Mapped[date] = mapped_column()



    # relationship: (one-to-many)
    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="member", cascade="all, delete-orphan")



    def __repr__(self):
        return f"Name: {self.name}, Email: {self.email}, Membership date: {self.membership_date}"




# Attributes: id (PK), title (required), isbn (unique, required),
#             year_published (optional, integer), available_copies (integer, default 1)
# Relationships: authors (many-to-many via book_authors), borrowings (one-to-many)
class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    isbn: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    year_published:Mapped[Optional[int]] = mapped_column()
    available_copies: Mapped[int] = mapped_column(default=1)


    # relationship: authors (many-to-many via book_authors), borrowings (one-to-many)
    authors: Mapped[list["Author"]] = relationship( 
        secondary=book_authors, back_populates="books"
    )

    borrowings: Mapped[list["Borrowing"]] = relationship(back_populates="book", cascade="all, delete-orphan")

    genres: Mapped[list["Genre"]] = relationship(secondary=book_genres, back_populates="books")



    def __repr__(self):
        return f"Book: {self.title}, ISBN: {self.isbn}, Year published: {self.year_published}, Available copies: {self.available_copies}"






# Attributes: id (PK), book_id (FK -> books.id), member_id (FK -> members.id),
#             checkout_date (date), return_date (date, nullable — NULL means not yet returned)
# Relationships: book, member
class Borrowing(Base):
    __tablename__ = "borrowings"
    id: Mapped[int] = mapped_column(primary_key=True)

    # foreign key
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))

    checkout_date: Mapped[date] = mapped_column()
    return_date: Mapped[date] = mapped_column(nullable=True)

    # relationship: one-to-many
    book: Mapped["Book"] = relationship(back_populates="borrowings")
    member: Mapped["Member"] = relationship(back_populates="borrowings")


    def __repr__(self):
        return f"Borrowing ID: {self.id}, Book ID: {self.book_id}, Member ID: {self.member_id}, Checkout date: {self.checkout_date}, Return date: {self.return_date}"




def init_db():
    """Create all tables in the database. Call once before using any other functions."""
    Base.metadata.create_all(engine)
    print("Tables created!")

