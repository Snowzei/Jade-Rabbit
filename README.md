# Jade Rabbit

This script is a simple tool to help you keep track of the people to whom you have lent money. It stores the loan information in a SQLite database file called "loans_*date*.db", which includes the loan date, the borrower's name, and the loan amount.
Requirements

``
Python 3
``

`` 
SQLite3
``

## Installation

To install the required packages, run the following command:

pip install -r requirements.txt

## Usage

To use the script, run the following command:

`` python loans.py [OPTIONS] ``

Options

    --create: Create a new database file called "loans_*date*.db"
    --add NAME AMOUNT: Add a new loan to the database with the borrower's name and the loan amount
    --display: Display all the loans in the database
    --combine OLD_DATABASE NEW_DATABASE: Combine two databases into a single database
    --search NAME: searches the database for loans with the given name and displays the total amount of money that person owes.
    --settle NAME AMOUNT: reduce the debt for the given name by the specified amount, or clear the debt if no amount is specified

## Examples

To create a new database file called "loans.db":

`` python loans.py --create ``

To add a new loan to the database with the borrower's name "John" and the loan amount "100":

`` python loans.py --add John 100 ``

To display all the loans in the database:

`` python loans.py --display ``

To combine two databases called "old_loans.db" and "new_loans.db" into a single database:

`` python loans.py --combine old_loans.db new_loans.db ``
