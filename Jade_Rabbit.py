import sqlite3
import argparse
import datetime

def create_loans_table():
    """Creates a table called "loans" in the database file "loans.db" to store the loan information."""
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'loans_{date}.db'
    conn = sqlite3.connect(filename)
    conn.execute('''CREATE TABLE loans (date text, name text, amount real)''')
    conn.close()

def add_loan(name, amount):
    """Adds a new loan to the "loans" table in the database file "loans.db", with the current date as the loan date."""
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'loans_{date}.db'
    conn = sqlite3.connect(filename)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, amount))
    conn.commit()
    conn.close()

def display_loans():
    """Displays all the loans in the "loans" table in the database file "loans.db"."""
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'loans_{date}.db'
    conn = sqlite3.connect(filename)
    cursor = conn.execute("SELECT * FROM loans")
    for row in cursor:
        print(row)
    conn.close()

def combine_databases(old_filename, new_filename):
    """Combines the data from two databases into a single database."""
    # Connect to the old and new databases
    conn_old = sqlite3.connect(old_filename)
    conn_new = sqlite3.connect(new_filename)
    cursor_old = conn_old.execute("SELECT * FROM loans")
    cursor_new = conn_new.execute("SELECT * FROM loans")
    # Insert the data from the old database into the new database
    for row in cursor_old:
        conn_new.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", row)
    # Insert the data from the new database into the old database
    for row in cursor_new:
        conn_old.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", row)
    # Commit the changes and close the connections
    conn_old.commit()
    conn_new.commit()
    conn_old.close()
    conn_new.close()

def main():
    parser = argparse.ArgumentParser(description='Keep track of the people to whom you have lent money.')
    parser.add_argument('--create', action='store_true', help='create a new database')
    parser.add_argument('--add', nargs=2, metavar=('NAME', 'AMOUNT'), help='add a new loan to the database')
    parser.add_argument('--display', action='store_true', help='display all the loans in the database')
    parser.add_argument('--combine', nargs=2, metavar=('OLD_DATABASE', 'NEW_DATABASE'), help='combine two databases')
    args = parser.parse_args()

    if args.create:
        create_loans_table()
    elif args.add:
        name, amount = args.add
        add_loan(name, amount)
    elif args.display:
        display_loans()
    elif args.combine:
        old_filename, new_filename = args.combine
        combine_databases(old_filename, new_filename)

if __name__ == '__main__':
    main()