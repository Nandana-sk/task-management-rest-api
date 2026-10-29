

\# Task Management REST API



\## Overview

A RESTful API built with Python and Flask to manage tasks. The application supports creating, retrieving, updating, and deleting tasks, with persistent storage using SQLite.



\## Features

\- Create tasks using POST requests

\- Retrieve all tasks using GET requests

\- Update tasks using PUT requests

\- Delete tasks using DELETE requests

\- Validate input and return appropriate HTTP status codes

\- Store tasks persistently in SQLite

\- Automated API testing with pytest



\## Technologies Used

\- Python

\- Flask

\- SQLite

\- pytest

\- REST API

\- Git and GitHub



\## Project Structure

\- `app.py` - Flask application and API endpoints

\- `test\_app.py` - Automated tests

\- `tasks.db` - SQLite database, created by the application

\- `requirements.txt` - Python dependencies

\- `README.md` - Project documentation



\## Installation



1\. Clone or download this repository.

2\. Open a terminal in the project directory.

3\. Create and activate a virtual environment:



&#x20;  ```powershell

&#x20;  python -m venv venv

&#x20;  .\\venv\\Scripts\\Activate.ps1

&#x20;  ```



4\. Install dependencies:



&#x20;  ```powershell

&#x20;  pip install -r requirements.txt

&#x20;  ```



\## Run the Application



```powershell

python app.py

```



The API runs locally at `http://127.0.0.1:5000`.



\## API Endpoints



| Method | Endpoint | Description |

|--------|----------|-------------|

| GET | `/tasks` | Retrieve all tasks |

| POST | `/tasks` | Create a task |

| PUT | `/tasks/<task\_id>` | Update a task |

| DELETE | `/tasks/<task\_id>` | Delete a task |



\### Example: Create a Task



Send a POST request to `/tasks` with JSON:



```json

{

&#x20; "title": "Complete API project"

}

```



\## Run Automated Tests



```powershell

python -m pytest -v

```



The project currently includes automated tests for retrieving tasks, creating tasks, input validation, updating tasks, and deleting tasks.



\## Learning Outcomes

\- REST API development

\- CRUD operations

\- Database integration

\- Input validation and error handling

\- Automated software testing



