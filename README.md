# FastAPI Application

This project is a FastAPI application providing a robust backend auth API. It's designed to be easily deployable, testable, and maintainable.

## Getting Started

These instructions will get your copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.8+
- pip (Python package installer)
- Docker (optional, for containerized deployment)
- Postgres SQL (Primary Database)
- Sqlite3 (TestDB)

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/solomonmarvel97/python-auth-service
    cd bportal-auth-service
    ```

2. **Set up a Virtual Environment (Optional but Recommended)**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

- **Using Uvicorn:**

    ```bash
    uvicorn app.main:app --reload
    ```

    The application will be available at `http://127.0.0.1:8000`. The `--reload` flag enables auto-reloading of the server on code changes.

- **Using Docker:**

    ```bash
    docker build -t fastapi-app .
    docker run -p 8080:8080 fastapi-app
    ```

    This will build and run the FastAPI application in a Docker container.

### Testing

To run tests using Pytest, execute the following command:

```bash
pytest
```

This will discover and run all test cases defined in your project.

## API Documentation

Once the application is running, you can access the Swagger UI documentation at `http://127.0.0.1:8080/docs`.


Configure github action for build and deployment