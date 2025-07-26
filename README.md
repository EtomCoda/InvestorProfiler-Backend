


#  Investment Guide

This project is a Django-based backend system that calculates a user's investment **risk profile** based on their responses to a seven-question form. 
It maps the user's choices to a predefined risk appetite type using a custom scoring system, and suggests to the user percentages to invest in certain fund categories. 
These fund categories each possess funds that are ranked on a 1-5 stars scale using the Morningstar ranking system logic 

##  Features

- 7-question investment risk questionnaire
- Score aggregation (time-based and tolerance-based)
- Dynamic risk profile assignment using database mappings
- REST API endpoint for submitting and calculating the profile
- Simple HTML frontend for testing and user response submission

---

##  Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** SQLite 
- **Frontend:** Basic HTML & CSS (with vanilla JS for form submission)

---

##  Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/EtomCoda/risk-profile-questionnaire.git
   cd risk-profile-questionnaire


2. **Set up a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate  # on Windows: env\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the server**

   ```bash
   python manage.py runserver
   ```

---

##  API Documentation

Check out the [Full API Docs](./docs/postman/api.md)

---

##  Testing via Frontend Form

Open [`risk_form.html`](./risk_form.html) in a browser to test the form submission. It includes:

* Radio inputs for Questions 1–4, 6–7
* Checkboxes for multi-answer Question 5
* JS that submits to `/core/risk-profile/submit` and displays the profile result

---



##  License

Unlicenced © 2025 EtomCoda

---


