from huggingface_hub import InferenceClient
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Qwen/Qwen2-7B-Instruct"#"HuggingFaceTB/SmolLM3-3B"

def load_model(config):
    model_name = config["name"]
    device = config.get("device")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16 if device=="cuda" else torch.float32)
    model = model.to(device)
    return model, tokenizer

def generate_response(model, tokenizer, query, max_length, language="en"):
    prompt = f"{query}"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(**inputs, max_new_tokens=max_length)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response