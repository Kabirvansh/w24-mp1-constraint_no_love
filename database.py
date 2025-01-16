import sqlite3

database = "library.db"

sql_commands = """
   drop table if exists reviews;
drop table if exists penalties;
drop table if exists borrowings;
drop table if exists books;
drop table if exists members;




PRAGMA foreign_keys = ON;

CREATE TABLE members (
    email CHAR(100),
    passwd CHAR(100),
    name CHAR(255) NOT NULL,
    byear INTEGER,
    faculty CHAR(100),
    PRIMARY KEY (email)
);

CREATE TABLE books (
    book_id INTEGER,
    title CHAR(255),
    author CHAR(150),
    pyear INTEGER,
    PRIMARY KEY (book_id)
);

CREATE TABLE borrowings(
    bid INTEGER,
    member CHAR(100) NOT NULL,
    book_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    PRIMARY KEY (bid),
    FOREIGN KEY (member) REFERENCES members(email),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);


CREATE TABLE penalties(
    pid INTEGER,
    bid INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    paid_amount INTEGER,
    PRIMARY KEY (pid),
    FOREIGN KEY (bid) REFERENCES borrowings(bid)
);


CREATE TABLE reviews(
    rid INTEGER,
    book_id INTEGER NOT NULL,
    member CHAR(100) NOT NULL,
    rating INTEGER NOT NULL,
    rtext CHAR(255),
    rdate DATE,
    PRIMARY KEY (rid),
    FOREIGN KEY (member) REFERENCES members(email),
    FOREIGN KEY (book_id) REFERENCES books(book_id)
);

INSERT INTO members (email, passwd, name, byear, faculty) VALUES
('john.doe@example.com', 'password123', 'John Doe', 1990, 'Computer Science'),
('jane.smith@example.com', 'password456', 'Jane Smith', 1992, 'Mathematics'),
('mike.brown@example.com', 'password789', 'Mike Brown', 1989, 'Physics'),
('a', 'a', 'a', 1989, 'Physics');

INSERT INTO books (book_id, title, author, pyear) VALUES
(1, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925),
(2, 'To Kill a Mockingbird', 'Harper Lee', 1960),
(3, '1984', 'Teorge Orwell', 1949),
(4, 'To Kill a Mockingbirdi', 'Harper Lee', 1960),
(5, 'To Kill a Mockingbirda', 'Harper Lee', 1960),
(6, 'To Kill a Mockingbirdaa', 'Harper Lee', 1960),
(7, 'To Kill a Mockingbirdaaa', 'Harper Lee', 1960),
(8, 'Ah Chak', 'Tarper Lee', 1960),
(9, 'The Great Gatsby', 'F. Scott Fitzgerald', 1925),
(10, 'To Kill a Mockingbird', 'Harper Lee', 1960),
(11, '1984', 'Teorge Orwell', 1949),
(12, 'To Kill a Mockingbirdi', 'Harper Lee', 1960),
(13, 'To Kill a Mockingbirda', 'Harper Lee', 1960),
(14, 'To Kill a Mockingbirdaa', 'Harper Lee', 1960),
(15, 'To Kill a Mockingbirdaaa', 'Harper Lee', 1960),
(16, 'Ah Chak', 'Tarper Lee', 1960),
(17, 'Ball Chak', 'Sarper Lee', 1960),
(18, 'Baill Chak', 'Aarper Lee', 1960),
(19, 'Bailli Chak', 'Aarper See', 1960),
(20, 'Chak', 'Barper See', 1960),
(21, 'Dhak', 'Ballo See', 1960);


 
INSERT INTO borrowings (bid, member, book_id, start_date, end_date) VALUES
(1, 'john.doe@example.com', 1, '2024-01-01', '2024-01-15'),
(2, 'jane.smith@example.com', 2, '2024-02-01', '2024-02-15'),
(3, 'mike.brown@example.com', 3, '2024-03-01', NULL),
(4, 'a', 2, '2024-03-01', NULL);

INSERT INTO penalties (pid, bid, amount, paid_amount) VALUES
(1, 4, 500, NULL); 

INSERT INTO reviews (rid, book_id, member, rating, rtext, rdate) VALUES
(1, 1, 'john.doe@example.com', 5, 'A masterpiece of literature', '2024-01-20'),
(2, 2, 'jane.smith@example.com', 4, 'Very impactful and thought-provoking', '2024-02-20');

"""

conn = sqlite3.connect(database)

cursor = conn.cursor()

try:
    cursor.executescript(sql_commands)
    conn.commit()
    print("successful")
except sqlite3.Error as e:
    print(e)
finally:
    if conn:
        conn.close()
