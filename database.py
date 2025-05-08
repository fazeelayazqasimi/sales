import sqlite3

def create_db():
    conn = sqlite3.connect('sales_commission.db')
    cursor = conn.cursor()

    # Creating agents table if not already exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS agents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        number TEXT,
                        email TEXT,
                        address TEXT,
                        joining_date TEXT,
                        salary REAL,
                        username TEXT,
                        password TEXT)''')

    # Creating sales table (if not exists)
    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        agent_id INTEGER,
                        customer_name TEXT,
                        customer_number TEXT,
                        address TEXT,
                        order_number TEXT,
                        platform TEXT,
                        product_detail TEXT,
                        imea TEXT,
                        price REAL,
                        commission REAL,
                        sale_date TEXT,
                        FOREIGN KEY (agent_id) REFERENCES agents(id))''')

    conn.commit()
    conn.close()

# Ensure the database is created
create_db()
