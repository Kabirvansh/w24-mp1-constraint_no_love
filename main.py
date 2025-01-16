import sqlite3
import sys
import os
from datetime import datetime, timedelta, date
import time
import getpass

# ----------------------- HEADINGS ----------------------- #
WELCOME = r'''
__        __   _                          _ 
\ \      / /__| | ___ ___  _ __ ___   ___| |
 \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ |
  \ V  V /  __/ | (_| (_) | | | | | |  __/_|
   \_/\_/ \___|_|\___\___/|_| |_| |_|\___(_)
'''
LOGIN = r'''
 _                _
| |    ___   __ _(_)_ __
| |   / _ \ / _` | | '_ \
| |__| (_) | (_| | | | | |
|_____\___/ \__, |_|_| |_|
            |___/
'''
MENU = r'''
 __  __
|  \/  | ___ _ __  _   _ 
| |\/| |/ _ \ '_ \| | | |
| |  | |  __/ | | | |_| |
|_|  |_|\___|_| |_|\__,_|
'''
RETURN = r'''
 ____      _
|  _ \ ___| |_ _   _ _ __ _ __
| |_) / _ \ __| | | | '__| '_ \
|  _ <  __/ |_| |_| | |  | | | |
|_| \_\___|\__|\__,_|_|  |_| |_|
'''
SEARCH = r'''
 ____                      _     
/ ___|  ___  __ _ _ __ ___| |__  
\___ \ / _ \/ _` | '__/ __| '_ \ 
 ___) |  __/ (_| | | | (__| | | |
|____/ \___|\__,_|_|  \___|_| |_|
'''

PENALTIES = r'''
 ____                  _ _   _
|  _ \ ___ _ __   __ _| | |_(_) ___  ___
| |_) / _ \ '_ \ / _` | | __| |/ _ \/ __|
|  __/  __/ | | | (_| | | |_| |  __/\__ \
|_|   \___|_| |_|\__,_|_|\__|_|\___||___/
'''
PROFILE = r'''
 ____             __ _ _      
|  _ \ _ __ ___  / _(_) | ___ 
| |_) | '__/ _ \| |_| | |/ _ \
|  __/| | | (_) |  _| | |  __/
|_|   |_|  \___/|_| |_|_|\___|
'''
REGISTER = r'''
 ____            _     _
|  _ \ ___  __ _(_)___| |_ ___ _ __ 
| |_) / _ \/ _` | / __| __/ _ \ '__|
|  _ <  __/ (_| | \__ \ ||  __/ |   
|_| \_\___|\__, |_|___/\__\___|_|   
           |___/
'''
GOODBYE = r'''
  ____                 _ _                _ 
 / ___| ___   ___   __| | |__  _   _  ___| |
| |  _ / _ \ / _ \ / _` | '_ \| | | |/ _ \ |
| |_| | (_) | (_) | (_| | |_) | |_| |  __/_|
 \____|\___/ \___/ \__,_|_.__/ \__, |\___(_)
                               |___/        
'''
# ----------------------- ######## ----------------------- #


# ------------------------ COLORS ------------------------ #
RED = '\033[91m'; HRED = '\033[41m'; GREEN = '\033[92m'; YELLOW = '\033[93m'
BLUE = '\033[94m'; PURPLE = '\033[95m'; CYAN = '\033[96m'; RESET = '\033[0m'
# ------------------------ ###### ------------------------ #


# ----------------------- PRINTERS ----------------------- #
def print_pa(attr:str, val):
    """
    Function to print the attributes of the member.
    attr: the attribute
    vale: value of that attribute
    """
    print(f"{colored(attr, CYAN):>30}", val)

def colored(string, t_col='', h_col = ''):
    '''
    Function to color the string
    string: the string to be colored
    t_col: colored to be applied, default = '' or nothing
    h_col: background color for the text, default = '' or nothing
    '''
    return t_col+h_col+string+RESET

def print_er(query:str, t):
    '''
    Function to print the error with color and to make it dissapear after the specified time
    query: the error text
    t: time in seconds
    '''
    print("\033[?25l", end='')
    print(bold(query.upper(), RED))
    time.sleep(t)
    print('\033[?25h',end='')
    print("\033[A\033[K")

