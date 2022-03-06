# Import Flask modules
import time
from flask import Flask, jsonify, abort, request, make_response, g
from flaskext.mysql import MySQL
import pandas as pd

# Create an object named app 
app = Flask(__name__)

# Configure MySQL database
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'mhs'
app.config['MYSQL_DATABASE_PASSWORD'] = 'M123456S'
app.config['MYSQL_DATABASE_DB'] = 'bookstore'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql = MySQL()
mysql.init_app(app)
connection = mysql.connect()
connection.autocommit(True)
cursor = connection.cursor()


# Take the data from csv file to the database
def parseCSV(filePath):
    # CVS Column Names
    col_names = ['isbn', 'title', 'author_first_name', 'author_last_name', 'page_count', 'description']
    # Use Pandas to parse the CSV file
    csvData = pd.read_csv(filePath, names=col_names, header=None, encoding='ISO-8859-1', skiprows=[0])
    # Loop through the Rows
    for i, row in csvData.iterrows():
        sql = f"""
        INSERT INTO `books` (isbn, title, author_first_name, author_last_name, page_count, description) 
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        value = (row['isbn'], row['title'], row['author_first_name'], row['author_last_name'], row['page_count'], row['description'])
        cursor.execute(sql, value)


# Initializing bookstore database method
def init_bookstore():
    drop_table_books = 'DROP TABLE IF EXISTS books;'
    drop_table_logs = 'DROP TABLE IF EXISTS logs;'
    books_table = """
    CREATE TABLE books(
    id INT NOT NULL AUTO_INCREMENT,
    isbn VARCHAR(50) NOT NULL,
    title VARCHAR(100) NOT NULL,
    author_first_name VARCHAR(100),
    author_last_name VARCHAR(100),
    page_count INT NOT NULL,
    description VARCHAR(5000),
    PRIMARY KEY (id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    logs_table = """
    CREATE TABLE logs(
    id INT NOT NULL AUTO_INCREMENT,
    request_is VARCHAR(50) NOT NULL,
    time_taken VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    cursor.execute(drop_table_books)
    cursor.execute(drop_table_logs)
    cursor.execute(books_table)
    cursor.execute(logs_table)
    parseCSV('./MOCK_DATA.csv')


# Get the time of request
@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


# Logging taken time method
def log_request_time():
    t = str(g.request_time())
    log = f"""
    INSERT INTO `logs` (request_is, time_taken) VALUES ('get all books', {t});
    """
    cursor.execute(log)


# Get all books method
def get_all_books():
    query = """
    SELECT * FROM `books`;
    """
    cursor.execute(query)
    result = cursor.fetchall()
    books = [
        {'id': row[0], 'isbn': row[1], 'title': row[2], 'author_first_name': row[3], 'author_last_name': row[4],
         'page_count': row[5], 'description': row[6]} for row in result]

    log_request_time()
    return books


# Get a specific book method
def find_book(id):
    query = f"""
    SELECT * FROM `books` WHERE id={id};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    book = None
    if row is not None:
        book = {'id': row[0], 'isbn': row[1], 'title': row[2], 'author_first_name': row[3],
                'author_last_name': row[4], 'page_count': row[5], 'description': row[6]}
    return book


# Insert a new book method
def insert_book(isbn, title, auth_f_n, auth_l_n, pages, description=''):
    insert = f"""
    INSERT INTO `books` (isbn, title, author_first_name, author_last_name, page_count, description)
    VALUES('{isbn}', '{title}', '{auth_f_n}', '{auth_l_n}', '{pages}', '{description}');
    """
    cursor.execute(insert)

    query = f"""
    SELECT * FROM `books` WHERE id = {cursor.lastrowid};
    """
    cursor.execute(query)
    row = cursor.fetchone()

    return {'id': row[0], 'isbn': row[1], 'title': row[2], 'author_first_name': row[3], 'author_last_name': row[4],
            'page_count': row[5], 'description': row[6]}


# Update a book method
def change_book(book):
    update = f"""
    UPDATE books
    SET isbn = '{book['isbn']}', title = '{book['title']}', author_first_name ='{book['author_first_name']}',
    author_last_name ='{book['author_last_name']}', page_count ='{book['page_count']}', description ='{book['description']}'
    WHERE id = {book['id']};
    """
    cursor.execute(update)

    query = f"""
    SELECT * FROM `books` WHERE id = {book['id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return {'id': row[0], 'isbn': row[1], 'title': row[2], 'author_first_name': row[3], 'author_last_name': row[4],
            'page_count': row[5], 'description': row[6]}


# Remove a book method
def remove_book(book):
    delete = f"""
    DELETE FROM `books`
    WHERE id = {book['id']};
    """
    cursor.execute(delete)

    query = f"""
    SELECT * FROM `books` WHERE id = {book['id']};
    """
    cursor.execute(query)
    row = cursor.fetchone()
    return True if row is None else False


# Home endpoint
@app.route('/')
def home():
    return "Welcome to MH's Bookstore API Service"


# Retrieve all books endpoint
@app.route('/books', methods=['GET'])
def get_books():
    data = get_all_books()
    return jsonify({'books': data})


# Retrieve a specific book endpoint
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = find_book(id)
    if book is None:
        abort(404)
    return jsonify({'book found': book})


# Insert new book  endpoint
@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or 'title' not in request.json:
        abort(400)
    return jsonify({'newly added book': insert_book(request.json['isbn'], request.json['title'],
                                                    request.json['auth_f_n'], request.json['auth_l_n'],
                                                    request.json['page_count'], request.json['description'])}), 201


# Update a book endpoint
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = find_book(id)
    if book is None:
        abort(404)
    if not request.json:
        abort(400)
    book['isbn'] = request.json.get('isbn', book['isbn'])
    book['title'] = request.json.get('title', book['title'])
    book['author_first_name'] = request.json.get('author_first_name', book['author_first_name'])
    book['author_last_name'] = request.json.get('author_last_name', book['author_last_name'])
    book['page_count'] = request.json.get('page_count', book['page_count'])
    book['description'] = request.json.get('description', book['description'])

    action = change_book(book)

    return jsonify({'Updated book': action})


# Delete a book endpoint
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = find_book(id)
    if book is None:
        abort(404)
    action = remove_book(book)
    return jsonify({'result': action})


# Handle errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    init_bookstore()
    app.run(host='0.0.0.0', port=8000)
