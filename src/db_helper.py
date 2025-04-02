import sqlite3
import datetime
from typing import List, Tuple, Any

class DatabaseHelper:
    def __init__(self, db_name: str = "expense_tracker.db"):
        """Initialize the database connection."""
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database."""
        return sqlite3.connect(self.db_name)

    def fetch_one(self, query, params):
        """Executes a query and returns one result."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()  # Fetches a single row

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()):
        """Execute an INSERT, UPDATE, DELETE query."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()

        cursor.execute("VACUUM;")
        conn.commit()
        print(f'{query} executed successively');
        conn.close()

    def fetch_all(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """Fetch all rows from a SELECT query."""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        print(results)
        return results

    def create_tables(self):
        """Create tables if they don't exist."""
        user_table = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT Member,
            date_joined TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
        transaction_table = '''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            category TEXT CHECK(category IN ('Food','Housing','Transport','Entertainment','Insurance','Health','Debt','Personal Care','Others','None')) NOT NULL,
            type TEXT CHECK(type IN ('income', 'expense', 'saving')) NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        '''
        self.execute_query(user_table)
        self.execute_query(transaction_table)

    ## ------------------- USERS TABLE FUNCTIONS ------------------- ##
    def add_user(self, username: str,email: str,  password: str):
        """Add a new user."""
        query = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)"
        self.execute_query(query, (email, username, password))
        return True

    def update_user_info(self,user_id:int, username: str,email: str):
        """Add a new user."""
        print(user_id ," ", username," ",email)
        query = "UPDATE users SET email = ? ,username = ? WHERE id = ?"
        print(self.execute_query(query, (email, username,user_id,)))
        return True

    def get_all_users(self):
        """Retrieve all users."""
        datas = []
        query = "SELECT id, email, username, date_joined FROM users"
        users = self.fetch_all(query)
        for user in users:
            datas.append({"id":user[0],"name":user[2],"email":user[1],"date":user[3]})
        return datas

    def get_user_by_id(self, user_id: int):
        """Retrieve a user by ID."""
        query = "SELECT id, email, username, date_joined FROM users WHERE id = ?"
        return self.fetch_all(query, (user_id,))

    def get_user_metrics_sum(self,user_id:int,is_admin: bool = False):
        print("id",user_id)
        """Retrieve the total amount (sum) of transactions for a specific user."""
        datas= []
        mydict ={}
        query = "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type=?"
        income = self.fetch_one(query, (user_id,"income",))  # Pass parameters as a tuple
        expenses = self.fetch_one(query, (user_id, "expense",))  # Pass parameters as a tuple
        savings = self.fetch_one(query, (user_id, "saving",))  # Pass parameters as a tuple

        # Handle None values by using a default value of 0 if no results are found
        total_income = income[0] if income[0] is not None else 0.0
        total_expenses = expenses[0] if expenses[0] is not None else 0.0
        total_savings = savings[0] if savings[0] is not None else 0.0

        # Calculate wallet balance: Income - Expenses + Savings
        wallet_balance = total_income - total_expenses + total_savings
        # Assuming 'income[0]' is a number and you want to format it with "FCFA"
        if is_admin:
            user_query = "SELECT username,email,date_joined FROM users WHERE id = ?"
            user = self.fetch_one(user_query, (user_id,))
            print("user",user)
            mydict["name"]=user[0]
            mydict["email"] = user[1]
            mydict["date"] = user[2]
            mydict["wallet_balance"] = wallet_balance
            mydict["total_income"] = total_income
            mydict["total_expenditure"] = total_expenses
            mydict["total_savings"] = total_savings

            return mydict
        else:
            datas.append({"title": "Total Income", "amt": str(total_income) + " FCFA"})

            datas.append({"title": "Total Expenses", "amt": str(total_expenses) + " FCFA"})

            datas.append({"title": "Total Savings", "amt": str(total_savings) + " FCFA"})
            datas.append({"title": "My Wallet", "amt": str(wallet_balance) + " FCFA"})

            return datas

    def calculate_monthly_metrics(self):
        """Retrieve the total amount (sum) of transactions for a specific user."""
        datas = []
        query = "SELECT SUM(amount) FROM transactions WHERE type=?"
        income = self.fetch_one(query, ("income",))  # Pass parameters as a tuple
        expenses = self.fetch_one(query, ("expense",))  # Pass parameters as a tuple
        savings = self.fetch_one(query, ("saving",))  # Pass parameters as a tuple

        # Handle None values by using a default value of 0 if no results are found
        total_income = income[0] if income[0] is not None else 0.0
        total_expenses = expenses[0] if expenses[0] is not None else 0.0
        total_savings = savings[0] if savings[0] is not None else 0.0

        datas.append({"title": "Total Income", "amt": str(total_income) + " FCFA"})

        datas.append({"title": "Total Expenses", "amt": str(total_expenses) + " FCFA"})

        datas.append({"title": "Total Savings", "amt": str(total_savings) + " FCFA"})
        return datas

    def get_last_7_days_expenses(self, user_id: int = None):
        """Retrieve the expenses for the last 7 days in a specific format."""
        expenses_data = []

        # Get the last 7 days dates (including today)
        for i in range(6, -1, -1):  # 6 to 0 (7 days in total)
            day = datetime.datetime.now() - datetime.timedelta(days=i)
            date_str = day.strftime("%m/%d/20%y")  # Store date in standard format
            print("Date str: ",date_str)

            # Query to get the sum of expenses for the given date
            if(user_id == None):
                query = """
                                 SELECT SUM(amount) 
                                 FROM transactions 
                                 WHERE type = 'expense' AND date = ?
                             """
                result = self.fetch_all(query, (date_str,))
            else:
                query = """
                     SELECT SUM(amount) 
                     FROM transactions 
                     WHERE type = 'expense' AND user_id = ? AND date = ?
                 """
                result = self.fetch_all(query, (user_id, date_str))

            # Check if there's any data for this day, default to 0 if not
            total_amount = result[0][0] if result[0][0] is not None else 0


            # Format the date into the "Mar 4" format
            formatted_date = day.strftime("%b %d")

            # Append the formatted date and amount to the list
            expenses_data.append({"date": formatted_date, "amount": total_amount})

        return expenses_data


    def get_user_by_email(self, email: str):
        """Retrieve a user by ID."""
        query = "SELECT * FROM users WHERE email = ?"
        return self.fetch_all(query, (email,))

    def login(self, email: str , password: str):
        """Retrieve a user by ID."""
        query = "SELECT id,role FROM users WHERE email = ? AND password = ?"
        return self.fetch_all(query, (email,password,))

    def delete_user(self, user_id: int):
        """Delete a user (and their transactions)."""
        query = "DELETE FROM users WHERE id = ?"
        self.execute_query(query, (user_id,))
        query = "DELETE FROM transactions WHERE user_id = ?"
        self.execute_query(query, (user_id,))
        return True

    ## ------------------- TRANSACTIONS TABLE FUNCTIONS ------------------- ##
    def add_transaction(self, user_id: int, title: str,category: str, trans_type: str, amount: float, description: str, date: str):
        """Add a transaction with a user-specified date."""
        query = "INSERT INTO transactions (user_id, title,category, type, amount, description, date) VALUES (?, ?, ?,?, ?, ?, ?)"
        self.execute_query(query, (user_id, title,category, trans_type, amount, description, date))
        return True

    def get_transactions_by_user(self, user_id: int ,type: str ="all"):
        """Retrieve all transactions for a user."""
        result  = []
        if user_id == None:
            query = "SELECT t.id, t.title, t.type, t.amount, t.description, t.date,u.username FROM transactions t JOIN users u ON t.user_id = u.id"
        else:
            query = "SELECT t.id, t.title, t.type, t.amount, t.description, t.date,u.username FROM transactions t JOIN users u ON t.user_id = u.id WHERE user_id = ?"
        if(type == "limit"):
            query= query + " LIMIT 5"
        if user_id == None:
            result = self.fetch_all(query)
        else:
            result = self.fetch_all(query, (user_id,))
        transactions = []
        for row in result:
            transactions.append({
                "id":row[0],
                "amount": row[3],
                "title": row[1],
                "type": row[2],
                "date": row[5],
                "description": row[4],
                "username": row[6]  # Add username if needed
            })

        return transactions

    def get_all_transactions(self,type:str = "all"):
        """Retrieve all transactions for a user."""

        query = """
        SELECT t.id, t.title, t.type, t.amount, t.description, t.date, u.username ,t.category
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        """
        if (type == "limit"):
            query = query + " LIMIT 5"

        # Execute the query with the user_id parameter
        result = self.fetch_all(query)
        transactions = []

        # Process the result (this will return a list of tuples)
        for row in result:
            transactions.append({
                "amount": row[3],
                "title": row[1],  # The 'title' field is being used as the 'category'
                "type": row[2],
                "date": row[5],
                "description": row[4],
                "username": row[6],
                "category":row[7]
            })

        return transactions

    def get_transactions_by_type(self, user_id: int, trans_type: str):
        """Retrieve transactions of a specific type (income, expense, saving)."""
        query = "SELECT id, title, amount, description, date FROM transactions WHERE user_id = ? AND type = ?"
        return self.fetch_all(query, (user_id, trans_type))

    def get_transaction_by_id(self, trans_id: int):
        """Retrieve transactions of a specific type (income, expense, saving)."""
        query = "SELECT  title, amount,type ,category, description, date FROM transactions WHERE id = ?"
        return self.fetch_all(query, (trans_id,))

    def get_last_month(self,categories: [],user_id: int):
        amounts = []

        for category in categories:
            query = "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type= ? AND category = ? AND (substr(date, 7, 4) || '-' || substr(date, 1, 2) || '-' || substr(date, 4, 2)) BETWEEN DATE('now', 'start of month', '-1 month') AND DATE('now', 'start of month', '-1 day')"
            result  = self.fetch_one(query, (user_id, "expense",category))
            if(result[0]==None):
                amounts.append(0)
            else:
                amounts.append(result[0])

        return amounts
    def get_this_month(self,categories: [],user_id: int):
        amounts = []
        for category in categories:
            query = "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type= ? AND category = ? AND (substr(date, 7, 4) || '-' || substr(date, 1, 2) || '-' || substr(date, 4, 2)) BETWEEN DATE('now', 'start of month') AND DATE('now', 'start of month', '+1 month', '-1 day')"
            result = self.fetch_one(query, (user_id, "expense",category))
            if (result[0] == None):
                amounts.append(0)
            else:
                amounts.append(result[0])

        return amounts

    def get_categories_percentage(self,categories: [],user_id: int):
        amounts = []
        for category in categories:
            query = "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type= ? AND category = ?"
            result = self.fetch_one(query, (user_id, "expense", category))
            if (result[0] == None):
                amounts.append(0)
            else:
                amounts.append(result[0])


        return amounts

    def get_month_transaction(self):
        query = '''
                    WITH RECURSIVE months(month_num) AS (
                        SELECT 1
                        UNION ALL
                        SELECT month_num + 1 FROM months WHERE month_num < 12
                    )
                    SELECT 
                        m.month_num,
                        COALESCE(SUM(t.amount), 0) AS total_amount
                    FROM months m
                    LEFT JOIN transactions t
                        ON m.month_num = CAST(substr(t.date, 1, 2) AS INTEGER)
                        AND substr(t.date, 7, 4) = strftime('%Y', 'now')
                     
                    GROUP BY m.month_num
                    ORDER BY m.month_num
                '''
        results = self.fetch_all(query)
        return [row[1] for row in results]
    def get_heights(self,user_id: int ,type:str):
        query = '''
            WITH RECURSIVE months(month_num) AS (
                SELECT 1
                UNION ALL
                SELECT month_num + 1 FROM months WHERE month_num < 12
            )
            SELECT 
                m.month_num,
                COALESCE(SUM(t.amount), 0) AS total_amount
            FROM months m
            LEFT JOIN transactions t
                ON m.month_num = CAST(substr(t.date, 1, 2) AS INTEGER)
                AND substr(t.date, 7, 4) = strftime('%Y', 'now')
                AND t.user_id = ?
                AND t.type = ?
            GROUP BY m.month_num
            ORDER BY m.month_num
        '''
        results = self.fetch_all(query, (user_id, type))
        return [row[1] for row in results]  # Return list of amounts


    def get_transactions_by_date(self, user_id: int, date: str):
        """Retrieve transactions for a user on a specific date."""
        query = "SELECT id, title, type, amount, description FROM transactions WHERE user_id = ? AND date = ?"
        return self.fetch_all(query, (user_id, date))

    def update_transaction(self, trans_id: int, title: str,expense_type: str, trans_type: str,  amount: float, description: str, date: str):
        """Update a transaction with a new date."""
        query = "UPDATE transactions SET title = ?, type = ?, category = ?, amount = ?, description = ?, date = ? WHERE id = ?"
        self.execute_query(query, (title, trans_type,expense_type, amount, description, date, trans_id))
        return True

    def delete_transaction(self, trans_id: int):
        """Delete a transaction."""
        query = "DELETE FROM transactions WHERE id = ?"
        self.execute_query(query, (trans_id,))
        return True