def bold(string:str, color=None):
    '''
    Function to print the text in bold format and with an optional color
    string: the text
    color: the color to be applied, if any
    '''
    if color != None:
        return color+f"\033[1m{string}"+RESET
    return f"\033[1m{string}"+RESET

def print_table(headings:tuple, spacings:tuple, heading=False, highlight='', color='', overdue =False):
    '''
    Function to print various tables in library inventory management system
    heading: the tuple of all the column values of a row
    spacings: tuple for the widths of the colums of a row
    heading: bool; specifiy if its the heading of the table
    highlight: background color of the row
    color: text color of the row
    overdue: bool; specific functionality for overdue books in return menu table
    '''
    if heading:
        border = "+" + "+".join(["-" * (spacing) for spacing in spacings]) + "+"
        header = "|" + "|".join([f"{headings[i]:^{spacings[i]}}" for i in range(len(headings))]) + "|"
        print(border)
        print(header)
        print(border)
    else:
        header = "|" +"|".join([f"{headings[i]:^{spacings[i]}}" for i in range(len(headings))]) + '|'
        if overdue == True:
            header += "       OVERDUE"
        print(colored(header, color, highlight))

def p_heading(string):
    '''
    Function to print the ascii heading
    '''
    print("\033[33m"+string+"\033[0m")

def exit_animation():
    '''
    An ascii animation that shows up on exit
    '''
    print("\033[?25l", end='')
    for i in [RED,GREEN,BLUE,YELLOW,PURPLE,CYAN,YELLOW,RED]:
        print(colored(GOODBYE, i)); time.sleep(0.15); clear()
    print("\033[?25h", end='')
# ----------------------- ######## ----------------------- #
    




# ----------------------- VALIDATIONS ----------------------- #
def email_check(email:str):
    '''
    Function to verify if the email entered is in the correct format
    '''
    if email.count('@') != 1:
        return True
    
    first_part, second_part = email.split('@')

    if (not first_part or not second_part):
        return True

    if '.' not in second_part:
        return True
    
    second_parts = second_part.split('.')
    if any(not part for part in second_parts):
        return True

    return False


def already_exist_email(email:str, conn:sqlite3.Connection):
    '''
    Checks if the email already exists in the database
    '''
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM members WHERE email LIKE ?", (email,))
    exists = cursor.fetchone()[0]
    return exists


def byear_check(byear):
    '''
    Checks if the birth year is reasonable (in this case, not in the same year as now)
    '''
    try:
        byear_int = int(byear)
        if byear_int <= datetime.now().year:
            return False
        else:
            return True
    except ValueError:
        return True
    


def password_check(password):
    '''
    Checks if the password is in the correct format
    '''
    if len(password) < 8:
        return True

    has_uppercase = True
    has_lowercase = True
    has_digit = True
    has_special = True

    special_characters = set("!@#$%^&*()-_+=[]{};:'\"\\|,.<>/?")

    for char in password:
        if char.isupper():
            has_uppercase = False
        elif char.islower():
            has_lowercase = False
        elif char.isdigit():
            has_digit = False
        elif char in special_characters:
            has_special = False

        if (not has_uppercase and not has_lowercase and not has_digit and not has_special):
            return False

    return True

# ----------------------- ######## ----------------------- #

def get_faculty_names(conn:sqlite3.Connection):
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT faculty FROM members")
    faculties = cursor.fetchall()
    faculty_names = ', '.join([faculty[0] for faculty in faculties])
    return faculty_names

def move_cursor(line, column):
    """
    Moves the cursor to the specified position in the terminal. It takes the line and 
    the column as input/parameter.
    """
    print(f'\033[{line};{column}H\033[K', end='') # Move the cursor to the specified position

def create_connection(db_file):
    '''
    creates a connection to the database
    '''
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn

def clear():
    '''
    clears the screen
    '''
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')


def start_menu(conn:sqlite3.Connection):
    """
    Display the start menu for the Library Management System.
    This function presents the user with options to either login, register,
    or exit the system.
    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    Returns: None
    Actions:
    - Calls the login() function if the user chooses to login.
    - Calls the sign_up() function if the user chooses to register.
    - Closes the database connection and exits the system if the user chooses to exit.
    """
    loop = True
    while loop:
        clear()
        p_heading(WELCOME)
        print(f"Welcome to our Library Management System, a comprehensive\nplatform designed just for beautiful people like you. ;)")
        print(bold(f'{"1. Login      2. Register     3. Exit":^57}', CYAN)); 
        print()

        user_input = input("Select an option: ")
        if user_input == "1":
            clear()
            loop = login(conn)
        elif user_input == "2":
            clear()
            loop = sign_up(conn)
        elif user_input == "3":
            loop = False
        else:
            move_cursor(12,0)
            print_er("Invalid option, please try again.", 1)
    clear()
    exit_animation()
    conn.close()
    sys.exit()




