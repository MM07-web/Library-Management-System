from flask import Flask, render_template, request, redirect , session
import mysql.connector
from datetime import date, timedelta

app = Flask(__name__)

# DB Connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pass@123",
        database="library_db"
    )


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            role = user[0]

            if role in ("librarian", "admin"):
                return redirect("/dashboard")
            else:
                return redirect("/user_dashboard")
        else:
            return "Invalid Login"

    return render_template("login.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# ---------------- DASHBOARD ----------------
@app.route("/user_dashboard")
def user_dashboard():
    return render_template("user_dashboard.html")



# ---------------- ADD BOOK ----------------
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    
    if session.get("role") == "admin":
        return "get access "
    
    if request.method == "POST":
        print("FORM SUBMITTED ✅")

        title = request.form["title"]
        author = request.form["author"]
        quantity = request.form["quantity"]

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO books (title, author, quantity) VALUES (%s,%s,%s)",
                (title, author, quantity)
            )
            conn.commit()
            print("Inserted successfully ✅")
        except Exception as e:
            print("ERROR:", e)

        return redirect("/view_books")

    return render_template("add_book.html")
# ---------------- Delete Book --------------------
@app.route("/delete_book/<int:book_id>")
def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()

    # 1️⃣ Delete all transactions related to this book
    cursor.execute("DELETE FROM transactions WHERE book_id=%s", (book_id,))

    # 2️⃣ Delete the book
    cursor.execute("DELETE FROM books WHERE book_id=%s", (book_id,))
    conn.commit()

    return redirect("/view_books")

# ------------ Update Book ---------------

@app.route("/update_book/<int:book_id>", methods=["GET", "POST"])
def update_book(book_id):
    if session.get("role") != "librarian":
        return "Access Denied ❌"

    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        quantity = request.form["quantity"]

        cursor.execute(
            "UPDATE books SET title=%s, author=%s, quantity=%s WHERE book_id=%s",
            (title, author, quantity, book_id)
        )
        conn.commit()
        return redirect("/view_books")

    cursor.execute("SELECT * FROM books WHERE book_id=%s", (book_id,))
    book = cursor.fetchone()
    return render_template("update_book.html", book=book)

# ---------------- VIEW BOOKS ----------------
@app.route("/view_books")
def view_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()

    return render_template("view_books.html", books=books)
# --------------- search book --------------

@app.route("/search_books")
def search_books():
    query = request.args.get("query")  # get input from form
    conn = connect_db()
    cursor = conn.cursor()

    # Search by title or author using LIKE
    sql = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
    search_value = f"%{query}%"
    cursor.execute(sql, (search_value, search_value))
    books = cursor.fetchall()

    return render_template("view_books.html", books=books)
# ----------------search -----------------------

@app.route("/search", methods=["GET", "POST"])
def search():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form["query"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s",
            ('%' + query + '%', '%' + query + '%')
        )
        results = cursor.fetchall()

    return render_template("search.html", results=results, query=query)

# --------------- register -------------    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()

        # Insert new user with role = user
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, "user")
        )
        conn.commit()

        return redirect("/")  # go to login page

    return render_template("register.html")

# --------------------- issue -------------------
from datetime import datetime, timedelta

# Issue Book
@app.route("/issue_book", methods=["GET", "POST"])
def issue_book():
    if session.get("role") != "librarian":
        return "Access Denied ❌"

    conn = connect_db()
    cursor = conn.cursor()

    if request.method == "POST":
        user_id = request.form["user_id"]
        book_id = request.form["book_id"]
        issue_date = datetime.now().date()

        # Insert into transactions
        cursor.execute(
            "INSERT INTO transactions (book_id, user_id, issue_date) VALUES (%s,%s,%s)",
            (book_id, user_id, issue_date)
        )
        conn.commit()

        return redirect("/view_transactions")

    # GET → show form
    cursor.execute("SELECT id, username FROM users WHERE role='user'")
    users = cursor.fetchall()
    cursor.execute("SELECT book_id, title FROM books")
    books = cursor.fetchall()

    return render_template("issue_book.html", users=users, books=books)


# ---------------------Return book ----------------
@app.route("/return_book/<int:transaction_id>")
def return_book(transaction_id):
    if session.get("role") != "librarian":
        return "Access Denied ❌"

    conn = connect_db()
    cursor = conn.cursor()

    # Get the transaction
    cursor.execute("SELECT issue_date FROM transactions WHERE transaction_id=%s", (transaction_id,))
    row = cursor.fetchone()
    if row is None:
        return "Transaction not found"

    issue_date = row[0]
    return_date = datetime.now().date()

    # Calculate fine (e.g., 10 Rs per day after 7 days)
    days_passed = (return_date - issue_date).days
    fine = 0
    if days_passed > 7:
        fine = (days_passed - 7) * 10

    # Update transaction
    cursor.execute(
        "UPDATE transactions SET return_date=%s, fine=%s WHERE transaction_id=%s",
        (return_date, fine, transaction_id)
    )
    conn.commit()

    return redirect("/view_transactions")


# ------------------transcation -------------------
@app.route("/view_transactions")
def view_transactions():
    if session.get("role") != "librarian":
        return "Access Denied ❌"

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.transaction_id, u.username, b.title, t.issue_date, t.return_date, t.fine
        FROM transactions t
        JOIN users u ON t.user_id=u.id
        JOIN books b ON t.book_id=b.book_id
    """)
    transactions = cursor.fetchall()
    return render_template("view_transactions.html", transactions=transactions)







# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
    
