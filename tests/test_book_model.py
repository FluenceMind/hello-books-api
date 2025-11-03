from app.models.book import Book

def test_to_dict_basic():
    b = Book(title="T", description="D")
    b.id = 1  # задаём явно, без БД-коммита
    assert b.to_dict() == {"id": 1, "title": "T", "description": "D"}

def test_to_dict_without_id():
    b = Book(title="T", description="D")
    # id ещё не присвоен -> ожидаем None
    assert b.to_dict() == {"id": None, "title": "T", "description": "D"}