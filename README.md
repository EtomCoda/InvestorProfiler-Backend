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

## Testing

This project includes a suite of tests to ensure the reliability of the `core` and `funds` applications.

### Core Application Tests

The tests for the `core` application are located in the `core/test/` directory and cover the following areas:

- **`test_core_utils.py`**: This module tests the business logic of the risk profiling system. It ensures that the `calculate_risk_profile` function behaves as expected in various scenarios, including:
  - Successful risk profile calculation.
  - Handling of `ValueError` when a question is missed.
  - Detection of a `ShortTimeHorizonError` for users with a short investment timeline.
  - Graceful failure when no risk profile matches the user's scores.

- **`test_core_views.py`**: This module tests the API endpoints of the `core` application. It verifies that the views handle requests correctly, including:
  - Successful submission of the risk profile form.
  - Proper handling of invalid HTTP methods.
  - Validation of request data to ensure all questions are answered.
  - Correct error responses for short time horizons or when no matching profile is found.

- **`test_profile_matching.py`**: This module validates the accuracy of the `ProfileMapping` model. It confirms that the predefined score ranges correctly map to the appropriate risk profiles, ensuring that users are assigned the correct investment profile based on their scores.

### Funds Application Tests

The tests for the `funds` application are located in the `funds/tests/` directory. These tests ensure the proper functioning of the fund management system, including:

- **`tests.py`**: This module covers the following functionalities:
  - **Model Creation**: Verifies that `Fund` and `FundCategory` objects are created correctly.
  - **Relationships**: Ensures that the relationship between funds and their categories is correctly established.
  - **API Endpoint**: Tests the `get_fund_profile` view to confirm that it returns the correct fund profiles and handles various scenarios, such as invalid request methods or cases where no data is available.

To run the tests, you can use the following command:

```bash
python manage.py test
```

---

## Testing via Frontend Form

Open `risk_form.html` in a browser to test the form submission. It includes:

*   Radio inputs for Questions 1–4, 6–7
*   Checkboxes for multi-answer Question 5
*   JS that submits to `/core/risk-profile-form/submit/` and displays the profile result

## License

Unlicensed © 2025 EtomCoda