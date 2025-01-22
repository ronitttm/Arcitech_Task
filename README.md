# CMS API Project

This project is a Content Management System (CMS) API built with Django and Django REST Framework. The API allows authors to register, login, create, edit, view, and delete content. Admin users have additional privileges to manage all content.

## Requirements

- Python
- Django
- Django REST Framework
- Django REST Framework Token Authentication
- Postman (for testing API endpoints)

## Installation

1. **Clone the Repository**

  git clone https://github.com/ronitttm/Arcitech_Task.git
  cd Arcitech_Task

2. **Create a Virtual Environment**

  python -m venv venv
  venv\Scripts\activate
  
3. **Install Dependencies**
   
  pip install -r requirements.txt

4. **Run Database Migrations**

  python manage.py makemigrations
  python manage.py migrate 

5. **Seed Admin Users**

  python manage.py seed_admin

## Usage:
1. **Run the Development Server**
  python manage.py runserver

2. **Access the Admin Interface:**

  Open your browser and navigate to http://127.0.0.1:8000/admin/. Log in with your superuser credentials.

3. **API Endpoints:**

**Register Author: POST http://127.0.0.1:8000/api/register/**
  ![image](https://github.com/user-attachments/assets/cca6246f-fbef-4c6d-8058-59b6eae21490)
  ![image](https://github.com/user-attachments/assets/de3d6069-8adf-4333-b9cf-9c89ad6e77e4)


**Login Author and Admin: POST http://127.0.0.1:8000/api/login/ ## Has to be done from POSTMAN**
  ![image](https://github.com/user-attachments/assets/701e209d-0f89-4e48-ac51-1d8d4776fca5)

**The AUTH token is used for login purposes**

**Create Content: POST http://127.0.0.1:8000/api/content/?token=YOUR_AUTH_TOKEN**
  ![image](https://github.com/user-attachments/assets/ff8f0bed-a05e-4178-ab3f-cd72e6191536)

**To add content, Fill the form anf click on POST**

**View Content: GET http://127.0.0.1:8000/api/content/?token=YOUR_AUTH_TOKEN**
  ![image](https://github.com/user-attachments/assets/ff8f0bed-a05e-4178-ab3f-cd72e6191536)

**All Author content can be viewed**

**Edit Content: PUT http://127.0.0.1:8000/api/content/<CONTENT_ID>/?token=YOUR_AUTH_TOKEN**
  ![image](https://github.com/user-attachments/assets/558c1068-a613-422a-a03b-d615cf42940d)

**Content ID has to inputted. The below form can be updated to edit content and clicking PUT**


**Delete Content: DELETE http://127.0.0.1:8000/api/content/CONTENT_ID/?token=YOUR_AUTH_TOKEN**
  ![image](https://github.com/user-attachments/assets/185bbe38-30fb-428f-8ca5-f4e2069939b9)

**Content ID has to inputted. The DELETE icon deletes the content of particular content ID.**


**Search Content: GET http://127.0.0.1:8000/api/content/search/?query=SEARCH_TERM&token=YOUR_AUTH_TOKEN**
  ![image](https://github.com/user-attachments/assets/b591b75d-14c2-4ba7-b014-26df5bed59ff)

**Search your content based on the Keywords added in the search query**


**Admin View All Content: GET http://127.0.0.1:8000/api/admin/content/CONTENT_ID/?token=ADMIN_AUTH_TOKEN**
![image](https://github.com/user-attachments/assets/3b905ebc-d6fd-46d0-b190-ac1941eb788c)

**Admin Edit Content: PUT http://127.0.0.1:8000/api/admin/content/CONTENT_ID/?token=ADMIN_AUTH_TOKEN**
![image](https://github.com/user-attachments/assets/3b905ebc-d6fd-46d0-b190-ac1941eb788c)

**Admin Delete Content: DELETE http://127.0.0.1:8000/api/admin/content/CONTENT_ID/?token=ADMIN_AUTH_TOKEN**
![image](https://github.com/user-attachments/assets/3b905ebc-d6fd-46d0-b190-ac1941eb788c)
