# User Management Microservice

A lightweight and scalable **User Management Microservice** built with **Flask**, **SQLAlchemy**, and **Flask-JWT-Extended**. This microservice provides RESTful APIs for user registration, authentication, and user management.

---

## Features

- **User Registration**: Create new users with a username, email, and password.
- **User Authentication**: Secure login using JSON Web Tokens (JWT).
- **User Management**: Fetch, update, and delete user details.
- **Protected Routes**: Access control using JWT authentication.
- **Database Integration**: Uses SQLAlchemy for database operations (supports SQLite, PostgreSQL, MySQL, etc.).
- **Error Handling**: Proper error responses for invalid requests.
- **Logging**: Integrated logging for debugging and monitoring.

---

## Technologies Used

- **Python**: Core programming language.
- **Flask**: Lightweight web framework for building APIs.
- **SQLAlchemy**: ORM for database interactions.
- **Flask-JWT-Extended**: JWT-based authentication.
- **Werkzeug**: Password hashing and security utilities.
- **SQLite**: Default database for development (can be replaced with other databases).

---

## Getting Started

### Prerequisites

- Python 3.7+
- pip (Python package manager)

---

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/henrymbuguak/UserVault.git
   cd user-management-microservice
   ```

1. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

1. **Run the Application**:
   ```bash
   python run.py
   ```
   The microservice will start at `http://127.0.0.1:5000`.

---

## API Endpoints

### **Authentication**
- **Login**:
  - **POST** `/api/login`
  - Request Body:
    ```json
    {
      "username": "testuser",
      "password": "testpass"
    }
    ```
  - Response:
    ```json
    {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

### **User Management**
- **Create User**:
  - **POST** `/api/users`
  - Request Body:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "newpass"
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "username": "newuser",
      "email": "newuser@example.com"
    }
    ```

- **Get All Users**:
  - **GET** `/api/users`
  - Response:
    ```json
    [
      {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
      }
    ]
    ```

- **Get User by ID**:
  - **GET** `/api/users/<id>`
  - Response:
    ```json
    {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    }
    ```

- **Update User**:
  - **PUT** `/api/users/<id>`
  - Request Body:
    ```json
    {
      "username": "updateduser",
      "email": "updated@example.com"
    }
    ```
  - Response:
    ```json
    {
      "id": 1,
      "username": "updateduser",
      "email": "updated@example.com"
    }
    ```

- **Delete User**:
  - **DELETE** `/api/users/<id>`
  - Response:
    ```json
    {
      "message": "User deleted successfully"
    }
    ```

---


## Example cURL Commands

### **1. Create a New User**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "email": "test@example.com", "password": "testpass"}' http://127.0.0.1:5000/api/users
```

### **2. Log in to Get a JWT Token**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"username": "testuser", "password": "testpass"}' http://127.0.0.1:5000/api/login
```

### **3. Fetch All Users (Protected Route)**
Replace `<your-access-token>` with the token received from the login response.
```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users
```

### **4. Fetch a Specific User by ID**
```bash
curl -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

### **5. Update a User**
```bash
curl -X PUT -H "Authorization: Bearer <your-access-token>" -H "Content-Type: application/json" -d '{"username": "updateduser", "email": "updated@example.com"}' http://127.0.0.1:5000/api/users/1
```

### **6. Delete a User**
```bash
curl -X DELETE -H "Authorization: Bearer <your-access-token>" http://127.0.0.1:5000/api/users/1
```

---

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: Database connection URL (default: `sqlite:///app.db`).
- `JWT_SECRET_KEY`: Secret key for JWT token generation (default: `your-secret-key`).

To set environment variables, create a `.env` file in the root directory:
```env
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your-secret-key
```

---

## Logging

Logs are stored in the `logs/` directory. The log file (`microservice.log`) contains information about requests, errors, and other events.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## Acknowledgments

- Flask and SQLAlchemy for providing a robust framework for building microservices.
- Flask-JWT-Extended for secure authentication.
- The Python community for continuous support and resources.

---

## Contact

For questions or feedback, please open an issue or contact the maintainer:
- **Henry Mbugua**
- **LinkedIn**: [Henry Mbugua](https://www.linkedin.com/in/henrymbugua/)
- **GitHub**: [henrymbuguak](https://github.com/henrymbuguak)

---

Enjoy building with the User Management Microservice! 🚀
