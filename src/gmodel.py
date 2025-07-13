from fastapi import FastAPI
from pydantic import BaseModel
from src.model import load_model
import yaml

app = FastAPI()

with open("src/config.yaml", "r") as f:
    config = yaml.safe_load(f)

model, tokenizer = load_model(config["model"])

class Query(BaseModel):
    text: str
    max_length: int = 50

@app.post("/generate")
async def generate(query: Query):
    print("Received prompt text:", query.text)
    inputs = tokenizer(query.text, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=query.max_length)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("Generated response:", response)
    return {"response": response}

