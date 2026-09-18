# Support Ticket AI

An AI-powered support ticket analytics system built for the DOTMappers AI Engineer Technical Assessment.

The system ingests a CSV dataset of 500 customer support tickets and provides:

- Natural-language querying of support ticket data
- Anomaly detection
- REST API using FastAPI
- Minimal web UI using Streamlit
- LLM-powered natural-language understanding using Google Gemini
- Local Pandas fallback for reliable numerical queries when the LLM quota is unavailable

---

## 1. Features

### CSV Data Ingestion

The application loads the provided `support_tickets.csv` dataset using Pandas.

The dataset contains 500 support tickets with information including:

- Ticket ID
- Creation timestamp
- Category
- Priority
- Status
- Response time
- Resolution time
- Agent ID
- Customer rating
- Issue summary

### Natural-Language Querying

Users can ask questions in normal English, for example:

- How many open tickets are there?
- How many critical tickets are there?
- What is the average customer rating?
- Which agent has the lowest average customer rating?
- What is the average customer rating for each category?

The system calculates important statistics from the dataset and provides them as context to the Gemini model.

### Anomaly Detection

The system detects:

1. Tickets with unusually long resolution times.
2. Unresolved High or Critical priority tickets that are older than 24 hours.

### REST API

FastAPI exposes the following endpoints:

- `GET /health`
- `GET /query`
- `GET /anomalies`

### Minimal UI

A Streamlit interface allows users to:

- View total ticket count
- Ask natural-language questions
- View AI-generated answers
- Detect and display ticket anomalies

---

## 2. Architecture

```text
                    +----------------------+
                    |   support_tickets.csv|
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    Pandas / Loader   |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |    FastAPI Backend   |
                    +----------+-----------+
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
        +----------------+          +-------------------+
        | Query Service  |          | Anomaly Detector  |
        +-------+--------+          +-------------------+
                |
                v
        +----------------+
        | Gemini LLM     |
        +-------+--------+
                |
                v
        +----------------+
        | Local Pandas   |
        | Fallback       |
        +----------------+

                    |
                    v
             +--------------+
             | Streamlit UI |
             +--------------+
             3. Technology Stack
Python
Pandas
FastAPI
Uvicorn
Streamlit
Google Gemini API
python-dotenv
Requests

**4. Project Structure**
dotmappers-ai-assessment/
│
├── app/
│   ├── main.py
│   ├── data_loader.py
│   ├── anomaly_detector.py
│   ├── llm_services.py
│   ├── query_engine.py
│   └── ui.py
│
├── data/
│   └── support_tickets.csv
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
**
5. Installation**
Clone the repository
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd dotmappers-ai-assessment
Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
Install dependencies
pip install -r requirements.txt

**6. Gemini API Configuration**

Create a .env file in the project root:

GEMINI_API_KEY=your_gemini_api_key

The API key is loaded using python-dotenv.

Do not commit the .env file to GitHub.

The .env file should be included in .gitignore.

**7. Running the FastAPI Backend**

Start the FastAPI server with:

python -m uvicorn app.main:app --host 127.0.0.1 --port 8001

The API will be available at:

http://127.0.0.1:8001

Interactive API documentation:

http://127.0.0.1:8001/docs
**
8. Running the Streamlit UI**

Open another terminal and run:

streamlit run app/ui.py

Streamlit will display the local URL in the terminal.

**9. API Endpoints**

Health Check
GET /health

Example response:

{
  "status": "healthy",
  "total_tickets": 500
}
Natural-Language Query
GET /query?question=<question>

Example:

GET /query?question=How many open tickets are there?

Example response:

{
  "answer": "There are 111 open tickets."
}
Anomaly Detection
GET /anomalies

Example response:

{
  "total_anomalies": 101,
  "anomalies": []
}

The anomalies array contains the individual flagged tickets.

**10. Example Queries**

Query 1

Question:

How many open tickets are there?

Example output:

There are 111 open tickets.
Query 2

Question:

How many critical tickets are there?

Example output:

There are 55 critical tickets.
Query 3

Question:

What is the average customer rating?

Example output:

The average customer rating is 3.75.
Query 4

Question:

Which agent has the lowest average customer rating?

Example output:

AGT-08 has the lowest average customer rating at 3.48.
Query 5

Question:

What is the average customer rating for each category?

Example output:

Average customer rating by category:
Billing: 3.72,
Technical: 3.74,
General: 3.78

**11. Anomaly Detection Logic**

The anomaly detector currently checks two conditions.

Long Resolution Time

Tickets with:

resolution_time_hrs > 48

are flagged as having a long resolution time.

Unresolved High-Priority Tickets

Tickets are flagged when:

Priority is High or Critical
Status is Open or Escalated
Ticket age is greater than 24 hours

The latest ticket creation timestamp in the dataset is used as the reference point for calculating ticket age. This makes the analysis reproducible for the historical dataset.
**
12. LLM Integration**

Google Gemini is used for natural-language understanding and response generation.

The application provides the LLM with calculated dataset statistics including:

Ticket counts by status
Ticket counts by priority
Ticket counts by category
Overall customer rating
Average response time
Average resolution time
Agent-level statistics
Category-level rating statistics

The LLM is instructed to answer using only the supplied dataset statistics and not invent numerical information.

**13. Reliability and Fallback**

The application also contains a local Pandas fallback.

If the Gemini API is temporarily unavailable or the API quota is exceeded, supported numerical queries can be answered directly from the CSV using Pandas.

This prevents the application from completely failing when the external LLM service is temporarily unavailable.

**14. Known Limitations**
Gemini API availability depends on the configured API quota and rate limits.
The local fallback currently supports a defined set of common analytical questions.
More complex arbitrary queries may require additional query-planning or data-analysis logic.
The current anomaly thresholds are rule-based.
The current application is designed as a prototype rather than a production-scale deployment.
Authentication and authorization are not implemented for the REST API.
The system currently works with the provided CSV dataset rather than a live ticketing database.

**15. Future Improvements**

Possible improvements include:

Add a structured query-planning layer for more complex questions.
Support more analytical operations such as trends and time-based comparisons.
Add interactive charts and dashboards.
Add database support for larger datasets.
Add authentication for API access.
Add automated tests.
Add Docker support for easier deployment.
Add more advanced statistical anomaly detection.
Add caching and retry handling for LLM requests.
**
16. Assessment Requirements Covered**

The implementation provides:

CSV ingestion and querying
Natural-language data queries
Anomaly detection
REST API
Minimal Streamlit UI
LLM integration
requirements.txt
Project documentation
Error handling and LLM fallback

**17. Author**

Developed as part of the DOTMappers AI Engineer Technical Assessment.



