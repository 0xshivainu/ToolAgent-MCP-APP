from fastapi import FastAPI, Body, HTTPException
from fastapi_mcp import FastApiMCP
from openai import OpenAI
from pydantic import BaseModel

from config import settings

app = FastAPI()
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
    You are a TOEIC expert. Generate a timely English news article about {topic},
    mark the date and time, and include a review section listing important TOEIC vocabulary,
    phrases, and sentence structures used in the article.
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
