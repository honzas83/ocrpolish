from typing import Any
from unittest.mock import MagicMock


def create_mock_ollama_response(content: str) -> dict[str, Any]:
    """
    Creates a mock response object compatible with the ollama client chat response.
    """
    return {"message": {"content": content, "role": "assistant"}}


class MockOllamaClient:
    def __init__(self, return_value: str):
        self.return_value = return_value
        self.chat = MagicMock(return_value=create_mock_ollama_response(return_value))
