import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# Constants
GENERATIVE_AI_MODEL_PATH = "routes.routes.Generative_AI_Model"

client = TestClient(app)


class TestRoutes:
    def test_query_response_success_check_structure(self):
        """Test the /query_response endpoint for valid input."""
        mock_model_output = {"message": "Some dynamic response string from the model."}
        mock_model_instance = MagicMock()
        mock_model_instance.generate_response_according_selected_model_type.return_value = (
            mock_model_output
        )

        with patch(GENERATIVE_AI_MODEL_PATH) as MockModel:
            MockModel.return_value = mock_model_instance

            response = client.post(
                "/query_response",
                json={
                    "user_query": "Tell me about testing",
                    "model_type": "OpenAI",
                },
            )

            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, dict)
            assert "message" in response_data
            assert isinstance(response_data["message"], str)
            mock_model_instance.generate_response_according_selected_model_type.assert_called_once_with(
                model_type="OpenAI", user_query="Tell me about testing"
            )

    def test_query_response_missing_query(self):
        """Test /query_response with missing user_query."""
        response = client.post("/query_response", json={"model_type": "OpenAI"})
        assert response.status_code == 400
        assert response.json() == {"message": "user_query or model_type is missing"}

    def test_query_response_missing_model_type(self):
        """Test /query_response with missing model_type."""
        response = client.post("/query_response", json={"user_query": "Test input"})
        assert response.status_code == 400
        assert response.json() == {"message": "user_query or model_type is missing"}

    def test_query_response_model_exception(self):
        """Test /query_response when model raises an exception."""
        error_message = "An internal model error occurred."
        mock_model_instance = MagicMock()
        mock_model_instance.generate_response_according_selected_model_type.side_effect = Exception(
            error_message
        )

        with patch(GENERATIVE_AI_MODEL_PATH) as MockModel:
            MockModel.return_value = mock_model_instance

            response = client.post(
                "/query_response",
                json={
                    "user_query": "Cause an error",
                    "model_type": "ErrorModel",
                },
            )

            assert response.status_code == 500
            assert response.json() == {"message": error_message}

    def test_get_session_history_success_check_structure(self):
        """Test /session_history endpoint."""
        mock_history_data = [{"user_query": "q1"}, {"user_query": "q2"}]
        mock_model_instance = MagicMock()
        mock_model_instance.get_session_history_from_MongoDB.return_value = (
            mock_history_data
        )

        with patch(GENERATIVE_AI_MODEL_PATH) as MockModel:
            MockModel.return_value = mock_model_instance

            response = client.get("/session_history")
            assert response.status_code == 200
            response_data = response.json()
            assert isinstance(response_data, list)
            if response_data:
                assert isinstance(response_data[0], dict)
                assert "user_query" in response_data[0]
            mock_model_instance.get_session_history_from_MongoDB.assert_called_once()

    def test_get_health_check_response(self):
        """Test /health endpoint returns expected message."""
        response = client.get("/health")
        assert response.status_code == 200
        response_data = response.json()
        assert response_data == {"message": "Service Health is Good"}
        assert "message" in response_data
        assert isinstance(response_data["message"], str)


# Optional: run via script
if __name__ == "__main__":
    pytest.main([__file__])
