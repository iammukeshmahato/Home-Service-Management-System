# Home Service Management System

## Table of Contents

-  [Introduction](#introduction)
-  [Technologies](#technologies)
-  [Installation](#installation)
-  [Contributing](#contributing)
-  [Author](#author)

## Introduction

The Home Service Management System is a web application designed to streamline and simplify household management task. Scheduling regular maintenance appointment with service man to fix your problems, this system provides a centralized platform for homeowners to organize and manage all aspects of home maintenance.

## Technologies

-  HTML
-  CSS
-  JavaScript
-  Bootstrap
-  Django
-  MySQL

## Installation

1. Clone the repository
2. Create the virtual environment

```bash
python -m venv venv
```

3. Activate the virtual environment

```bash
source venv/bin/activate
```

4. Run the following command to install the required packages

```bash
pip install -r requirements.txt
```

5. Run the following command to start mysql the server

```bash
mysql.server start
```

_Note:_ If your are using XAMPP, start the Apache and MySQL server and change the database settings in the `settings.py` file

6. Create a `Home_Service` database in MySQL

7. Run the following command to create the tables in the database

```bash
env python manage.py makemigrations
env python manage.py migrate
```

8. Create a superuser to access the admin panel

```bash
env python manage.py createsuperuser
```

Note: You will be prompted to enter the email and password and manymore

9. Run the following command to start the server

```bash
env python manage.py runserver
```

10. Open the browser and go to the following link

```bash
http://127.0.0.1:8000/
```

## Contributing

-  Fork the repo [Home-Service-Management-System](https://github.com/iammukeshmahato/Home-Service-Management-System)
-  Commit your changes
-  Create pull request mentioning comment regarding your changes

## Author

-  [Mukesh Mahato](https://github.com/iammukeshmahato)
