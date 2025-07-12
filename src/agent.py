from smolagents import CodeAgent, ApiWebSearchTool
from smolagents.models import TransformersModel
from src.model import load_model

class ChatbotAgent:
    def __init__(self, config, serpapi_key):
        model, tokenizer = load_model(config)
        smol_model = TransformersModel(model=model, tokenizer=tokenizer)
        self.agent = CodeAgent(
            tools=[ApiWebSearchTool(endpoint="https://serpapi.com/search", api_key=serpapi_key, api_key_name="api_key")],
            model=smol_model,
            instructions=(
                "You are a helpful assistant for public service queries. "
                "If you need up-to-date information, use the web_search tool. "
                "Incorporate the results into your answer naturally."
            )
        )

    def handle_query(self, query):
        return self.agent.run(query)