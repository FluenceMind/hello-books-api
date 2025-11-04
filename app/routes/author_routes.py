from flask import Blueprint, request, make_response, abort
from ..db import db
from ..models.author import Author
from ..models.book import Book
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("authors", __name__, url_prefix="/authors")


@bp.get("")
def get_authors():
    return get_models_with_filters(Author, request.args), 200


@bp.post("")
def create_author():
    data = request.get_json()
    return create_model(Author, data)


@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    data = request.get_json() or {}
    data["author_id"] = author.id
    return create_model(Book, data)


@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    return [b.to_dict() for b in author.books], 200