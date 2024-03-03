import sqlite3
from faker import Faker
import random

# Connect to SQLite database or create if not exists
conn = sqlite3.connect('bookstore.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS authors (
                    author_id INTEGER PRIMARY KEY,
                    author_name TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS genres (
                    genre_id INTEGER PRIMARY KEY,
                    genre_name TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT,
                    author_id INTEGER,
                    genre_id INTEGER,
                    price REAL,
                    publication_year INTEGER,
                    FOREIGN KEY (author_id) REFERENCES authors(author_id),
                    FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY,
                    customer_name TEXT,
                    email TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                    order_id INTEGER PRIMARY KEY,
                    customer_id INTEGER,
                    order_date DATE,
                    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                    order_item_id INTEGER PRIMARY KEY,
                    order_id INTEGER,
                    book_id INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (order_id) REFERENCES orders(order_id),
                    FOREIGN KEY (book_id) REFERENCES books(book_id)
                )''')

# Instantiate Faker
fake = Faker()

# Function to generate authors
def generate_authors(num_authors):
    for _ in range(num_authors):
        author_name = fake.name()
        cursor.execute("INSERT INTO authors (author_name) VALUES (?)", 
                       (author_name,))
    conn.commit()

# Function to generate genres
def generate_genres(num_genres):
    genres = ["Fiction", "Non-fiction", "Science Fiction", "Mystery", "Thriller",
              "Romance", "Fantasy", "Horror"]
    for i in range(num_genres):
        genre_name = genres[i]
        cursor.execute("INSERT INTO genres (genre_name) VALUES (?)", (genre_name,))
    conn.commit()

# Function to generate books
def generate_books(num_books):
    for _ in range(num_books):
        title = fake.catch_phrase()
        author_id = random.randint(1, 100)  # Assuming 100 authors
        genre_id = random.randint(1, 8)     # Assuming 8 genres
        price = round(random.uniform(5, 50), 2)
        publication_year = random.randint(1900, 2023)
        cursor.execute("INSERT INTO books (title, author_id, \
                       genre_id, price, publication_year) VALUES (?, ?, ?, ?, ?)",
                       (title, author_id, genre_id, price, publication_year))
    conn.commit()

# Function to generate customers
def generate_customers(num_customers):
    for _ in range(num_customers):
        customer_name = fake.name()
        email = fake.email()
        cursor.execute("INSERT INTO customers (customer_name, email) VALUES (?, ?)",
                       (customer_name, email))
    conn.commit()

# Function to generate orders
def generate_orders(num_orders):
    for _ in range(num_orders):
        customer_id = random.randint(1, 100)  # Assuming 100 customers
        order_date = fake.date_between(start_date='-1y', end_date='today')
        cursor.execute("INSERT INTO orders (customer_id, order_date) VALUES (?, ?)", 
                       (customer_id, order_date))
    conn.commit()

# Function to generate order items
def generate_order_items(num_order_items):
    for _ in range(num_order_items):
        order_id = random.randint(1, 100)  # Assuming 100 orders
        book_id = random.randint(1, 1000)  # Assuming 1000 books
        quantity = random.randint(1, 5)
        cursor.execute("INSERT INTO order_items (order_id, book_id, quantity) \
                       VALUES (?, ?, ?)", (order_id, book_id, quantity))
    conn.commit()

# Generate data
generate_authors(100)
generate_genres(8)
generate_books(1000)
generate_customers(100)
generate_orders(500)
generate_order_items(1500)

# Close connection
conn.close()
