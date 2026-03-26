## 📚 Library Management System 

[![python Version](https://img.shields.io/badge/25.0.2-JAVA%2B-blue)](https://www.oracle.com/java/technologies/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![SQL](https://img.shields.io/badge/database-Mysql%20-orange)](https://dev.mysql.com/downloads/)

---

## 🎯 Project Overview
A web-based Library Management System using Python (Flask) and MySQL.
This Library Management System is a simple, console-based Python application designed to manage basic library operations.

## Key Objectives:

- Add new books to the library
- Display all available books
- Search for books by title
- Borrow and return books
- Remove books from the collection

---
## Features
- Role-based login (Admin/User)
- Admin can add, update, delete books
- Users can view/search books
- Registration for new users
- Attractive UI using CSS

## 📁 Project Structure

```
library_management_system/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project description and instructions
├── static/
│   └── style.css           # CSS for frontend styling
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── user_dashboard.html
│   ├── add_book.html
│   └── view_books.html
└── db_scripts/
    ├── create_tables.sql   # SQL to create users & books tables
    └── sample_data.sql     # Optional: sample data insertion
```

## Setup Instructions

1. **Clone Repo**
```bash
git clone https://github.com/yourusername/library_management_system.git
cd library_management_system
```
2. **Install dependencies**
 ```
pip install -r requirements.txt
```

3. **Setup Database**

Open MySQL
Run ```create_tables.sql``` and ``` sample_data.sql```in ```db_scripts/```
```
Example command:
USE library_db;
SOURCE path/to/db_scripts/create_tables.sql;
SOURCE path/to/db_scripts/sample_data.sql;
```

4.**Run Flask App**
```
python app.py
```



##  Project Structure
- app.py → Main backend
- templates/ → HTML pages
- static/ → CSS files
- db_scripts/ → SQL scripts

---

## 👨‍💻 Author

MAYURESH MADANE

- 🎓 Education: [B.TECH(IT)], [BATU UNIVERSITY]
- 🔗 LinkedIn: [https://www.linkedin.com/in/mayuresh-madane-82682428b]
-  🐙 GitHub: [https://github.com/MM07]
- 📧 Email:mayureshmadane44@gmail.com

