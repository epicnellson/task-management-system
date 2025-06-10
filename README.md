# Task Management System

A full-stack web application for managing tasks, built with Flask and PostgreSQL.

## Features

- User Authentication (Register, Login, Logout)
- Create, Read, Update, Delete (CRUD) operations for tasks
- Task Categories
- Priority Levels
- Deadlines
- User Dashboard
- Responsive Design
- File Attachments
- Email Notifications
- Activity Logging
- Task Templates
- Export Functionality

## Tech Stack

- Backend: Python (Flask)
- Database: PostgreSQL
- Frontend: HTML, CSS, JavaScript
- Authentication: Flask-Login
- Forms: Flask-WTF
- Database ORM: SQLAlchemy
- Email: Flask-Mail
- Caching: Flask-Caching
- Rate Limiting: Flask-Limiter

## Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd task-management-system
   ```

2. **Set up PostgreSQL**
   ```bash
   # Create a new PostgreSQL database
   createdb taskmanager
   
   # Or using psql
   psql -U postgres
   CREATE DATABASE taskmanager;
   ```

3. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Environment Setup**
   - Copy `.env.example` to `.env`
   - Update the following variables in `.env`:
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/taskmanager
     SECRET_KEY=your-secret-key
     MAIL_USERNAME=your-email
     MAIL_PASSWORD=your-password
     ```

6. **Database Migration**
   ```bash
   # Initialize migrations
   flask db init
   
   # Create initial migration
   flask db migrate -m "Initial migration"
   
   # Apply migrations
   flask db upgrade
   ```

7. **Run the application**
   ```bash
   flask run
   ```

## Project Structure

```
taskmanager/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── user.py
│   │   ├── task.py
│   │   ├── category.py
│   │   ├── comment.py
│   │   ├── notification.py
│   │   ├── attachment.py
│   │   ├── template.py
│   │   └── activity.py
│   ├── routes/
│   ├── static/
│   ├── templates/
│   └── utils/
├── migrations/
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
└── run.py
```

## Database Schema

The application uses the following main tables:
- Users
- Tasks
- Categories
- Comments
- Notifications
- Attachments
- Templates
- Activity Logs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository. 