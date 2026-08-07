from groq import Groq


class GroqProvider:
    provider_id = "groq"
    display_name = "Groq"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def complete_chat(self, system: str, user: str, model: str) -> str:
        client = Groq(api_key=self._api_key)
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
            max_tokens=500,
            top_p=1,
            stream=False,
            response_format={"type": "json_object"},
        )
        return completion.choices[0].message.content or "{}"
