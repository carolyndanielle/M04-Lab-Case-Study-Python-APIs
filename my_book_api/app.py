from flask import Flask, request, jsonify
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.DEBUG)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publisher = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Book('{self.book_name}', '{self.author}', '{self.publisher}')"

@app.before_first_request
def create_tables():
    db.create_all()

#CRUD Operations

# Create a new book
@app.route('/book', methods=['POST'])
def add_book():
    logging.debug("Received request to add book")
    data = request.get_json()
    logging.debug(f"Request data: {data}")
    new_book = Book(book_name=data['book_name'], author=data['author'], publisher=data['publisher'])
    db.session.add(new_book)
    db.session.commit()
    logging.debug(f"Book created with ID: {new_book.id}")
    return jsonify({'id': new_book.id, 'message': 'New book created'}), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher} for book in books])

# Get a book by id
@app.route('/book/<int:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id) # get_or_404() will return 404 status code if the book is not found
    return jsonify({'book_name': book.book_name, 'author': book.author, 'publisher': book.publisher})

# Update a book by id
@app.route('/book/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    data = request.get_json()
    book.book_name = data['book_name']
    book.author = data['author']
    book.publisher = data['publisher']
    db.session.commit()
    return jsonify({'message': 'Book updated'}), 200

# Delete a book by id
@app.route('/book/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted'}), 200

if __name__ == '__main__':    app.run(debug=True)
