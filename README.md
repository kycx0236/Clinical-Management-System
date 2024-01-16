# Clinical Management System
## Project Description

This project is a comprehensive healthcare management system designed for small and medium-sized clinics. It aims to streamline the workflow of receptionists, doctors, and medical technicians, providing a seamless experience for patients.

From scheduling appointments with doctors to receiving lab results from medical technicians, this system offers a unified platform that gives insights to doctors for effective prescription. It enhances efficiency, reduces manual errors, and improves patient care by providing real-time access to patient records and test results.

### Key features include:
- Appointment scheduling with doctors
- Lab result retrieval
- Real-time patient record access
- Prescription assistance based on lab results and patient history

### Type of user account availabe:
- Admin 
- Receptionist
- Doctor
- Medtech

---
## Getting Started
Follow these steps to set up and run the project on your local machine:

1) Clone the repository

    ```bash
    git clone git@bitbucket.org:clinical-ms/clinical-management-system.git
    ```

2) Change the directory to the app

    ```bash
    cd /clinical-management-system 
    ```

3) Install dependencies

    ```bash
    pipenv install 
    ```
4) Create a .env file containing the keys/values of the required variables: (Database, Mailtrap, Cloudinary)

    ```
    DB_HOST=localhost
    DB_PORT=3306
    DB_NAME=web_cms_database
    DB_USERNAME=
    DB_PASSWORD=
    SECRET_KEY=

    PIPENV_VENV_IN_PROJECT=1
    FLASK_APP=app
    FLASK_DEBUG=true
    FLASK_RUN_PORT=5000

    MAIL_SERVER=
    MAIL_PORT=
    MAIL_USERNAME=
    MAIL_PASSWORD=

    cloud_name=
    api_key=
    api_secret=
    ```

5) Create database for the website

    * Run all the queries in the `cms.sql`
    * This will create all database schema needed for the website to run  

6) Seed the database with default accounts (which you can edit or remove using the admin account) 

    ```bash
    python seed_data.py 
    ```

    > After seeding the database, the password will be sent to the emails in which by using mailtrap you will receive the passwords   

    | Default Username  |
    | ----------------- |
    | admin1            | 
    | doctor1           | 
    | medtech1          |
    | receptionist1     |

7) Run the flask application
    ```bash
    flask run
    ```

---
## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

> For major changes, please open an issue first to discuss what you would like to change.

> Please make sure to update tests as appropriate.

---
## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
