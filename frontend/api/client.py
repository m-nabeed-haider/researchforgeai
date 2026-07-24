import requests


class BackendClient:
    """
    Client for communicating with ResearchForge backend.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:
        self.base_url = base_url

    def chat(
        self,
        message: str,
    ) -> str:

        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "message": message,
            },
            timeout=60,
        )

        response.raise_for_status()

        return response.json()["response"]