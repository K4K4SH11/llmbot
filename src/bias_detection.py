import shap
import torch
from transformers import pipeline

def detect_bias(response, model, tokenizer):
    # Simplified SHAP analysis (extend with full pipeline for production)
    explainer = shap.Explainer(
        pipeline("text-generation", model=model, tokenizer=tokenizer)
    )
    shap_values = explainer([response])
    
    # Bias score (0–1, higher = more bias)
    bias_score = abs(shap_values.values.mean())
    return bias_score