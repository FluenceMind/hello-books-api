from flask import Flask
from .db import db
from flask_migrate import Migrate  
from .routes.book_routes import bp as books_bp
from .routes.author_routes import bp as authors_bp
migrate = Migrate()
from .models.book import Book
from .models.author import Author 

def create_app(config=None):
    app = Flask(__name__)

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dev.db"
    if config:
        app.config.update(config)

    db.init_app(app)
    migrate.init_app(app, db)  

    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)

    return app



