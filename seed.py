"""
Module 3 Project: Library Management System
seed.py — Populate the database with sample data for testing.

Run after implementing your models and CRUD functions:
    python seed.py

Sample data is loaded from sample_data.json.
"""

import json
from datetime import date
from models import init_db, engine, Book, Author, Member
from crud import add_author, add_book, add_member, checkout_book, return_book
from sqlalchemy.orm import Session


def seed():
    """Load sample data from sample_data.json and insert it into the database."""
    init_db()

    with open("sample_data.json") as f:
        data = json.load(f)

    # each entry maps 1:1 onto add_author()'s parameters.
    for a in data["authors"]:
        add_author(a["name"], a.get("bio"))

   # Books — create, then link authors by name (add_book() has no author param)
    for b in data["books"]:
        new_book = add_book(b["title"], b["isbn"], b.get     ("year_published"), b.get("available_copies", 1))

        with Session(engine) as session:
            book = session.get(Book, new_book.id)
            for author_name in b["authors"]:
                author = session.query(Author).filter_by(name=author_name).first()
                if author is not None:
                    book.authors.append(author)
            session.commit()


    # Members
    for m in data["members"]:
        add_member(m["name"], m["email"])


    # Borrowings — look up book/member by isbn/email, checkout with the historical date, then return it if a return_date was given
    for br in data["borrowings"]:
        with Session(engine) as session:
            book = session.query(Book).filter_by(isbn=br["book_isbn"]).first()
            member = session.query(Member).filter_by(email=br["member_email"]).first()

        if book is None or member is None:
            print(f" Skipping borrowing. could not find book/member: {br}")
            continue

        checkout_date = date.fromisoformat(br["checkout_date"])
        new_borrowing = checkout_book(book.id, member.id, checkout_date=checkout_date)

        if br["return_date"]:
            return_date = date.fromisoformat(br["return_date"])
            return_book(new_borrowing.id, return_date=return_date)



    print("Seed complete!")


if __name__ == "__main__":
    seed()