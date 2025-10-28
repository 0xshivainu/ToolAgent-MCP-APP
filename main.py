from fastapi import FastAPI, Body, HTTPException
from fastapi_mcp import FastApiMCP
from openai import OpenAI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time
from config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或 ["*"] 開發階段用
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp = FastApiMCP(app)
# mcp.mount_http()

client = OpenAI(
    api_key=settings.api_key,
    base_url=settings.base_url
)

class GenerateArticleParams(BaseModel):
    topic: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "simple-mcp"}


@app.post("/generate_article", operation_id="generate_article")
async def generate_article(parameters: GenerateArticleParams = Body(...)):
    topic = parameters.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Missing parameter: topic")
    prompt = f"""
    You are a TOEIC instructor and English news writer.
    Your task is to create a structured TOEIC learning news article about: "{topic}".

    ## OUTPUT FORMAT
    Respond strictly in this JSON-like structure (without code fences):
    {{
        "metadata": {{
            "title": string,
            "date": string (format: YYYY-MM-DD),
            "reading_level": "B1-B2",
            "word_count": integer
        }},
        "article": {{
            "headline": string,
            "body": string (3–5 short paragraphs, clear and concise),
            "conclusion": string
        }},
        "review": {{
            "vocabulary": [ "word: definition", ... (5–10 items) ],
            "phrases": [ "phrase: meaning", ... (3–5 items) ],
            "sentence_patterns": [ "pattern: example usage", ... (3–5 items) ]
        }}
    }}

    ## STYLE REQUIREMENTS
    - Write in natural English suitable for TOEIC learners.
    - Keep sentences under 20 words when possible.
    - Use current, fact-based, real-world tone (e.g., economy, technology, workplace, travel).
    - Avoid complex idioms or slang.
    - Provide helpful, relevant learning material in the review section.

    ## GOAL
    Produce a clear, educational English article that sounds authentic and is visually structured for rendering on a frontend application.
    """
    response = client.chat.completions.create(
        model="gemini-2.0-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": response.choices[0].message.content}


if __name__ == "__main__":
    mcp = FastApiMCP(
        app,
        include_operations=["generate_article"],
    )
    mcp.mount()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
