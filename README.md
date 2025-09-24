# Food Donation and Surplus Management System

## Description:
This system helps manage surplus food from restaurants, households, and events and connects it with NGOs, charities, and needy people.It ensures food donations are recorded, matched, and tracked efficiently.

## Features:
User Registration & Login-Donors and NGOs can create accounts and login securely.
Add Food Donation (Donor)-Donors can add surplus food details: item, quantity, expiry date.
View Available Donations (NGO)-NGOs can browse all available food donations in real time.
Request Donation (NGO)-NGOs can request specific donations they need.
Approve / Reject Request (Donor)-Donors can approve or reject donation requests.
Donation Status Tracking-Track donations as “available”, “accepted”, or “distributed”.
 
 ## Project Structure:

 SURPLUS MANAGEMENT SYSTEM/
 |
 |---src/  # core application logic
 |     |---logic.py  # Business logic and task 
 operations
 |     |__db.py      # Database operations
 |
 |---API/             # Backend api
 |    |__main.py      # FastAPI endpoints
 |
 |---FrontEnd/         # Frontend application
 |    |__app.py        # Streamlit web interface
 |
 |___requirements.txt  # Python Dependencies
 |
 |___README.md  # Python Documentation
 |
 |___.env   # Python Variables


## Quick Start

### Prerequisites

-Python 3.8 or higher
-A Supabase Account
-Git(Push,cloning)
 
### 1.Clone or download the project
 # Option 1: Clone with Git
 git clone <repository url>

 # Option 2:Download and extract the ZIP file

### 2.Install Dependencies
  
  # install all required python packages
  pip install -r  requirements.txt

###  3.Setup supabase database

1.Create a supabase project
2.Create the task tables:
   -Go to the sql editor in your supabase  dashboard
   -Run this sql command:
   ```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('donor','ngo')) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE requests (
    request_id SERIAL PRIMARY KEY,
    ngo_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    donation_id INTEGER REFERENCES donations(donation_id) ON DELETE CASCADE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE donations (
    donation_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    food_item TEXT NOT NULL,
    quantity TEXT NOT NULL,
    expiry_date DATE,
    status TEXT DEFAULT 'available',
    created_at TIMESTAMP DEFAULT NOW()
);
```
3. **Get Your Credentials:

### 4.Configure environment Variable

1.Create a `.env` file in the project root

2.Add your Supabase credentials to `.env`;
SUPABASE_URL=your_project_url_here
SUPABASE_KEY=your_anon_key_here

**Example:**
SUPABASE_URL="https://idrpcwtugfjsxjvfgrym.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlkcnBjd3R1Z2Zqc3hqdmZncnltIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTgwODIyNDgsImV4cCI6MjA3MzY1ODI0OH0.i_tThAqol4gDRoIgMl6l6LiwG05sWQFdPmHGS7ux1jM"

### 5. Run the Application

## Streamlit Frontend
streamlit run FrontEnd/app.py

The app will open in your browser at `http://localhost:8080`

## FastAPI Backend

cd API
python main.py
 
The API will be available at `http://localhost:8081`

## How to use

**Frontend**:Streamlit(Python web framework)
**Backend**:FastAPI(Python REST API framework)
**Database**:Supabase(PostgreSQL-based backend-as-a-service)
**Language**:Python 3.8+

### Key Components

1.**`src/db.py`** :Database operations
   - Handles all CRUD operations with Supabase
2.**`src/logic.py`**:Business logic
    - Task validation and processing


### Troubleshooting

## Common Issues

1.**"Module not found" Errors**
     - Make sure you've installed all dependencies: `pip install -r requirements.txt`
     - Check that you've running commands from the correct directory
    
## Future Enhancements

Ideas for extending this project:

- **USer Authentication**:Add user accounts and login
- **Task Categories**:Organize tasks by subject or category
- **Notifications**:Email or push notifications for due dates
- **File Attachments**:Attach files to tasks
- **Collaboration**:Share tasks with classmates
- **Mobile App**:React Native or Flutter mobile version
- **Data Export**:Export tasks to CSV or PDF
- **Task Templates**:Create reusable task templates

## Support

If you encounter any issues or have questions:
Phone number:`7842285882`
Email:`varshareddy1808@gmail.com`