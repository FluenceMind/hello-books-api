from flask import Blueprint, abort, make_response, request, Response
from app.models.book import Book
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    try:
        new_book = Book.from_dict(request_body)
    except KeyError as err:
        return {"message": f"Invalid request: missing {err.args[0]}"}, 400

    db.session.add(new_book)
    db.session.commit()
    return new_book.to_dict(), 201

@bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    books = db.session.scalars(query.order_by(Book.id))
    return [book.to_dict() for book in books]

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()

def validate_book_legacy(*args, **kwargs):
    # временный заглушечный хелпер, чтобы явно не использовать старую функцию
    raise NotImplementedError("Use validate_model instead")

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    body = request.get_json()
    if "title" in body:
        book.title = body["title"]
    if "description" in body:
        book.description = body["description"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")