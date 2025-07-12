from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.model import load_model
from src.agent import ChatbotAgent
from src.cache import RedisCache
from src.gdpr_compliance import anonymize_data, log_interaction
from src.bias_detection import detect_bias
import yaml
import uvicorn

app = FastAPI(title="AI Public Service Chatbot")
app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="src/templates")

# Load config
with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)

model, tokenizer = load_model(config["model"])
serpapi_key = config.get("serpapi_key", "")
agent = ChatbotAgent(model, tokenizer, config["model"]["max_length"], serpapi_key)
cache = RedisCache(config["redis"])

class Query(BaseModel):
    text: str
    language: str = "en"

@app.post("/chat")
async def chat(query: Query):
    cache_key = f"{query.language}:{query.text}"
    cached_response = cache.get(cache_key)
    if cached_response:
        return {"response": cached_response, "cached": True}

    response = agent.handle_query(query.text, query.language)
    bias_score = detect_bias(response, model, tokenizer)
    if bias_score > 0.5:
        response = "Response flagged for potential bias. Please rephrase query."

    anonymized_query = anonymize_data(query.text)
    log_interaction(anonymized_query, response)
    cache.set(cache_key, response)
    return {"response": response, "cached": False}

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host=config["api"]["host"], port=config["api"]["port"])