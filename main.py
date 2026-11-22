from fastmcp import FastMCP
import os
import sqlite3
import json

mcp=FastMCP(name="Expense Tracker")

#Adding the path to the expense db file
DB_PATH=os.path.join(os.path.dirname(__file__), "expense.db")

#Creating and initializing the database table if it doesn't exists
def in_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS expense(
            id integer primary key autoincrement,
            date text not null,
            amount real not null,
            category text not null,
            subcategory text default '',
            description text default ''
            )
            ''')
        c.commit()    
in_db()

#Creating a add expense tool to insert the new expenses into the list
@mcp.tool()
def add_expense(date: str, amount: int, category: str, subcategory="", description=""):
    """Adds an expense to the database"""
    with sqlite3.connect(DB_PATH) as c:
        c.execute('''INSERT INTO expense(date, amount, category, subcategory, description)
                    VALUES(?,?,?,?,?)''', (date, amount, category, subcategory, description))
        c.commit()
    return "Expense added successfully"

# START_DATE = "2026-10-01"
# END_DATE = "2026-10-31"

#Creating a tool to remove any expense from the list based on the id
@mcp.tool()
def remove_expense(expense_id: int, date: str):
    """Removes an expense from the database by ID"""
    with sqlite3.connect(DB_PATH) as c:
        c.execute('''DELETE FROM expense WHERE id = ? or date = ?''', (expense_id,date))
        c.commit()
    return "Expense removed successfully from the list"

#Creating a tool to list down all the expenses present in the db
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, description
            FROM expense
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

#Including the server information
@mcp.resource("info://server")
def server_info() -> str:
    """Return the information about the server"""
    info = {
        "name": "Expense Tracker",
        "version": "1.0.0",
        "description": "A simple expense tracker server",
        "author": "Rajesh Kumar Sahoo",
        "tools": ["add_expense", "list_expenses", "remove_expense"],
        }
    return json.dumps(info,indent=3)

if __name__=="__main__":
    mcp.run(transport="http", host="0.0.0.0",port=8080)