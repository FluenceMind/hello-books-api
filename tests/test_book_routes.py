def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr",
    }


def test_get_one_book_no_data_returns_404(client):
    # Act
    response = client.get("/books/1")
    # Assert
    assert response.status_code == 404


def test_get_all_books_with_fixture_returns_list(client, two_saved_books):
    # Act
    response = client.get("/books")
    body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert body == [
        {"id": 1, "title": "Ocean Book", "description": "watr 4evr"},
        {"id": 2, "title": "Mountain Book", "description": "i luv 2 climb rocks"},
    ]


def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!",
    })
    body = response.get_json()
    # Assert
    assert response.status_code == 201
    assert body == {
        "id": 1,
        "title": "New Book",
        "description": "The Best!",
    }