# test_app.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import the FastAPI app from app.py
from app import app

# Define the path to where Generative_AI_Model is imported in routes.py
GENERATIVE_AI_MODEL_PATH = "routes.routes.Generative_AI_Model"
HEALTH_CHECK_PATH = "routes.routes"

# # Create a TestClient instance using the FastAPI app
client = TestClient(app)


class TestRoutes:
    """
    Test class for testing the endpoints defined in routes.py,
    which are included in the main application.
    """

    def test_query_response_success_check_structure(self):
        """Test the /query_response endpoint, checking response structure and types."""
        # We still mock the model's output, but now we mock a *typical* structure,
        # not a fixed string we expect to match exactly.
        # Assume the model method is expected to return a dict with a 'response' key containing a string.
        mock_model_output = {"message": "Some dynamic response string from the model."}
        mock_model_instance = MagicMock()
        # Configure the mock model instance method to return the mock structure
        mock_model_instance.generate_response_according_selected_model_type.return_value = (
            mock_model_output
        )

        # Use patch to replace the actual Generative_AI_Model class
        with patch(GENERATIVE_AI_MODEL_PATH) as MockModel:
            # Configure the mock class so that creating an instance returns our mock instance
            MockModel.return_value = mock_model_instance

            test_payload = {
                "user_query": "Tell me about testing",
                "model_type": "OpenAI",
            }
            response = client.post("/query_response", json=test_payload)

            # Assertions: Check status code, response is JSON, check structure/types
            assert response.status_code == 200
            response_data = response.json()  # Get the JSON response body

            # Check that the response is a dictionary
            assert isinstance(response_data, dict)
            # Check that the expected key "response" is in the dictionary
            assert "message" in response_data
            # Check that the value associated with "response" is a string
            assert isinstance(response_data["message"], str)

            # Verify that the method on the model was called correctly (this part is still valid and important)
            mock_model_instance.generate_response_according_selected_model_type.assert_called_once_with(
                model_type="OpenAI", user_query="Tell me about testing"
            )

    def test_query_response_missing_query(self):
        """
        Test the /query_response endpoint with missing user_query.
        This test checks the error handling for invalid input.
        """
        # Prepare the test payload with missing user_query
        test_payload = {"model_type": "OpenAI"}
        # Make a POST request to the /query_response endpoint
        response = client.post("/query_response", json=test_payload)

        # Assert that the response status code is 400 (Bad Request)
        assert response.status_code == 400
        # Assert that the response JSON contains the expected error detail
        assert response.json() == {"detail": "user_query and model_type are required"}

    def test_query_response_missing_model_type(self):
        """
        Test the /query_response endpoint with missing model_type.
        This test checks the error handling for invalid input.
        """
        # Prepare the test payload with missing model_type
        test_payload = {"user_query": "Tell me about testing"}
        # Make a POST request to the /query_response endpoint
        response = client.post("/query_response", json=test_payload)

        # Assert that the response status code is 400 (Bad Request)
        assert response.status_code == 400
        # Assert that the response JSON contains the expected error detail
        assert response.json() == {"detail": "user_query and model_type are required"}

    def test_query_response_model_exception(self):
        """
        Test the /query_response endpoint when the model raises an exception.
        This test checks the error handling when the model encounters an error.
        """
        # Define an error message
        error_message = "An internal model error occurred."
        # Create a mock instance of the Generative_AI_Model
        mock_model_instance = MagicMock()
        # Configure the mock instance to raise an exception
        mock_model_instance.generate_response_according_selected_model_type.side_effect = Exception(
            error_message
        )

        # Use patch to replace the actual Generative_AI_Model class with our mock
        with patch(GENERATIVE_AI_MODEL_PATH) as MockModel:
            # Configure the mock class to return our mock instance when instantiated.
            MockModel.return_value = mock_model_instance

            # Prepare the test payload
            test_payload = {"user_query": "Cause an error", "model_type": "ErrorModel"}
            # Make a POST request to the /query_response endpoint
            response = client.post("/query_response", json=test_payload)

            # Assert that the response status code is 500 (Internal Server Error)
            assert response.status_code == 500
            # Assert that the response JSON contains the error message
            assert response.json() == {"detail": error_message}

    # Example of how you'd check structure for session history too
    def test_get_session_history_success_check_structure(self):
        """Test the /session_history endpoint success, checking response structure."""
        # Mock history data - typically a list of dictionaries
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

            # Check that the response is a list
            assert isinstance(response_data, list)
            # If the list is not empty, check the structure of the first item
            if response_data:
                assert isinstance(response_data[0], dict)
                assert "user_query" in response_data[0]
                assert isinstance(response_data[0]["user_query"], str)

            mock_model_instance.get_session_history_from_MongoDB.assert_called_once()

    # Function to test of the health check routes
    def test_get_health_check_response(self):
        """Test the /health endpoint success, checking response structure."""
        # Mock health data - typically a dictionary
        mock_health_data = {"message": "Service Health is Good"}
        mock_health_instance = MagicMock()
        mock_health_instance.get_health_check.return_value = mock_health_data

        with patch(HEALTH_CHECK_PATH) as MockModel:
            MockModel.return_value = mock_health_instance

            response = client.get("/health")

            assert response.status_code == 200
            response_data = response.json()

            # Check that the response is a list
            assert isinstance(response_data, dict)
            # If the list is not empty, check the structure of the first item
            if response_data:
                assert response_data == mock_health_data
                assert "message" in response_data
                assert isinstance(response_data["message"], str)
                assert response_data["message"] == "Service Health is Good"
            mock_health_instance.get_health_check.assert_called_once()


# Run the tests using pytest
if __name__ == "__main__":
    pytest.main([__file__])
