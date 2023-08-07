import sqlite3

# Connect to the database (or create it if it doesn't exist)
db = sqlite3.connect('ebookstore_db')

# Check if the books table exists
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
table_exists = cursor.fetchone()

# If the books table does not exist, create it
if table_exists is None:
    cursor.execute('''
        CREATE TABLE books (id INTEGER PRIMARY KEY, Title TEXT,
                            Author TEXT, Qty INTEGER)
    ''')
    db.commit()

    id1 = 3001 
    title1 = 'A Tale of Two Cities'
    author1 = 'Charles Dickens'
    qty1 = 30

    id2 = 3002 
    title2 = "Harry Potter and the Philosopher's Stone"
    author2 = 'J.K. Rowling'
    qty2 = 40

    id3 = 3003 
    title3 = 'The Lion, the Witch and the Wardrobe'
    author3 = 'C.S. Lewis'
    qty3 = 25

    id4 = 3004
    title4 = 'The Lord of the Rings'
    author4 = 'J.R.R Tolkien'
    qty4 = 37

    id5 = 3005 
    title5 = 'Alice in Wonderland'
    author5 = 'Lewis Carroll'
    qty5 = 12

    # Insert initial books into the table
    books_data = [(id1, title1, author1, qty1),
                  (id2, title2, author2, qty2),
                  (id3, title3, author3, qty3),
                  (id4, title4, author4, qty4),
                  (id5, title5, author5, qty5)]

    cursor.executemany('''INSERT INTO books(id, Title, Author, Qty)
                        VALUES(?,?,?,?)''', books_data)

    db.commit()

def get_integer_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

while True:
    menu = input('''Please select one of the following options:
1  - Enter book 
2  - Update book
3  - Delete book
4  - Search books
0  - Exit
''')

    if menu == "1":
        id = get_integer_input("Enter book ID: ")
        title = input("Enter book title: ")
        author = input("Enter book author: ")
        qty = get_integer_input("Enter book quantity: ")
        cursor.execute('''INSERT INTO books(id, Title, Author, Qty)
                          VALUES(?,?,?,?)''', (id, title, author, qty))
        db.commit()
        print("Book added successfully!")
        
    elif menu == "2":
        id = get_integer_input("Enter book ID to update: ")
        new_qty = get_integer_input("Enter new quantity: ")
        cursor.execute('''UPDATE books SET Qty = ? WHERE id = ?''', (new_qty, id))
        db.commit()
        print("Book updated successfully!")
        
    elif menu == "3":
        id = get_integer_input("Enter book ID to delete: ")
        cursor.execute('''DELETE FROM books WHERE id = ?''', (id,))
        db.commit()
        print("Book deleted successfully!")
        
    elif menu == "4":
        search_term = input("Enter book name or author: ")
        cursor.execute('''SELECT * FROM books WHERE Title LIKE ? OR Author LIKE ?''', ('%'+search_term+'%', '%'+search_term+'%'))
        results = cursor.fetchall()
        if len(results) == 0:
            print("No results found.")
        else:
            for row in results:
                print(row)
        
    elif menu == "0":
        print("Program Exited")
        break
        
    else:
        print("Invalid choice. Please try again.")

# Close the database connection
db.close()