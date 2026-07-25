import requests


class BackendClient:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:

        self.base_url = base_url

    def chat(
        self,
        messages: list[dict],
    ) -> dict:

        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "messages": messages,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()