import pytest
from src.model import load_model, generate_response

def test_generate_response():
    config = {
        "name": "Qwen/Qwen2-7B-Instruct",
        "max_length": 512,
        "device": "cuda"
    }
    model, tokenizer = load_model(config)
    response = generate_response(model, tokenizer, "How do I cook a potato", 128, "en")
    assert isinstance(response, str)
    assert len(response) > 0
    print(response)