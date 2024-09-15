from typing import List, Optional

from pydantic import BaseModel


class ReviewBase(BaseModel):
    user_id: int
    review_text: str
    rating: int


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    book_id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    year_published: int
    summary: Optional[str] = None


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: int
    reviews: List[Review] = []

    class Config:
        orm_mode = True


# Response schemas
class ReviewResponse(BaseModel):
    id: int
    review_text: str
    rating: int


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str]
    year_published: Optional[int]
    summary: Optional[str]
    reviews: List[ReviewResponse] = []

    class Config:
        orm_mode = True  # This allows SQLAlchemy objects to be converted to Pydantic


class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    genre: Optional[str]
    year_published: Optional[int]
    summary: Optional[str]
