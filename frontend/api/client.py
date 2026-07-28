import requests


class BackendClient:

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8000",
    ) -> None:

        self.base_url = base_url

    def chat(
    self,
    session_id: str,
    message: dict,
) -> dict:

        response = requests.post(
            f"{self.base_url}/chat",
            json={
                "session_id": session_id,
                "message": message,
            },
            timeout=60,
        )

        print("Status:", response.status_code)
        print("Response:", response.text)

        response.raise_for_status()

        return response.json()