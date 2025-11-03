import pytest
from werkzeug.exceptions import HTTPException
from app.models.book import Book
from app.routes.route_utilities import validate_model

def test_validate_model(two_saved_books):
    result = validate_model(Book, 1)
    assert result.id == 1
    assert result.title == "Ocean Book"
    assert result.description == "watr 4evr"

def test_validate_model_missing_record(two_saved_books):
    with pytest.raises(HTTPException):
        validate_model(Book, "3")

def test_validate_model_invalid_id(two_saved_books):
    with pytest.raises(HTTPException):
        validate_model(Book, "cat")