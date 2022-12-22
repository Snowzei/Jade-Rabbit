import sqlite3
import argparse
import datetime
import os

def connect_to_db():
    import glob
    files = glob.glob("*.db")
    if not files:
        print("Error: no .db files found")
        return
    filename = files[0]
    return sqlite3.connect(filename)

def create_loans_table():
    """Creates a table called "loans" in the database file "loans.db" to store the loan information."""
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'loans_{date}.db'
    conn = sqlite3.connect(filename)
    conn.execute('''CREATE TABLE loans (id INTEGER PRIMARY KEY AUTOINCREMENT, date text, name text, amount real)''')
    conn.close()

def add_loan(name, amount):
    """Adds a new loan to the "loans" table in the first .db file found in the current directory, with the current date as the loan date."""
    amount = float(amount)  # convert amount to a floating point number
    conn = connect_to_db()
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, amount))
    conn.commit()
    conn.close()

def display_loans():
    """Displays all the loans in the "loans" table in the first .db file found in the current directory."""
    conn = connect_to_db()
    cursor = conn.execute("SELECT * FROM loans")
    for row in cursor:
        print(row)
    conn.close()

def get_total_amount(name):
    conn = connect_to_db()
    cursor = conn.execute("SELECT * FROM loans WHERE name=?", (name,))
    total_amount = 0
    for row in cursor:
        total_amount += row[3]
    conn.close()
    return total_amount

def search_name(name):
    """Searches for loans in the "loans" table in the first .db file found in the current directory for a specific person."""
    total_amount = get_total_amount()
    print(f'{name} owes a total of {total_amount}')

def settle_debt(name, amount=None):
    """Settles a loan in the "loans" table in the first .db file found in the current directory. If no amount is specified, the loan is considered to be fully settled. Otherwise, the specified amount is subtracted from the original loan amount."""
    conn = connect_to_db()
    total_amount = get_total_amount(name)
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    if amount == None:
        conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, -total_amount))
    else:
        conn.execute("INSERT INTO loans (date, name, amount) VALUES (?, ?, ?)", (date, name, -int(amount)))
    conn.commit()
    conn.close()

def combine_databases(old_filename, new_filename):
    """Combines the data from the first .db file found in the current directory with the specified new database,
    while avoiding duplicates."""
    # Connect to the old and new databases
    conn_old = sqlite3.connect(old_filename)
    conn_new = sqlite3.connect(new_filename)
    cursor_old = conn_old.execute("SELECT * FROM loans")
    cursor_new = conn_new.execute("SELECT * FROM loans")
    # Insert the data from the new database into the old database, avoiding duplicates
    next_id = cursor_old.execute("SELECT MAX(id) FROM loans").fetchone()[0] + 1
    for row in cursor_new:
        if not cursor_old.execute("SELECT * FROM loans WHERE date=? AND name=? AND amount=?", row[1:]).fetchone():
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
    parser = argparse.ArgumentParser(description='Keep track of the people to whom you have lent money.')
    parser.add_argument('--create', action='store_true', help='create a new database')
    parser.add_argument('--add', nargs=2, metavar=('NAME', 'AMOUNT'), help='add a new loan to the database')
    parser.add_argument('--display', action='store_true', help='display all the loans in the database')
    parser.add_argument('--search', nargs=1, metavar=('NAME'), help='search the database for loans with the given name and display the total amount of money that person owes')
    parser.add_argument('--settle', nargs='+', metavar=('NAME', 'AMOUNT'), help='settle a loan in the database. If no amount is specified, the loan is considered to be fully settled. Otherwise, the specified amount is subtracted from the original loan amount.')
    parser.add_argument('--combine', nargs=2, metavar=('OLD_DATABASE', 'NEW_DATABASE'), help='combine two databases')
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