Flask Blog with User Authentication

This is a Flask-based web application for managing a blog with user authentication, administrative privileges, and comment functionality. It allows users to register, log in, create and edit posts, and leave comments on posts. The application uses a variety of Flask extensions to enhance functionality, including CKEditor for rich text editing, SQLAlchemy for database management, and Flask-Login for user session management.

## Features

- **User Authentication**: Users can register, log in, and log out securely.
- **Admin Privileges**: Admin users can create, edit, and delete blog posts.
- **Post Comments**: Registered users can comment on blog posts.
- **Gravatar Integration**: Display user avatars with Gravatar.
- **Rich Text Editing**: Use CKEditor for creating and editing blog posts.
- **Responsive Design**: Built with Bootstrap for a modern, responsive user interface.
- **Secure Passwords**: Passwords are hashed using Werkzeug's security module.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/flask-blog.git
    cd flask-blog
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages from `requirements.txt`**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python
    >>> from main import db
    >>> db.create_all()
    >>> exit()
    ```

5. **Run the application**:
    ```bash
    flask run
    ```

6. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5002/`.

## Usage

- **Home Page**: Displays all blog posts, with options for users to read more or leave comments.
- **Register**: Create a new user account to access additional features like commenting and posting.
- **Login**: Log in to your account to access the full features of the site.
- **Admin**: The admin user has special privileges to add, edit, and delete blog posts.
- **Add/Edit Posts**: Admins can create and update posts with an easy-to-use interface.

- Feel free to fork this repository, create a new branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.
