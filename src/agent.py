from smolagents import CodeAgent, ApiWebSearchTool
from smolagents.models import TransformersModel, ChatMessage
from src.model import load_model
import httpx

class RemoteModelWrapper:
    def __init__(self, model_server_url):
        self.model_server_url = model_server_url
        self.system_prompt = (
            "You are a helpful assistant for public service queries."
            "If you need up-to-date information, use the web_search tool."
            "Incorporate the results into your answer naturally."
        )

    def generate(self, input_messages, max_new_tokens=50, stop_sequences=None, **kwargs):
        latest_user_message = None
        for msg in reversed(input_messages):
            if msg.role == "user":
                content = msg.content
                if isinstance(content, list):
                    texts = []
                    for item in content:
                        if isinstance(item, dict) and 'text' in item:
                            texts.append(item['text'])
                        else:
                            texts.append(str(item))
                    latest_user_message = "\n".join(texts)
                elif isinstance(content, dict) and 'text' in content:
                    latest_user_message = content['text']
                elif isinstance(content, str):
                    latest_user_message = content
                else:
                    latest_user_message = str(content)
                break

        if latest_user_message is None:
            latest_user_message = ""

        prompt = f"{self.system_prompt}\n\nUser: {latest_user_message}\nAssistant:"

        data = {"text": prompt, "max_length": max_new_tokens}
        print(f"Prompt length: {len(prompt)} characters")
        print(f"Prompt preview:\n{prompt[:500]}")

        try:
            response = httpx.post(f"{self.model_server_url}/generate", json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            model_response = result["response"]
            return ChatMessage(role="assistant", content=model_response)
        except httpx.RequestError as e:
            raise RuntimeError(f"Model server request failed: {e}")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Model server returned error: {e.response.status_code}")


class ChatbotAgent:
    def __init__(self, model_server_url, serpapi_key):
        remote_model = RemoteModelWrapper(model_server_url)
        self.agent = CodeAgent(
            tools=[
                ApiWebSearchTool(
                    endpoint="https://serpapi.com/search",
                    api_key=serpapi_key,
                    api_key_name="api_key"
                )
            ],
            model=remote_model,
            instructions=(
                "You are a helpful assistant for public service queries. "
                "If you need up-to-date information, use the web_search tool. "
                "Incorporate the results into your answer naturally."
            )
        )

    def handle_query(self, query):
        return self.agent.run(query)