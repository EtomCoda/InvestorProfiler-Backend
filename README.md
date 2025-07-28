# Investment Guide

This project is a Django-based backend system that determines a user's investment risk profile and suggests a corresponding portfolio of investment funds. The system is divided into two main applications: `core` and `funds`.

## Core Application

The `core` application is responsible for calculating a user's risk profile based on their answers to a 7-question survey. The risk profile is determined by two scores: a **time score** and a **tolerance score**. These scores are calculated from the user's responses and then mapped to a predefined risk profile.

### Features

- 7-question investment risk questionnaire
- Score aggregation (time-based and tolerance-based)
- Dynamic risk profile assignment using database mappings
- REST API endpoint for submitting and calculating the profile
- Simple HTML frontend for testing and user response submission

### How Risk Is Calculated

- **Time Score:** Sum of scores from Question 1 and 2
- **Tolerance Score:** Sum of scores from Questions 3–7
- Scores are matched against the `ProfileMapping` model to determine the profile

## Funds Application

The `funds` application manages the investment funds and their categories. Each risk profile is associated with a set of fund categories, and each category contains a list of funds. The funds are ranked on a 1-5 stars scale using the Morningstar ranking system logic.

### Features

- Fund categorization based on risk profiles
- Fund ranking using the Morningstar rating system
- REST API endpoint to retrieve fund information based on risk profiles

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite
- **Frontend:** Basic HTML & CSS (with vanilla JS for form submission)

## Installation

1.  **Clone the repo**

    ```bash
    git clone https://github.com/EtomCoda/risk-profile-questionnaire.git
    cd risk-profile-questionnaire
    ```

2.  **Set up a virtual environment**

    ```bash
    python -m venv env
    source env/bin/activate  # on Windows: env\Scripts\activate
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run migrations**

    ```bash
    python manage.py migrate
    ```

5.  **Seed the database**

    To populate the database with initial data, run the following commands:

    ```bash
    python manage.py seed_questions
    python manage.py seed_risk_profiles
    python manage.py seed_risk_profile_mapping
    ```

6.  **Start the server**

    ```bash
    python manage.py runserver
    ```
    
---

##  API Documentation

Check out the [Full API Docs](./docs/postman/api.md)
---

## Testing via Frontend Form

Open `risk_form.html` in a browser to test the form submission. It includes:

*   Radio inputs for Questions 1–4, 6–7
*   Checkboxes for multi-answer Question 5
*   JS that submits to `/core/risk-profile-form/submit/` and displays the profile result

## License

Unlicensed © 2025 EtomCoda