# COVID-19 Patient Tracker

> A platform that enables HR Teams and Medical Teams to keep track of patients and their immediate contacts. To be used by organizations and factories trying to work through the pandemic.



## Features

* Email Verification on creating a new account.

* Streamlined Onboarding form for new patients.

  ![Onboarding Process](../assets/Assets/README/onboarding.png?raw=True)

* Streamlined Daily Update form for patient tracking.

  ![Daily Update Form](../assets/Assets/README/dailyUpdate.png?raw=True)

* Detail view per patient.

  ![Patient Detail View](../assets/Assets/README/detailview.png?raw=True)

* Symptom trends view for doctors to track patient health.

  ![Symptom Trends](../assets/Assets/README/symptomtrendview.png?raw=True)

* Separate Doctor and HR comments per patient.

  ![HR Comments](../assets/Assets/README/hrcommentview.png?raw=True)

* Automatic categorization of patient criticality based on symptoms.

* Records primary contacts of every patient as well.

---


## Setup Instructions

* Clone the repository.
* Set your virtual environment up.
* Rename `env-template.txt` to `.env` and fill in the details. You only need to fill the `DJANGO_SECRET_KEY`, `LOGIN_REDIRECT_URL` and `LOGIN_URL` to get started.
* Activate your virtual environment and run `pip install -r requirements.txt` .
* Make the migrations and run them using: `python manage.py makemigrations` and then `python manage.py migrate`.
* Run the tests using `python manage.py test`.
* Run the development server using `python manage.py runserver`.
* Navigate to `localhost:8000/docs` on your browser for the documentation.



---

## Roadmap

* Dockerize the application

* Host it on a more production ready platform.

  

