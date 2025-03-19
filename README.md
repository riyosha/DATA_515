# Letterboxd Movie Analyzer & Roast Generator

![GitHub Actions Workflow](https://github.com/riyosha/DATA_515/actions/workflows/build_test.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/riyosha/DATA_515/badge.svg)

# Letterboxd Movie Analyzer & Roast Generator

![Build-Test Workflow](https://github.com/your-repo/actions/workflows/build_test.yml/badge.svg)  
![Coverage Status](https://coveralls.io/repos/github/your-repo/badge.svg)  

## Introduction  

The **Letterboxd Movie Analyzer & Roast Generator** is an AI-powered tool designed to help users quickly evaluate movies based on **Letterboxd reviews** and generate **personalized roasts** of their Letterboxd profile data.  

### **Key Features**  
- **Movie Analysis**: Generates a **sentiment-based summary** of real-time Letterboxd reviews.  
- **Aspect-Based Sentiment Analysis**: Extracts **key movie aspects** such as acting, direction, cinematography, and humor.  
- **User Roast Generator**: Scrapes **Letterboxd profile data** to deliver a **hilarious roast** based on viewing habits and ratings.  

---

## **Public Website**  
TBD (if hosted)  

---

## **Team Members**  

| Name  | GitHub Profile |  
|--------|--------------|  
| Dyuti  | [GitHub](https://github.com/dyutivartak)  |  
| Edgar  | [GitHub](https://github.com/Edgineer)  |  
| Riyosha  | [GitHub](https://github.com/riyosha)  |  
| Saikiran  | [GitHub](https://github.com/asaikiranb)  |  

---

## **Table of Contents**  

- [Introduction](#introduction)  
- [User Profiles](#user-profiles)  
- [Tasks of Interest](#tasks-of-interest)  
- [Repository Structure](#repository-structure)  
- [Installation](#installation)  
- [Environment](#environment)  
- [Data](#data)  
- [Application](#application)  
- [Examples](#examples)  
- [Disclaimer](#disclaimer)  

---

## **Repository Structure**  
```plaintext
.
├── Makefile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── environment.yml
│   ├── src
│   │   ├── helpers
│   │   │   ├── letterboxd_analyzers.py
│   │   │   ├── roast_generator.py
│   │   │   ├── scrapers.py
│   │   │   ├── scrapers_roast.py
│   │   └── main.py
│   ├── tests
│   │   ├── helpers
│   │   │   ├── test_letterboxd_analyzers.py
│   │   │   ├── test_scrapers.py
│   │   ├── test_main.py
│   │   ├── test_roast_generator.py
│   │   ├── test_scrapers_roast.py
├── docker-compose.dev.yml
├── docker-compose.yml
├── docs
│   ├── Functional_Specification.md
│   ├── component_specification.md
│   ├── installation.md
│   ├── milestones.md
│   ├── technology_review
│   │   ├── demo.md
│   │   ├── libraries_overview.md
├── frontend
│   ├── Dockerfile
│   ├── README.md
│   ├── package.json
│   ├── src
│   │   ├── App.jsx
│   │   ├── MovieReview
│   │   │   ├── Error.jsx
│   │   │   ├── Movie.jsx
│   │   │   ├── MovieInfo.jsx
│   │   │   ├── Video.jsx
│   │   ├── Roast
│   │   │   ├── Roast.jsx
│   │   ├── main.jsx
└── vite.config.js
```

---

## **Installation**

For a list of all available commands, run:

```bash
make help
```

This will display a list of preconfigured Makefile commands for managing the project.

To set up the project, use the provided `Makefile` commands for a streamlined installation process.  

To clone this repository, run:  

```bash
 git clone https://github.com/riyosha/DATA_515.git
```

Ensure **Git** is installed before running this command.  

---

## **Environment**  

### **Setting Up Python Environment**

To set up the backend environment, run:  

```bash
make setup-backend  
```

To deactivate the environment, run:

```bash
make deactivate
```

To remove the environment, run:

```bash
make clean-backend
```

---

## **Running the Backend**

To start the backend, use:  

```bash
make run-backend  
```

---

## **Running the Frontend**

To start the frontend, use:  

```bash
make run-frontend  
```

---

## **Data Sources**  

This project **scrapes data live** from **Letterboxd** instead of relying on static datasets.  

### **1. Movie Reviews (Live Scraping)**  
- **Source:** `letterboxd.com/film/{movie-name}/`  
- **Scraped Fields:**  
  - Movie details (title, director, year, genres, synopsis)  
  - Reviews (rating, review text)  

### **2. User Profile Data (Live Scraping)**  
- **Source:** `letterboxd.com/{username}/stats/`  
- **Scraped Fields:**  
  - Most-watched genre, actor, director  
  - Total movies watched, total hours watched  
  - Longest streak of movie-watching days  
  - Rating patterns and binge-watching behavior  

---

## **Application**  

The web application is built with **Flask (backend) and React (frontend)**.  

### **Running Tests**

Use the following commands to run tests.  

### **Backend Tests**

To run backend tests, use:  
```bash
make test-backend  
```

### **Frontend Tests**

To run frontend tests, use:  
```bash
make test-frontend  
```

---

## **Examples**  

TBD (Add a link to a **demo video or screenshots** once available).  

---

## **Disclaimer**  

This project is a **fan-based tool** that scrapes publicly available information from **Letterboxd** for personal use. It is **not affiliated with or endorsed by Letterboxd** in any way.  

Use this tool responsibly and respect **Letterboxd's terms of service**.  

---
