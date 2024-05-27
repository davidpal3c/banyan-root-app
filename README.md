# Event Hub

## Introduction

Event Hub is a comprehensive event management application designed to streamline the process of creating, managing, and attending events. Built with Django, a powerful Python web framework, Event Hub offers robust features such as user authentication, event creation and management, venue details, and more. This application is ideal for organizations looking to centralize their event planning and execution processes.

## Features

- **User Authentication:** Securely manage user accounts with registration, login, and logout capabilities.
- **Admin Dashboard:** Superusers can approve events, ensuring quality control over what gets published.
- **Event Management:** Users can create, update, and delete events, including setting dates, times, and descriptions.
- **Venue Details:** Store detailed information about venues, including addresses, contact information, and images.
- **Attendance Tracking:** Keep track of who will be attending each event.
- **Search Functionality:** Easily find events and venues through keyword searches.
- **Export Options:** Download venue lists in PDF, CSV, or plain text formats.
- **Responsive Design:** Works seamlessly across desktop and mobile devices.

## Installation

To install Event Hub locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/davidpal3c/eventhub-mgmt-app.git
   ```

2. Navigate to the cloned directory:
   ```
   cd Event-Hub
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Ensure PostgreSQL is installed and running.
   - Create a new database and user for the application.
   - Update the `DATABASES` section in `settings.py` with your database credentials.

5. Apply migrations:
   ```
   python manage.py migrate
   ```

6. Collect static files:
   ```
   python manage.py collectstatic
   ```

7. Run the server:
   ```
   python manage.py runserver
   ```

## Tools & Technologies

- **Backend:** Django
- **Database:** PostgreSQL
- **Authentication:** Django's built-in authentication system
- **Static Files Handling:** Django's static files support
- **PDF Generation:** ReportLab library
- **CSV Export:** Python's csv module
- **Email Sending:** Django's email sending utilities

## Usage

Once installed, navigate to `http://localhost:8000` in your browser to access the Event Hub application. Use the admin panel to manage events and venues, or sign up as a regular user to create and attend events.

## License

Event Hub is open-source software licensed under the MIT license.


Deployment
EventHub is deployed on Railway. Visit EventHub to explore the platform.

## Built With
Django - The web framework used
Bootstrap - Used for styling
ReportLab - For generating PDF reports
Pillow - Image processing library
Gunicorn - WSGI HTTP Server for UNIX
HTML/CSS/Javascript - front-end languages


## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request
License
Distributed under the MIT License. See LICENSE for more information.

Contact
Your Name - davidpal3c@gmail.com

Project Link: https://github.com/davidpal3c/eventhub-mgmt-app.git