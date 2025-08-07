import os
import requests
from models.stream_models import HeygenSessionModel

class HeygenClient:
    def __init__(self):
        self.heygen_api_key = os.getenv("HEYGEN_API_KEY")
        self.url = "https://api.heygen.com"

    def create_session(self):
        resp = requests.post(
            f"{self.url}/v1/streaming.new",
            headers={
                "Authorization": f"Bearer {self.heygen_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "version": "v2",
                "avatar_id": "Ann_Therapist_public",
            }
        )
        print(resp.json()["data"])

        return HeygenSessionModel(**resp.json()["data"])

    def start_stream(self, session_id: str):
        resp = requests.post(
            f"{self.url}/v1/streaming.start",
            headers={
                "Authorization": f"Bearer {self.heygen_api_key}",
                "Content-Type": "application/json"
            },
            json={"session_id": session_id}
        )

        return resp.json()

    def send_text(self, session_id: str, text: str, task_type: str = "chat"):
        resp = requests.post(
            f"{self.url}/v1/streaming.task",
            headers={
                "Authorization": f"Bearer {self.heygen_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "session_id": session_id,
                "text": text,
                "task_type": task_type
            }
        )

        return resp.json()