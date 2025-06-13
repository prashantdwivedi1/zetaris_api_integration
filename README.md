This is a simple FastAPI application that fetches the latest questions from Stack Overflow using the Stack Exchange API.

🚀 Features
Retrieve the most recent Stack Overflow questions.

Filter questions by a specific tag.

Customize the number of questions returned.

🧪 Example Usage
Endpoint
bash
Copy
Edit
GET /questions
Query Parameters
Parameter	Type	Description	Default
tag	string	Optional tag to filter questions by (e.g. python)	None
pagesize	int	Number of questions to retrieve (max 100)	5

Sample Request
bash
Copy
Edit
GET /questions?tag=python&pagesize=3
Sample Response
json
Copy
Edit
{
  "questions": [
    {
      "title": "How to use FastAPI with SQLAlchemy?",
      "score": 4,
      "tags": ["python", "fastapi", "sqlalchemy"],
      "link": "https://stackoverflow.com/questions/12345678"
    },
    ...
  ]
}
🛠️ Requirements
Python 3.7+

fastapi

uvicorn

requests

📦 Installation
bash
Copy
Edit
git clone https://github.com/yourusername/stackoverflow-fastapi-api.git
cd stackoverflow-fastapi-api
pip install -r requirements.txt
▶️ Running the App
Start the server using Uvicorn:

bash
Copy
Edit
uvicorn main:app --reload
Then navigate to:

API docs: http://localhost:8000/docs

Questions endpoint: http://localhost:8000/questions

📝 Notes
This project uses the public Stack Exchange API, which may be rate-limited.

Ensure proper error handling in production.
