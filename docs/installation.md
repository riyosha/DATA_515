### Installation Guide

## Requirements
Before you begin, ensure you have the following installed:

- **Docker**: Install from the official website: [Docker](https://www.docker.com/)
- **Make**: Usually pre-installed on macOS and Linux; Windows users may need to install it

## Installation Steps

### 1. Clone the Repository (using SSH)
```sh
git clone git@github.com:riyosha/DATA_515.git
cd DATA_515
```

### 2. Adding Dependencies

#### Backend (Python)
- To add new Python libraries, modify the Conda environment file:
  `backend/environment.yml`
- After updating the file, rebuild the Docker containers (see step 3).

#### Frontend (React)
- To add new JavaScript dependencies, modify:  
  `frontend/package.json`
- After updating the file, rebuild the Docker containers.

### 3. Running the Application
First ensure that you have a `.env` file at the root of the project to store secrets.

To start both the backend and frontend, run:
```sh
make build  # Build containers (first time or after dependency changes)
make up     # Start containers in detached mode
```

These commands will:
- Build and start the **backend** and **frontend** as separate containers
- Automatically install dependencies based on `environment.yml` and `package.json` respectively

Once running, you can access:
- **Frontend**: `http://localhost:5173`  
- **Backend API**: `http://localhost:5515`

To stop the application:
```sh
make down
```

### 4. Viewing Logs
To see real-time logs from both containers:
```sh
make logs
```

## Running Test Suites

### Frontend Tests
To run frontend unit tests:
```sh
make test-frontend
```

### Backend Tests
To run backend tests using `unittest`:
```sh
make test-backend
```

### All Tests
To run both frontend and backend tests:
```sh
make test
```

## Code Coverage

### Frontend Coverage
To run frontend tests with coverage reporting:
```sh
make coverage-frontend
```

### Backend Coverage
To run backend tests with coverage tracking:
```sh
make coverage-backend
```

To generate and view the coverage report:
```sh
make coverage-backend-report
```

### All Coverage
To run all tests with coverage:
```sh
make coverage
```

## Other Useful Commands

For a complete list of available commands:
```sh
make help
```

Additional useful commands:
- `make shell-frontend` - Open a shell in the frontend container
- `make shell-backend` - Open a shell in the backend container
- `make lint` - Run linting on both frontend and backend code
```

You can also completely rebuild the containers if needed:
```sh
make rebuild
```