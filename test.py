from fastmcp import FastMCP
import os
import sqlite3

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

#Creating a tool to list down all the expenses present in the db
@mcp.tool()
def list_expense():
    with sqlite3.connect(DB_PATH) as c:
        curr=c.execute('''SELECT id,date,amount,category,subcategory,description FROM EXPENSE ORDER BY ID ASC''')
        cols=[d[0] for d in curr.description]
        return [dict(zip(cols,row)) for row in curr.fetchall()]

if __name__=="__main__":
    mcp.run()
