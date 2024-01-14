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

4) Create database for the website

    * Run all the queries in the `cms.sql` this will create default accounts for each user, and default schedules for the appointments of the doctor 

5) Run the flask application
    ```bash
    flask run
    ```
---
## Contributing
If you would like to contribute to this project, please fork the repository and submit a pull request.

For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

---
## License
This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License.
