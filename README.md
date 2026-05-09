# BudgetNest - Expense Tracker Application

## Overview
BudgetNest is a web-based expense tracking application developed to help users efficiently manage and monitor their daily expenses. The application allows users to record expenses based on categories and purposes, track individual family member expenses, and analyze spending patterns through monthly and yearly filters.

The project is designed with a user-friendly interface and provides an organized way to maintain personal and family financial records.

---

## Features
- User authentication and secure login system
- Daily expense tracking and management
- Category-based expense recording
- Family member-wise expense monitoring
- Monthly and yearly expense filtering
- Expense summary and analysis dashboard
- Responsive and user-friendly interface
- Secure data storage using SQLite/MySQL database

---

## Technologies Used
- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: SQLite / MySQL

---

## Project Structure

```bash
BudgetNest/
│
├── accounts/
├── BudgetNest/
├── family/
├── static/
├── templates/
├── db.sqlite3
├── manage.py
└── README.md

Installation Steps
1. Clone the Repository
git clone https://github.com/your-username/BudgetNest.git
2. Navigate to Project Directory
cd BudgetNest
3. Create Virtual Environment
python -m venv env
4. Activate Virtual Environment
Windows
env\Scripts\activate
Linux / Mac
source env/bin/activate
5. Install Required Packages
pip install -r requirements.txt
6. Apply Migrations
python manage.py makemigrations
python manage.py migrate
7. Run the Server
python manage.py runserver
Output

The BudgetNest application helps users efficiently manage and analyze expenses with category-wise and family member-wise tracking. The filtering and reporting features support better budgeting and financial planning.


