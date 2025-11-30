# Personal Expense Tracker (Flask + SQLite)

A simple and clean **web-based Expense Tracker** built using **Flask**, **SQLite**, and **HTML/CSS**.  
This application helps users track daily expenses, manage categories, filter by month, and export data.

---

## Features

###  Core Features
- Add new expenses  
- Edit and delete existing expenses  
- Filter expenses by **month** and **category**  
- View **total spending**  
- Automatically calculates category-wise totals  
- Export all expenses to **CSV**  
- Automatic database creation on first run  

###  UI Features
- Clean and simple interface  
- Responsive design  
- Organized table view for all expenses  

---

##  Tech Stack

| Part | Technology |
|------|------------|
| Backend | Flask (Python) |
| Database | SQLite |
| Frontend | HTML, CSS, Jinja Templates |
| Export | CSV |

---

##  Project Structure
expense-tracker/
│
├── app.py
├── requirements.txt
├── schema.sql
├── sample_data.csv
├── .gitignore
│
├── templates/
│ ├── base.html
│ ├── index.html
│ └── add_edit.html
│
└── static/
└── style.css

---

##  Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/byte-AbhijitVichare/expense-tracker.git
cd expense-tracker

### 2️⃣ Create Virtual Environment

python -m venv venv
.\venv\Scripts\activate   

### 3️⃣ Install Dependencies

pip install -r requirements.txt

### 4️⃣ Run the Application

python app.py

Then open the app in your browser:

http://127.0.0.1:5000/


Export Data

Click Export CSV to download all your expenses in a CSV file.

Future Enhancements:
Pie chart for category spending
Line chart for monthly spending trends
Dark mode theme
User authentication (login/signup)

License
This project is licensed under the MIT License.

Support the Project
If you like this project, please ⭐ star the repository!