def search(conn,email,key="n_borrow"):
    """
    Search for books or borrow a book based on the given key.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the member.
    - key (str): Key indicating the action to perform. Defaults to "n_borrow".

    Returns:
    - bool: True if the user chooses to go back, False if they choose to exit.
    """
    if(key=="n_borrow"):
        loop = True
        while(loop):
            clear()
            p_heading(SEARCH)
            commands = r"""Use one of the following commands
        --------------------------------
            1. Press S to Search a book
            2. Press B to Borrow a book
            3. Press < to Go Back
        """

            print("\n"+commands)
            res = input("Response: ")

            if(res.lower() == "s"):
                search = input("Enter a book to search: ")
                loop = search_books(conn,search,email)
            elif(res.lower()== "b"):
                borrow = input("Enter a book id to borrow: ")
                loop = borrow_book(conn,borrow, email)
            elif(res.lower() =="<"):
                break
            else:
                print_er("Invalid Input", 1)
    else:
        loop = True
        while(loop):
            borrow = input("Enter a book id to borrow: ")
            loop=borrow_book(conn,borrow, email)
            if(loop == False):
                return False
        

    return True



def search_books(conn, keyword, email,page=1):
    """
    Searches for books based on a given keyword, displaying results in paginated format.

    Parameters:
        conn (sqlite3.Connection): The SQLite database connection.
        keyword (str): The keyword to search for in book titles or authors.
        email (str): The email address of the user performing the search.
        page (int, optional): The page number of the search results. Defaults to 1.

    Returns:
        bool: False if the user chooses to quit or go back to the main menu, otherwise True.
    """
    cursor = conn.cursor()
    offset = (page - 1) * 5 


    query = '''
        select * from
            (select  bk.book_id, title,author,pyear,
                    IFNULL((select AVG(rating) from reviews rv where rv.book_id == bk.book_id), 0),
                    IFNULL((select 'Borrowed' from borrowings br where br.book_id == bk.book_id and end_date is NULL), 'Available')
            from books bk
            WHERE title like ?
            ORDER by title ASC)
            UNION
            select * from
            (select  bk.book_id, title, author, pyear,
            IFNULL((select AVG(rating) from reviews rv where rv.book_id == bk.book_id), 0),
                    IFNULL((select 'Borrowed' from borrowings br where br.book_id == bk.book_id and end_date is NULL), 'Available')
            from books bk
            WHERE author like ?
            ORDER by author ASC)
        limit 5 offset ?;'''



    cursor.execute(query, (f'%{keyword}%', f'%{keyword}%', offset))
    books = cursor.fetchall()

    if len(books)==0:
        print_er("No Books Found! Try Again", 1)
        search(conn,email)
    
    else:
        headings = ('Book ID', 'Title', 'Author', 'Year', 'Avg. Rating', 'Availability')
        spacings = (10, 30, 20, 6, 11, 12)
        print_table(headings, spacings, heading=True)

        for book in books:
            print_table(book, spacings)
        
        if len(books) == 5:
            commands = r"""Use one of the following commands
--------------------------------
    1. Press M to Show More Results
    2. Press S to Search Again
    3. Press B to Borrow
    4. Press < to go to Main Menu
"""
            print("\n"+commands)

            loop = True
            while(loop):
                    more = input("Response: ")
                    if more.lower() == 'm':
                        loop = search_books(conn, keyword,email, page + 1)
                    elif more.lower() == "s":
                        loop = search(conn,email)
                    elif more.lower() == "<":
                        break
                    elif(more.lower() == "b"):
                        loop = search(conn,email,"borrow")
                    else:
                        print_er("Invalid Input", 1)
            return False
            
        if len(books) <= 5:
            commands = r"""Use one of the following commands
--------------------------------
    1. Press S to Search Again
    2. Press B to Borrow
    3. Press < to go to Main Menu
"""
            print("\n"+commands)

            more = input("Response: ")
            if more.lower() == "s":
                search(conn,email)
            elif(more.lower() == "b"):
                search(conn,email,"bhoro")
            elif more.lower() == "<":
                return False
            else:
                print_er("Invalid Input", 1)


