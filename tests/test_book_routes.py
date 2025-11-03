import pytest
from app.models.book import Book


def test_get_all_books_with_no_records(client):
    response = client.get("/books")
    body = response.get_json()
    assert response.status_code == 200
    assert body == []


def test_get_one_book(client, two_saved_books):
    response = client.get("/books/1")
    body = response.get_json()
    assert response.status_code == 200
    assert body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr",
    }


def test_get_one_book_no_data_returns_404(client):
    response = client.get("/books/1")
    assert response.status_code == 404


def test_get_all_books_with_fixture_returns_list(client, two_saved_books):
    response = client.get("/books")
    body = response.get_json()
    assert response.status_code == 200
    assert body == [
        {"id": 1, "title": "Ocean Book", "description": "watr 4evr"},
        {"id": 2, "title": "Mountain Book", "description": "i luv 2 climb rocks"},
    ]


def test_create_one_book(client):
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!",
    })
    body = response.get_json()
    assert response.status_code == 201
    assert body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!",
    }


def test_create_one_book_no_title(client):
    resp = client.post("/books", json={"description": "The Best!"})
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "Invalid request: missing title"}


def test_create_one_book_no_description(client):
    resp = client.post("/books", json={"title": "New Book"})
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "Invalid request: missing description"}


def test_create_one_book_with_extra_keys(client):
    resp = client.post("/books", json={
        "title": "New Book", "description": "The Best!", "extra": "ignored"
    })
    assert resp.status_code == 201
    assert resp.get_json() == {
        "id": 1, "title": "New Book", "description": "The Best!"
    }


def test_from_dict_ok():
    data = {"title": "New Book", "description": "The Best!"}
    b = Book.from_dict(data)
    assert isinstance(b, Book)
    assert b.title == "New Book"
    assert b.description == "The Best!"


def test_from_dict_missing_title():
    with pytest.raises(KeyError, match="title"):
        Book.from_dict({"description": "x"})


def test_from_dict_missing_description():
    with pytest.raises(KeyError, match="description"):
        Book.from_dict({"title": "x"})


def test_from_dict_ignores_extra_keys():
    data = {"title": "A", "description": "B", "extra": "C"}
    b = Book.from_dict(data)
    assert b.title == "A"
    assert b.description == "B"


# ✅ UPDATED TESTS FOR CAPITALIZATION

def test_get_one_book_missing_record(client, two_saved_books):
    resp = client.get("/books/3")
    assert resp.status_code == 404
    assert resp.get_json() == {"message": "Book 3 not found"}


def test_get_one_book_invalid_id(client, two_saved_books):
    resp = client.get("/books/cat")
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "Book cat invalid"}


def test_delete_book_missing_record(client, two_saved_books):
    resp = client.delete("/books/3")
    assert resp.status_code == 404
    assert resp.get_json() == {"message": "Book 3 not found"}


def test_delete_book_invalid_id(client, two_saved_books):
    resp = client.delete("/books/cat")
    assert resp.status_code == 400
    assert resp.get_json() == {"message": "Book cat invalid"}