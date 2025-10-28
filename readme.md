# 📰 FastAPI MCP TOEIC Article Generator

A FastAPI-based **MCP (Model Context Protocol)** service that generates structured English learning news articles for TOEIC learners.  
The service integrates with OpenAI-compatible language models and provides a clean JSON output designed for web rendering.

---

## 🚀 Features

- Generate realistic, TOEIC-style English news articles
- Returns structured JSON (metadata, article, and review)
- Ready for MCP integration or standalone API use
- Includes responsive web interface for manual testing
- Deployable via Docker or Render

---

## 🧩 Directory Structure

├── main.py # Core FastAPI MCP server
├── requirements.txt # Python dependencies
├── Dockerfile # Build instructions for container deployment
├── docker-compose.yml # Local testing / container orchestration
├── config.py/ # Contains API configuration to call .env files
└── index.html # (Optional) Simple web client (frontend)



---

## ⚙️ Setup & Installation

### 1. Clone and enter project directory

```
git clone https://github.com/0xshivainu/EnglishArticleAgent-MCP-APP.git
cd EnglishArticleAgent-MCP-APP
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Configure environment

Create a file `config/settings.py` and define your OpenAI-compatible settings:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
api_key: str = "YOUR_API_KEY"
base_url: str = "https://api.openai.com..."

settings = Settings()
```

---

## ▶️ Run Locally

### Using Uvicorn

```
python main.py
```
### Or with Docker Compose(mac)
```
docker compose up --build
```

Server will be available at:  
👉 `http://0.0.0.0:10000`

---

## 🌐 API Endpoints

### Health Check

GET /health

Response:
```json
{
    "status": "healthy",
    "service": "simple-mcp"
}
```

### Generate Article

POST /generate_article

**Request Body**
```json
{
    "topic": "artificial intelligence in the workplace"
}
```
**Sample cURL Command**
```shell
curl -X POST "https://0.0.0.0:10000/generate_article"
-H "Content-Type: application/json"
-d '{"topic": "artificial intelligence in the workplace"}'
```