def borrow_book(conn, book_id, member_email):
    """
    Borrow a book for a member.

    Parameters:
        conn (sqlite3.Connection): The SQLite database connection.
        book_id (str): The ID of the book to be borrowed.
        member_email (str): The email address of the member borrowing the book.

    Returns:
        bool: False if the book is successfully borrowed, otherwise True.
    """
    cursor = conn.cursor()
    query1 = "SELECT COUNT(*) FROM borrowings WHERE book_id = ? AND end_date IS NULL"

    cursor.execute(query1, (book_id,))

    query2 = "Select COUNT(*) from books where book_id = ?"


    if cursor.fetchone()[0] > 0:
        print_er("Sorry, this book is currently not available",1)
        return True
    
    cursor.execute(query2, (book_id,))

    if cursor.fetchone()[0]==0:
        print_er("Sorry, the book don't exist",1)
        return True

    
    query2 = "INSERT INTO borrowings (member, book_id, start_date) VALUES (?, ?, ?)"
    cursor.execute(query2, (member_email, book_id, date.today()))
    conn.commit()
    print("Book borrowed successfully.")
    time.sleep(1)
    return False




def user_menu(conn:sqlite3.Connection, email:str):
    """
    Display the user menu for the Library Management System.

    This function presents the logged-in user with various options such as viewing
    their profile, searching for a book, returning a book, paying penalties, and
    logging out.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the logged-in user.

    Returns:
    - bool: False if the user chooses to exit, otherwise True.
    """
    logout = False
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE email=?", [email])
    user = cursor.fetchone()
    while not logout:
        clear()
        p_heading(MENU)
        text = bold(user[2], CYAN)
        print("Hello", text)
        print("Choose one of the options below to proceed:\n\tI: View your Profile\n\tS: Search a Book\n\tR: Return a Book\n\tP: Pay a Penalty\n\tL: Logout\n\tQ: Quit")
        prompt = input("--> ").lower()
        if prompt == "i":
            action = member_profile(conn,email)
            if action == False:
                return False
        elif prompt == "s":
            action = search(conn,email)
            if action == False:
                return False
            
        elif prompt == "r":
            action = return_menu(conn,email)
            if action == False:
                return False
        elif prompt == "p":
            action = pay_penalties(conn, email)
            if action == False:
                return False
        elif prompt == "l":
            logout = True
        elif prompt == "q":
            return False
        else:
            print_er("Please enter a valid input", 1)
    return logout
# john.doe@example.com
# password123






