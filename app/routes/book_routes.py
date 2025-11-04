from flask import Blueprint, request, jsonify, make_response, Response
from ..db import db
from ..models.book import Book
from ..models.author import Author
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("books_bp", __name__, url_prefix="/books")


@bp.post("")
def create_book():
    data = request.get_json() or {}
    if "author_id" in data and data["author_id"] is not None:
        validate_model(Author, data["author_id"])
    return create_model(Book, data)


@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args), 200


@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict(), 200


def validate_book_legacy(*args, **kwargs):
    raise NotImplementedError("Use validate_model instead")


@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    body = request.get_json() or {}
    if "title" in body:
        book.title = body["title"]
    if "description" in body:
        book.description = body["description"]
    if "author_id" in body:
        if body["author_id"] is None:
            book.author_id = None
        else:
            author = validate_model(Author, body["author_id"])
            book.author_id = author.id
    db.session.commit()
    return book.to_dict(), 200


@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")