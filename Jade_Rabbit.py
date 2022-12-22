import sqlite3
import argparse
import datetime
import os
import glob

def connect_to_db():
    """
    Connect to the first .db file found in the current directory.

    Returns:
    - sqlite3.Connection: A connection to the .db file.
    """
    # Find all .db files in the current directory
    files = glob.glob("*.db")
    # Check if any .db files were found
    if not files:
        print("Error: no .db files found")
        return
    # Get the first .db file found
    filename = files[0]
    # Connect to the .db file and return the connection
    return sqlite3.connect(filename)

def create_loans_table():
    """
    Create a table called "loans" in the database file "loans.db" to store loan information.
    The table will have the following columns: id, date, name, amount.
    """
    # Get the current date in YYYY-MM-DD format
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Create the filename for the database file
    filename = f'loans_{date}.db'
    # Connect to the database file
    conn = sqlite3.connect(filename)
    # Execute the SQL statement to create the "loans" table
    conn.execute('''CREATE TABLE loans (id INTEGER PRIMARY KEY AUTOINCREMENT, date text, name text, amount real)''')
    # Close the connection to the database file
    conn.close()


def add_loan(name, amount):
    """
    Add a new loan to the "loans" table in the first .db file found in the current directory, with the current date as the loan date.

    Args:
    - name (str): The name of the borrower.
    - amount (float): The amount of the loan.
    """
    # Convert the amount to a floating point number
    amount = float(amount)
    # Connect to the database
    conn = connect_to_db()
    # Get the current date in YYYY-MM-DD format
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # Execute the SQL statement to insert a new row into the "loans" table
    conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, amount))
    # Save the changes to the database
    conn.commit()
    # Close the connection to the database
    conn.close()

def display_loans():
    """
    Display all the loans in the "loans" table in the first .db file found in the current directory.
    """
    # Connect to the database
    conn = connect_to_db()
    # Get a cursor object for executing SQL statements
    cursor = conn.execute("SELECT * FROM loans")
    # Iterate through the rows of the "loans" table and print each row
    for row in cursor:
        print(row)
    # Close the connection to the database
    conn.close()

def get_total_amount(name):
    """
    Get the total amount of loans for a specific person from the "loans" table in the first .db file found in the current directory.

    Args:
    - name (str): The name of the borrower.

    Returns:
    - float: The total amount of loans for the borrower.
    """
    # Connect to the database
    conn = connect_to_db()
    # Get a cursor object for executing SQL statements
    cursor = conn.execute("SELECT * FROM loans WHERE name=?", (name,))
    # Initialize the total amount to 0
    total_amount = 0
    # Iterate through the rows of the "loans" table and add the amount for each loan to the total amount
    for row in cursor:
        total_amount += row[3]
    # Close the connection to the database
    conn.close()
    # Return the total amount of loans for the borrower
    return total_amount

def search_name(name):
    """
    Search for loans in the "loans" table in the first .db file found in the current directory for a specific person.

    Args:
    - name (str): The name of the borrower.
    """
    # Get the total amount of loans for the borrower
    total_amount = get_total_amount(name)
    # Print the total amount of loans for the borrower
    print(f'{name} owes a total of {total_amount}')

def settle_debt(name, amount=None):
    """
    Settle a loan in the "loans" table in the first .db file found in the current directory.
    If no amount is specified, the loan is considered to be fully settled.
    Otherwise, the specified amount is subtracted from the original loan amount.

    Args:
    - name (str): The name of the borrower.
    - amount (float, optional): The amount to be settled. If not provided, the loan is considered to be fully settled.
    """
    # Connect to the database
    conn = connect_to_db()
    # Get the total amount of loans for the borrower
    total_amount = get_total_amount(name)
    # Get the current date in YYYY-MM-DD format
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    # If no amount was provided, insert a row into the "loans" table with a negative amount equal to the total amount of loans for the borrower
    if amount == None:
        conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, -total_amount))
    # If an amount was provided, insert a row into the "loans" table with a negative amount equal to the provided amount
    else:
        conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, -int(amount)))
    # Save the changes to the database
    conn.commit()
    # Close the connection to the database
    conn.close()

def combine_databases(old_filename, new_filename):
    """
    Combine the data from the first .db file found in the current directory with the specified new database,
    while avoiding duplicates.

    Args:
    - old_filename (str): The filename of the old database.
    - new_filename (str): The filename of the new database.
    """
    # Connect to the old and new databases
    conn_old = sqlite3.connect(old_filename)
    conn_new = sqlite3.connect(new_filename)
    # Get cursor objects for executing SQL statements on the old and new databases
    cursor_old = conn_old.execute("SELECT * FROM loans")
    cursor_new = conn_new.execute("SELECT * FROM loans")
    # Insert the data from the new database into the old database, avoiding duplicates
    # Get the next available id value for the "loans" table in the old database
    next_id = cursor_old.execute("SELECT MAX(id) FROM loans").fetchone()[0] + 1
    # Iterate through the rows of the "loans" table in the new database
    for row in cursor_new:
        # Check if a row with the same date, name, and amount already exists in the "loans" table in the old database
        if not cursor_old.execute("SELECT * FROM loans WHERE date=? AND name=? AND amount=?", row[1:]).fetchone():
            # If the row does not exist, insert it into the "loans" table in the old database
            conn_old.execute("INSERT INTO loans (id, date, name, amount) VALUES (?, ?, ?, ?)", (next_id, *row[1:]))
            next_id += 1
    # Commit the changes and close the connections
    conn_old.commit()
    conn_new.commit()
    conn_old.close()
    conn_new.close()
    # Delete the old file
    os.remove(new_filename)

def main():
    """
    Command-line utility for keeping track of loans.

    The available commands are:
    - create: create a new database
    - add: add a new loan to the database
    - display: display all the loans in the database
    - search: search the database for loans with the given name and display the total amount of money that person owes
    - settle: settle a loan in the database. If no amount is specified, the loan is considered to be fully settled. Otherwise, the specified amount is subtracted from the original loan amount.
    - combine: combine two databases
    """
    # Create a parser for parsing command-line arguments
    parser = argparse.ArgumentParser(description='Keep track of the people to whom you have lent money.')
    # Add arguments for each of the available commands
    parser.add_argument('--create', action='store_true', help='create a new database')
    parser.add_argument('--add', nargs=2, metavar=('NAME', 'AMOUNT'), help='add a new loan to the database')
    parser.add_argument('--display', action='store_true', help='display all the loans in the database')
    parser.add_argument('--search', nargs=1, metavar=('NAME'), help='search the database for loans with the given name and display the total amount of money that person owes')
    parser.add_argument('--settle', nargs='+', metavar=('NAME', 'AMOUNT'), help='settle a loan in the database. If no amount is specified, the loan is considered to be fully settled. Otherwise, the specified amount is subtracted from the original loan amount.')
    parser.add_argument('--combine', nargs=2, metavar=('OLD_DATABASE', 'NEW_DATABASE'), help='combine two databases')
    # Parse the command-line arguments
    args = parser.parse_args()

    if args.create:
        create_loans_table()
    elif args.add:
        name, amount = args.add
        add_loan(name, amount)
    elif args.display:
        display_loans()
    elif args.search:
        name = args.search[0]
        search_name(name)
    elif args.settle:
        name, amount = args.settle
        settle_debt(name, amount)
    elif args.combine:
        old_filename, new_filename = args.combine
        combine_databases(old_filename, new_filename)

if __name__ == '__main__':
    main()