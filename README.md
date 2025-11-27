**Online Job Recruitment & Application Portal**
A full-stack web application built for Flipkart Internship Task — with Role-Based Access, Email Notifications, and Job Workflow Management.

**Overview**
This project simulates a real-world job recruitment system where Applicants apply for jobs, Employers post and manage job listings, and Admins oversee the entire platform.
The system is built using:
Frontend : HTML, CSS, JavaScript
Backend : Django (Python)
Database : MySQL
Authentication : Django Auth + Custom Role-Based Access
Emails : SMTP (Gmail)

**Features**
Admin - Can log into admin dashboard, manage all users/jobs/applications
Employer - Post jobs, edit jobs, view applicants, update status, send notifications
Applicant - Browse jobs, apply with resume (PDF), track applications

**Functional Modules**

	•	 Single authentication page with Login / Register toggle
	•	 Role-based signup (dynamic fields per role)
	•	 Job posting with title, salary range, skills, deadlines, company name
	•	 Job search + filters (by keyword, salary, category, experience)
	•	 Resume upload validation (PDF only, max 5MB, MIME & Binary validation)
	•	 Real email notifications for:
	•	Signup confirmation
	•	Job applied
	•	Application status updated (Selected / Rejected / Under Review)
	•	 Employer dashboard: Job performance + application count
	•	 Applicant dashboard: Track application status

**Installation & Setup Guide**

1) Clone the Repository 
    git clone https://github.com/GVSASIDHAR/JOB_PORTAL.git
    cd JOB_PORTAL
2)  Create Virtual Environment
    python3 -m venv jpvenv
    source jpvenv/bin/activate
3)  Install Dependencies
    pip install -r requirements.txt
4)  Configure Environment Variables
    DB_NAME=job_portal
    DB_USER=jobuser
    DB_PASSWORD=jobpass
    DB_HOST=127.0.0.1
    DB_PORT=3306
    
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USE_TLS=1
    EMAIL_HOST_USER=yourgmail@gmail.com
    EMAIL_HOST_PASSWORD=your-app-password
    DEFAULT_FROM_EMAIL=yourgmail@gmail.com
5)  Setup MySQL Database
    CREATE DATABASE job_portal CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    CREATE USER 'jobuser'@'localhost' IDENTIFIED BY 'jobpass';
    GRANT ALL PRIVILEGES ON job_portal.* TO 'jobuser'@'localhost';
    FLUSH PRIVILEGES;
6)  Apply Migrations
    python manage.py migrate
7)  Create Superuser
    python manage.py createsuperuser
8)  Run The Project
    python manage.py runserver

**Project Structure**
jobportal/
│
├── accounts/        → Authentication, signup, login, roles
├── core/            → Dashboards & homepage
├── jobs/            → Job posting, applications, workflow
│
├── templates/       → All HTML templates
├── static/css/      → UI styling (main.css)
│
└── .env             

**Testing Workflow (Expected User Journey)**

Visit Home                    -   Shows job list
Click Apply (not logged in)   -   Redirects to signup
Signup as Applicant           -   Email sent → role dashboard
Signup as Employer            -   Can post jobs
Applicant applies             -   Employer receives notification
Employer updates status       -   Applicant receives email update

**Screenshots**

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/6b79c276-d317-49c7-af69-cf26cc2d62a0" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/a69d61f3-f298-4cdb-bf16-6d7607ef68ae" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/3aac15a5-f5f4-4d8c-83a4-09d344901ed0" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/d46445ff-4867-447d-b600-e703e7a59a0d" />

<img width="2940" height="1912" alt="image" src="https://github.com/user-attachments/assets/6afc2197-d149-4894-a11c-67eefdf01233" />




**Developed By - Venkata Sasidhar Guturi**




