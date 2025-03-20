# Letterboxd Movie Review Analyzer & Roast Generator

![GitHub Actions Workflow](https://github.com/riyosha/DATA_515/actions/workflows/build_test.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/riyosha/DATA_515/badge.svg)
[![code style: prettier](https://img.shields.io/badge/code%20style-prettier-F7B93E.svg)](https://github.com/prettier/prettier)

## Introduction  

The **Letterboxd Movie Analyzer & Roast Generator** is an AI-powered tool designed to help users quickly evaluate movies based on **Letterboxd reviews** and generate **personalized roasts** of their Letterboxd profile data.  

### **Key Features**  
- **Movie Analysis**: Generates a **sentiment-based summary** of real-time Letterboxd reviews.  
- **Aspect-Based Sentiment Analysis**: Extracts **key movie aspects** such as acting, direction, cinematography, and humor.
- **Vibe Checker**: Compares a Letterboxd user's reviews and a movie's reviews to analyze what a user might like/dislike about the movie.
- **User Roast Generator**: Scrapes **Letterboxd profile data** to deliver a **hilarious roast** based on viewing habits and ratings.  

---

## **Preview**  
![Video Preview](docs/assets/video_preview.gif)


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

- [Dependencies](#dependencies) 
- [Introduction](#introduction)  
- [User Profiles](#user-profiles)  
- [Tasks of Interest](#tasks-of-interest)  
- [Repository Structure](#repository-structure)  
- [Installation](#installation)
- [Generating Gemini API Keys](#generating-api-keys)
- [Running the Project](#running-the-project) 
- [Environment, Tests and Coverage](#environment)
- [Packaging and Distribution](#distribution)  
- [Data](#data)  
- [Application](#application)  
- [Examples](#examples)  
- [Disclaimer](#disclaimer)  

---

## **Repository Structure**  
```plaintext
├── LICENSE
├── Makefile
├── README.md
├── backend
│   ├── Dockerfile
│   ├── MANIFEST.in
│   ├── dist
│   │   ├── letterboxd_analyzer-1.0.0-py3-none-any.whl
│   │   └── letterboxd_analyzer-1.0.0.tar.gz
│   ├── environment.yml
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── src
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   └── app.cpython-313.pyc
│   │   ├── app.py
│   │   └── helpers
│   │       ├── __pycache__
│   │       │   ├── letterboxd_analyzers.cpython-313.pyc
│   │       │   ├── roast_generator.cpython-313.pyc
│   │       │   ├── scrapers.cpython-313.pyc
│   │       │   └── scrapers_roast.cpython-313.pyc
│   │       ├── letterboxd_analyzers.py
│   │       ├── roast_generator.py
│   │       ├── scrapers.py
│   │       └── scrapers_roast.py
│   └── tests
│       ├── __init__.py
│       ├── helpers
│       │   ├── __init__.py
│       │   ├── test_letterboxd_analyzers.py
│       │   └── test_scrapers.py
│       ├── test_app.py
│       ├── test_roast_generator.py
│       └── test_scrapers_roast.py
├── docker-compose.dev.yml
├── docker-compose.yml
├── docs
│   ├── Functional_Specification.md
│   ├── assets
│   │   ├── Letterboxd review Analyzer.pdf
│   │   ├── Letterboxd review Analyzer.pptx
│   │   ├── demo1.mp4
│   │   └── video_preview.gif
│   ├── component_specification.md
│   ├── milestones.md
│   ├── technology_review
│   │   ├── demo.md
│   │   └── libraries_overview.md
│   └── video_preview.gif
├── example
│   └── demo1.md
└── frontend
    ├── Dockerfile
    ├── README.md
    ├── eslint.config.js
    ├── index.html
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── public
    │   └── videos
    │       └── go-to-the-lobby.mp4
    ├── src
    │   ├── Landing.css
    │   ├── Landing.jsx
    │   ├── MovieReview
    │   │   ├── AspectGraph.jsx
    │   │   ├── Error.jsx
    │   │   ├── Movie.css
    │   │   ├── Movie.jsx
    │   │   ├── MovieInfo.css
    │   │   ├── MovieInfo.jsx
    │   │   ├── VibeCheck.css
    │   │   ├── VibeCheck.jsx
    │   │   ├── Video.css
    │   │   ├── Video.jsx
    │   │   └── __tests__
    │   │       ├── AspectGraph.test.jsx
    │   │       ├── Error.test.jsx
    │   │       ├── Movie.test.jsx
    │   │       ├── MovieInfo.test.jsx
    │   │       ├── VibeCheck.test.jsx
    │   │       └── Video.test.jsx
    │   ├── Roast
    │   │   ├── Roast.css
    │   │   ├── Roast.jsx
    │   │   └── __tests__
    │   │       └── Roast.test.jsx
    │   ├── __tests__
    │   │   ├── Landing.test.jsx
    │   │   └── main.test.jsx
    │   ├── index.css
    │   ├── main.jsx
    │   └── setupTests.js
    └── vite.config.js
```

---
## **Dependencies**

Please have the latest versions of Docker and Git installed on your local system.

Docker: https://www.docker.com/

Git: https://git-scm.com/downloads

Make: The GNU command - if on windows may need to install a Windows Subsystem for Linux

## **Installation** 

To clone this repository, run:  

```bash
 git clone https://github.com/riyosha/letterboxd-review-analyzer.git
```
---

For a list of all available make commands, run:

```bash
make help
```
This will display a list of preconfigured `Makefile` commands for managing the project.
For the first time initialization of the project, run:
```bash
make init
```
---
## **Generating API Keys**

Please follow this link to generate 6 Gemini API keys: https://ai.google.dev/gemini-api/docs/api-key 

Update backend/.env with your actual API keys.

---
## **Running the Project**  

Run these commands in order - 

```bash
open -a Docker
make build
make dev
```
On a new terminal run make ps to ensure both the backend and frontend docker containers are running

Use the frontend link to launch the website! 
`http://localhost:5173`

---

## **Environment, Tests and Coverage**  

To individually setup environments and run tests for frontend and backend, please refer to commands listed by `make help`.

---

## **Packaging and Distribution**

We only setup packaging and distribution for the Python backend server portion of our application.
To build the backend and generate a distributable tarbell file and wheel file all you need to do is run `make build-backend-package`

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

---

## **Demo**  
[![Watch the video](https://img.youtube.com/vi/h8JnYarm5BA/0.jpg)](https://www.youtube.com/watch?v=h8JnYarm5BA)


---

## **Disclaimer**  

This project is a **fan-based tool** that scrapes publicly available information from **Letterboxd** for personal use. It is **not affiliated with or endorsed by Letterboxd** in any way.  

Use this tool responsibly and respect **Letterboxd's terms of service**.  

---
