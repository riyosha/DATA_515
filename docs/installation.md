### Installation Guide

## Requirements
Before you begin, ensure you have the following installed:

- **Docker**: Install from the official website: [Docker](https://www.docker.com/)

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
To start both the backend and frontend, run:
```sh
docker-compose up --build
```
This command will:
- Build and start the **backend** and **frontend** as separate containers.
- Automatically install dependencies based on `environment.yml` and `package.json` respectively.

Once running, you can access:
- **Frontend**: `http://localhost:5173`  
- **Backend API**: `http://localhost:5515`

## Running Test Suites

### Frontend Tests
To run frontend unit tests:
```sh
docker exec -it frontend npm test
```

### Backend Tests
To run backend tests using `unittest`:
```sh
docker exec -it backend python -m unittest discover tests/
```
