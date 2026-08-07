from openai import OpenAI


class OpenAICompatibleProvider:
    provider_id = "openai_compatible"
    display_name = "OpenAI-compatible"

    def __init__(self, api_key: str, base_url: str):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")

    def complete_chat(self, system: str, user: str, model: str) -> str:
        client = OpenAI(api_key=self._api_key or "ollama", base_url=self._base_url)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        return completion.choices[0].message.content or "{}"
