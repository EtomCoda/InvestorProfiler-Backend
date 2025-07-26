


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

##  API Endpoint

### `POST /core/risk-profile/submit`

Submit selected options and receive a risk profile based on scoring logic.

**Request Body:**

```json
{
  "option_ids": [1, 4, 6, 8, 9, 10, 13, 16]
}
```

>  Make sure `option_ids` includes more than 7 responses:
>
> * Questions 1–4, 6–7: **one option each**
> * Question 5: **multiple options allowed**

**Response:**

```json
{
  "risk_profile": "Moderate"
   "description": "Invest in a mix of U.S. equities and bonds, with a smaller allocation to international equities. "
}
```

**Error Response:**

```json
{
  "error": "You must answer at least 7 or more questions."
}
```

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