def member_profile(conn:sqlite3.Connection, email:str):
    """
    Display the profile of the logged-in member.

    This function retrieves and displays various information about the logged-in member,
    including their name, email, birth year, previous borrowings, current borrowings, overdue
    borrowings, unpaid penalties, and unpaid amount.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the logged-in member.

    Returns:
    - bool: True if the user chooses to go back, False if they choose to exit.
    """
    clear()
    p_heading(PROFILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE email=?;", [email])
    user = cursor.fetchone()
    name = user[2]
    Email = user[0]
    birth_year = user[3]
    print_pa(f"Name:",name)
    print_pa(f"Email:",Email)
    print_pa(f"Birth Year:",birth_year)

    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member=? and end_date IS NOT NULL;", (email,))
    previous_borrowings = cursor.fetchone()
    print_pa(f"Previous Borrowings:",previous_borrowings[0])

    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member=? and end_date IS NULL;", (email,))
    current_borrowings = cursor.fetchone()
    print_pa(f"Current Borrowings:",current_borrowings[0])

    now = datetime.now()
    now = now.strftime("%Y-%m-%d")
    cursor.execute("SELECT COUNT(*) FROM borrowings WHERE member=? and end_date IS NULL and (julianday(?) - julianday(start_date)) > 20 ;", (email,now,))
    overdue_borrowings = cursor.fetchone()
    print_pa(f"Overdue Borrowings:",overdue_borrowings[0])

    cursor.execute("SELECT COUNT(*) FROM penalties p JOIN borrowings b ON p.bid = b.bid WHERE member=? and p.amount - p.paid_amount > 0 ;", (email,))
    c_unpaid_penalty = cursor.fetchone()
    print_pa(f"Unpaid Penalties:",c_unpaid_penalty[0])

    cursor.execute("SELECT SUM(p.amount - p.paid_amount) FROM penalties p JOIN borrowings b ON p.bid = b.bid WHERE member=?;", (email,))
    unpaid_penalty = cursor.fetchone()[0]
    if unpaid_penalty == None: unpaid_penalty = 0
    print_pa(f"Unpaid Amount:",f'$ {unpaid_penalty:,}')
    time.sleep(1.5)
    print('\nEnter "<" to go back to previous screen or "Q" to exit.\n--> ')
    while True:
        move_cursor(18,5)
        command = input()
        if command == "<":
            return True
        elif command == 'q':
            return False
        move_cursor(16,0)
        print_er("Please enter a valid input.", 1)



def login(conn:sqlite3.Connection):
    """
    Authenticate users by asking for their email and password.

    This function prompts the user to enter their email and password for login.
    If the credentials are correct, it calls the user_menu function to display
    the user menu.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.

    Returns:
    - bool: True if the user chooses to go back, False otherwise.
    """
    user_exist = None
    p_heading(LOGIN)  
    print(f'PLEASE ENTER THE DETAILS BELOW TO LOGIN {colored("(Q: quit, <: Go back anywhere)", PURPLE)}\n')
    print(bold(f'{"Enter your email: ":>21}'))
    print(bold(f'{"Enter your password: ":>21}'))
    while user_exist == None:
        move_cursor(11,22)
        email = input(BLUE)
        print(RESET)
        if email == "<": return True
        elif email in ['q','Q']: clear(); conn.close();sys.exit("Goodbye!")

        password = getpass.getpass(prompt="\033[12;22H")
        if password == "<": return True
        elif password in ['q','Q']: clear();conn.close(); sys.exit("Goodbye!")

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members WHERE email LIKE ? AND passwd=?",(email, password,))
            user_exist = cursor.fetchone()
        except sqlite3.Error as err:
            print(err)
        if not user_exist:
            move_cursor(10,0)
            print_er("Invalid email or password.", 1)

    if user_exist:
        global NEW_PENALTIES
        NEW_PENALTIES = penalty_adjuster(conn, email)
        return user_menu(conn, user_exist[0])


def sign_up(conn:sqlite3.Connection):
    """
    Allow users to sign up for the system by providing necessary details.

    This function prompts the user to provide their email, password, name, birth year,
    and faculty to sign up for the system.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.

    Returns:
    - bool: True if the user chooses to go back or after they successfully sign up, False otherwise.
    """
    cursor = conn.cursor()
    loop = True
    p_heading(REGISTER)
    print(f"ENTER THE DETAILS BELOW TO SIGN UP {colored('(Q: quit, <: Go Back)', PURPLE)}\n")
    print(bold('Login Details'.upper(), CYAN))
    print(bold(f"{'Email:':>15}\n{'Password:':>15}"))
    
    loop = True
    while(loop==True):
        email = input(f"{YELLOW}\033[12;17H\033[K"); print(RESET, end ="")
        if email == '<': return True                # GO BACK
        elif email in ['q', 'Q']: return False      # EXIT

        loop = email_check(email)
        validation = already_exist_email(email, conn)
        if(loop == True):
            print_er("\033[10;0HInvalid Format", 1)
        if validation >= 1:
                print_er("\033[10;0HUser already exits, Please login", 1.5)
                return True

    password_requirements = r"""Password Strength Requirements:
--------------------------------
    1. Length: At least 8 characters
    2. Upper Case: Must contain at least one upper case letter (A-Z)
    3. Lower Case: Must contain at least one lower case letter (a-z)
    4. Numbers: Must contain at least one digit (0-9)
    5. Must include at least one of the following special characters: ! @ # $ % ^ & * ( ) - _ + = [ ] { } | \ ; : ' " , < . > / ? 
"""
    move_cursor(15,0)
    print(colored(password_requirements, RED))



    loop = True
    while(loop):
        password = getpass.getpass(prompt="\033[12;22H")
        # password = getpass.getpass(prompt="")
        print(RESET, end ="")
        if password == '<': return True                # GO BACK
        elif password in ['q', 'Q']: return False      # EXIT

        loop = password_check(password)
        if(loop):
            print_er("\033[10;0HPassword is Weak", 1)
    
    for i in range(9):
        print("\033[?25l\033[K")
    move_cursor(15, 0); print("\033[?25h", end="")

    print(bold('Personal Details'.upper(), CYAN))
    print(bold(f"{'Name:':>15}\n{'Birth Year:':>15}\n{'Faculty:':>15}\n"))

    name = ""
    while(not name):
        name = input(f"{YELLOW}\033[16;17H\033[K"); print(RESET, end ="")
        if name == '<': return True                # GO BACK
        elif name in ['q', 'Q']: return False      # EXIT

        if(not name):
            print_er("\033[14;0HInvalid Name", 1)

    loop = True
    while(loop==True):
        byear = input(f"{YELLOW}\033[17;17H\033[K"); print(RESET, end ="")
        if byear == '<': return True                # GO BACK
        elif byear in ['q', 'Q']: return False      # EXIT

        loop = byear_check(byear)
        if(loop == True):
            print_er("\033[14;0HInvalid Year", 1)
    
    text = "Enter your faculty name (Eg. "+ get_faculty_names(conn)+")"  
    faculty = ""
    while(not faculty):
        faculty = input(f"{YELLOW}\033[18;17H\033[K"); print(RESET, end ="")
        if faculty == '<': return True                # GO BACK
        elif faculty in ['q', 'Q']: return False      # EXIT

        if faculty == '':
            print_er(f"\033[14;0HInvalid Faculty; {text}", 1.5)
    
    try:
        cursor.execute('''
            INSERT INTO members(email, passwd, name, byear, faculty) VALUES (?, ?, ?, ?, ?)
        ''', (email, password, name, byear, faculty))
        conn.commit()
        print("\033[?25l", end="")
        print(bold("You've signed up successfully!".upper(), GREEN))
        

    except sqlite3.Error as e:
        print(e)

    time.sleep(2)
    print("\033[?25h", end="")
    return True



def penalty_adjuster(conn: sqlite3.Connection, email: str):
    """
    Adjust penalties for overdue books and update the database accordingly.

    This function calculates penalties for each overdue book borrowed by the
    member, updates the penalty amount in the database, and returns a list of
    books with updated penalties.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the member.

    Returns:
    - list: List of tuples containing book details with updated penalties.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT b.bid, bk.title, b.start_date FROM borrowings b, books bk WHERE b.member =? AND b.book_id = bk.book_id AND b.end_date IS NULL;", (email,))
    books = cursor.fetchall()
    new_penalties = []
    for i in range(len(books)):
        time_kept = datetime.strptime(str(date.today()), "%Y-%m-%d") - (datetime.strptime(books[i][2], "%Y-%m-%d") + timedelta(days=20))
        time_kept = int(str(time_kept).split()[0])
        if time_kept >= 1:            
            cursor.execute("SELECT COUNT(*) FROM penalties WHERE bid = ?", (books[i][0],))
            penalty = cursor.fetchone()
            if penalty[0] == 0:
                cursor.execute("INSERT INTO penalties (bid, amount, paid_amount) VALUES (?, ?, 0)", (books[i][0], time_kept))
                conn.commit()
            elif penalty[0] == 1:
                cursor.execute("UPDATE penalties SET amount = ? WHERE bid = ?", (time_kept, books[i][0]))
                conn.commit()
            new_penalties.append(books[i])
    return new_penalties

def return_menu(conn: sqlite3.Connection, email: str):
    """
    Display the return menu for the member to return borrowed books.

    This function allows the member to return borrowed books, review the books if desired,
    and updates the database accordingly.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the member.

    Returns:
    - bool: True if the user chooses to go back, False if they choose to exit.
    """
    while True:    
        clear()
        p_heading(RETURN)
        cursor = conn.cursor()
        cursor.execute("SELECT b.bid, bk.title, b.start_date FROM borrowings b, books bk WHERE b.member =? AND b.book_id = bk.book_id AND b.end_date IS NULL;", (email,))
        books = cursor.fetchall()
        if len(books) == 0:
            print('\033[?25l')
            print(bold("\nthere are no books to be returned. you are all set!".upper(), GREEN)); time.sleep(1.5)
            print('\033[?25h')
            break
        
        spacings = (4,4,50,10,10)
        headings = ('SNO','BID','TITLE','START DATE','END DATE')
        print_table(headings, spacings, True)
        for i in range(len(books)):
            end_date= str(datetime.strftime((datetime.strptime(books[i][-1], "%Y-%m-%d") + timedelta(days=20)), "%Y-%m-%d"))
            data = (i+1,books[i][0],books[i][1],books[i][2],end_date)
            if books[i] in NEW_PENALTIES:
                print_table(data,spacings,False,HRED,YELLOW,True)
            else:
                print_table(data,spacings)
        border = "+" + "+".join(["-" * (spacing) for spacing in spacings]) + "+"
        print(border)

        possible_inputs = [str(i+1) for i in range(len(books))] + ['q','<']
        print()
        print(f"Enter the serial number (SNO) of the borrowing you want to return {colored('(Q: quit, <: Go back)', PURPLE)}:")
        
        input_loc = 13+len(books)
        move_cursor(input_loc, 90)
        returning = input().strip().lower()
        while returning not in possible_inputs:
            move_cursor(input_loc-1, 0)
            print_er("Please enter a valid input", 1)
            move_cursor(input_loc,90)
            returning = input().strip().lower()
        if returning not in ['q', '<']:
            returning_bid = books[int(returning)-1][0]
            cursor.execute("UPDATE borrowings SET end_date = ? WHERE bid = ?", (str(date.today()), returning_bid))
            conn.commit()
            
            move_cursor(input_loc, 0)
            review_option = input("Would you like to review the book? (Y/N): ").lower()
            while review_option not in ['y','n']:
                move_cursor(input_loc-1, 0); print_er("Please enter a valid input",1)
                move_cursor(input_loc, 0)
                review_option = input("Would you like to review the book? (Y/N): ").lower()
            
            clear()
            p_heading(RETURN)
            if review_option == 'y':
                review_rating = 0
                print(colored(f"Now reviewing {bold(books[int(returning)-1][1], CYAN)}", YELLOW))
                print("Enter a number rating from 1 to 5 (inclusive): ")
                print("Enter your comment: ")
                while review_rating not in range(1,6): 
                    try: 
                        move_cursor(9, 48)
                        review_rating = int(input())
                        assert review_rating in range(3,6)
                    except:
                        move_cursor(7,0); print_er("Please enter a valid input", 1)
                move_cursor(10,21)
                review_text = input().strip()
                if review_text == "": review_text = None
            
                cursor.execute("SELECT book_id FROM borrowings WHERE bid = ?", (returning_bid,))
                book_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO reviews (book_id,member,rating,rtext,rdate) VALUES (?,?,?,?,?)", (book_id,email,review_rating,review_text,str(date.today())))
                conn.commit()
                move_cursor(10,0); move_cursor(9,0); move_cursor(8,0); 
            print('\033[?25l', end='')
            print(bold("\nbook has been returned and the record has been updated".upper(), GREEN)); time.sleep(1.5)
            if len(books)-1 > 0:
                print("\nWould you like to return another book? (Y/N)\n-->"); print('\033[4A\033[K\033[12;5H\033[?25h', end="")
                again = input()
                while again not in ['y','n']: 
                    print('\033[A\033[A\033[K'); print_er('Please enter a valid input', 1.5)
                    again = input("\nWould you like to return another book? (Y/N)\n-->").lower()
                if again == 'n':
                    break
            else:
                break
    
        elif returning == "q":
            return False
        elif returning == '<':
            return True       

def pay_penalties(conn: sqlite3.Connection, email: str):
    """
    Allow the member to pay penalties for overdue books.

    This function displays the penalties associated with overdue books for the member
    to pay. It updates the payment status in the database accordingly.

    Parameters:
    - conn (sqlite3.Connection): SQLite database connection.
    - email (str): Email address of the member.

    Returns:
    - bool: True if the user chooses to go back, False if they choose to exit.
    """
    while True:
        clear()
        p_heading(PENALTIES)
        cursor = conn.cursor()
        cursor.execute("""SELECT p.pid, bk.title, p.amount, ifnull(p.paid_amount,0) FROM penalties p, 
                       books bk JOIN borrowings b ON p.bid = b.bid WHERE member=? AND p.amount - ifnull(p.paid_amount,0) > 0 
                       AND bk.book_id = b.book_id;""", (email,))
        penalties = cursor.fetchall()
        if len(penalties) == 0:
            print('\033[?25l')
            print(bold("\nthere are no penalties to be paid. you are all set!".upper(), GREEN)); time.sleep(1.5)
            print('\033[?25h')
            break
        
        spacings = (4,4,50,12,12)
        headings = ('SNO','PID','TITLE','AMOUNT','PAID AMOUNT')

        print_table(headings, spacings, True)
        for i in range(len(penalties)):
            data = (i+1,penalties[i][0],penalties[i][1],penalties[i][2],penalties[i][3])
            print_table(data,spacings)
        border = "+" + "+".join(["-" * (spacing) for spacing in spacings]) + "+"
        print(border)

        possible_inputs = [str(i+1) for i in range(len(penalties))] + ['q','<']
        print()
        print(f"Enter the serial number (SNO) of the penalty you want to pay {colored('(Q: quit, <: Go back)', PURPLE)}:")
        input_loc = 13+len(penalties)
        move_cursor(input_loc, 85)
        paying = input().strip().lower()
        while paying not in possible_inputs:
            move_cursor(input_loc-1, 0)
            print_er("Please enter a valid input", 1)
            move_cursor(input_loc,85)
            paying = input().strip().lower()
        if paying not in ['q', '<']:
            paying_pid = penalties[int(paying)-1][0]
            choice = input("Would you like to pay it in full? (Y/N)\n--> ").strip().lower()
            while choice not in ['y','n']:
                move_cursor(input_loc-1, 0)
                print_er("Invalid input", 1)
                move_cursor(input_loc+2,5)
                choice = input().strip().lower()
            if choice == 'y':
                amount = penalties[int(paying)-1][2]-penalties[int(paying)-1][3]
            else:
                print('\033[A\033[K\033[A\033[K', end='')
                amount = input("Amount: $ ").strip().replace(",", "")
                while amount.isnumeric() == False and '-' not in amount:
                    move_cursor(input_loc-1, 0)
                    print_er("Please enter an integer amount", 1)
                    move_cursor(input_loc+1,11)
                    amount = input().strip().replace(',', '')
                amount = int(amount)
            clear()
            if amount > 0:
                payment = 0; returned_amount = 0
                if amount > penalties[int(paying)-1][2]-penalties[int(paying)-1][3]:
                    payment = penalties[int(paying)-1][2]-penalties[int(paying)-1][3]
                    returned_amount =  amount - payment
                else: 
                    payment = amount
                cursor.execute("UPDATE penalties SET paid_amount = ? WHERE pid = ?", (penalties[int(paying)-1][3]+payment, paying_pid))
                conn.commit()
                p_heading(PENALTIES)
                print(f"\n\033[?25l{bold(f'A penalty of'.upper())} {colored(f'$ {payment:,}',YELLOW)} {bold(f'has been paid for PID:'.upper())} {colored(str(paying_pid),YELLOW)}")
                if returned_amount > 0:
                    print(bold(f'You have been returned'), colored(f'$ {returned_amount:,}', GREEN))
                time.sleep(1); input("Press Enter to continue..."); print("\033[?25h", end='')
            elif amount == 0:
                p_heading(PENALTIES)
                print(f"\n\033[?25l{bold(f'Nothing has been changed'.upper(), CYAN)}"); time.sleep(1); print("\033[?25h", end='')
            
            if amount < penalties[int(paying)-1][2]-penalties[int(paying)-1][3] or len(penalties)-1 > 0:
                clear()
                p_heading(PENALTIES)
                print("\nWould you like to do another payment? (Y/N)")
                another = input("--> ").strip().lower()
                while another not in ['y','n']:
                    print("\033[3A\033[2K", end='')
                    print_er('ivalid input', 1); print('\033[B\033[5C', end='')
                    another = input("").strip().lower()
                if another == 'n':
                    break
            else:
                break

        elif paying == 'q':
            return False
        elif paying == '<':
            break



# def main():
#     database = "library.db"
#     conn = create_connection(database)
#     start_menu(conn)
#     # user_menu(conn,"john.doe@example.com")

# if __name__ == '__main__':
#     main()


def main(file):
    conn = create_connection(file)
    start_menu(conn)
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No Database Found!")
        sys.exit(1)

    file = sys.argv[1]
    main(file)
