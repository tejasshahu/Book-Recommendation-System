from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

from database import get_db
from models import Book, Review
from schemas import BookCreate, BookUpdate, ReviewCreate, BookResponse, ReviewResponse
from utility import basic_auth

# Router to separate API views
router = APIRouter()

import pickle
import numpy as np
import logging



# API Endpoints

@router.post("/books", response_model=BookResponse)
def add_book(book: BookCreate, db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    books = db.query(Book).all()
    return books


@router.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db),
                username: str = Depends(basic_auth)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()
    return {"id": book_id, "deleted": True}


@router.post("/books/{book_id}/reviews", response_model=ReviewResponse)
def add_review(book_id: int, review: ReviewCreate, db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_review = Review(book_id=book_id, review_text=review.review_text, rating=review.rating,
                       user_id=1)  # Simulate user_id
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/books/{book_id}/reviews", response_model=list[ReviewResponse])
def get_reviews(book_id: int, db: Session = Depends(get_db), username: str = Depends(basic_auth)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    return reviews


@router.post('/recommend_books')
def recommend(user_input: str, username: str = Depends(basic_auth)):
    pt = pickle.load(open('../ml/pt.pkl', 'rb'))
    books = pickle.load(open('../ml/books.pkl', 'rb'))
    similarity_scores = pickle.load(open('../ml/similarity_scores.pkl', 'rb'))
    user_input = str(user_input)
    data = []
    try:
        index = np.where(pt.index == user_input)[0][0]
    except IndexError as e:
        return "Sorry, entered book is not available in Database"
    except Exception as general_exception:
        logging.error(general_exception)
        return "Sorry, entered book is not available in Database"
    else:
        similar_items = sorted(list(enumerate(similarity_scores[index])),
                               key=lambda x: x[1], reverse=True)[1:6]
        for i in similar_items:
            book_dict = {}
            temp_df = books[books['Book-Title'] == pt.index[i[0]]]
            book_dict["Book-Title"] = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            book_dict["Book-Author"] = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            data.append(book_dict)

    return data
