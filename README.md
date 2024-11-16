# Blood Bank Management System

## Project Description
A web-based application for managing blood donors, blood requests, and administrative functions. This application allows users to register as blood donors, request blood, and enables admins to manage donor information and blood requests. It is built using Python, Flask, and SQLite.

### Features
1. *User Registration:* Allows users to register as blood donors with details like name, blood type, age, and contact information.
2. *Blood Request Search:* Users can search for compatible blood donors by blood type.
3. *Admin Authentication:* Admins can securely log in to manage donor data.
4. *Admin Dashboard:* Admins can view, add, and delete donor information as well as see blood requests.
5. *Session Management:* User sessions are managed for secure admin access.

### Project Structure
- *app.py:* Main application file that initializes Flask and defines routes and database setup.
- *Templates Folder:* Contains the HTML files for rendering different pages.
    - *index.html:* Home page.
    - *admin.html:* Admin login page.
    - *dashboard.html:* Admin dashboard to view and manage donors and requests.
    - *become_donor.html:* Form page for users to register as donors.
    - *need_blood.html:* Search page to find donors by blood type.

## Setup and Installation
### Prerequisites
- Python 3.x
- Flask
- SQLite

### Installation Steps
1. Clone the Repository.
```
git clone https://github.com/your-username/blood-bank-management-system.git
cd blood-bank-management-system
```
2. Install Dependencies Install the required Python packages using pip.
```
pip install Flask
```

3. Initialize the Database Run the following to create the `blood_bank.db` SQLite database and required tables:
```
python app.py
```
This will create tables for `Admin`, `Donor`, and `Request` in the database and add an initial admin user.

4. Start the Application Run the Flask application:
```
python app.py
```
The application will be available at `http://127.0.0.1:5000`.

### Admin Credentials
The initial admin credentials are:
- Username: `admin`
- Password: `123`
*For security, please update the password after your first login.*

### Usage 
- *Admin Login:* Go to `/admin` to access the login page for the admin.
- *Donor Registration:* Go to `/become_donor` to sign up as a blood donor.
- *Blood Request Search:* Go to `/need_blood` to search for donors by blood type.  

### Project Routes
1. `/` -	Home page.
2. `/admin` -	Admin login page.
3. `/admin/dashboard`	- Admin dashboard.
4. `/admin/add_donor`	- Route for adding a new donor (POST).
5. `/admin/delete_donor/<donor_id>` -	Delete a donor (Admin Only).
6. `/become_donor` -	Donor registration page.
7. `/need_blood` -	Page to search for blood donors.

## Database Schema
The application uses three tables:

1. *Admin:* Stores admin login credentials.
2. *Donor:* Stores details about blood donors.
3. *Request:* Stores blood request details.

## License
This project is open-source and available under the MIT License.










