import pytest
from fastapi.testclient import TestClient
from main import app

def test_create_poll_success():
    response = client.post(
        "/create_poll",
        data={
            "title": "Sample Poll",
            "description": "This is a sample poll.",
            "start_date": "2023-06-01",
            "end_date": "2023-06-30",
            "quest_type": "multiple_choice"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Poll created successfully"}
