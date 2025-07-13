import shap
import torch
from transformers import pipeline

def detect_bias(response, model, tokenizer):
    explainer = shap.Explainer(
        pipeline("text-generation", model=model, tokenizer=tokenizer)
    )
    shap_values = explainer([response])
    
    bias_score = abs(shap_values.values.mean())
    return bias_score