# Deploy FastAPI Application with GitHub Actions and AWS Lambda

**Deploy_FastAPI_Github_Action_AWS_Lambda** is a GitHub repository for automating the deployment of a FastAPI application to AWS Lambda using GitHub Actions. It includes workflows for formatting, testing, building, and deploying the application as a serverless function, ensuring seamless CI/CD integration.

This repository demonstrates how to deploy a FastAPI application to AWS Lambda using GitHub Actions for CI/CD. The project includes a structured FastAPI application, automated workflows for testing and deployment, and integration with AWS services like Lambda and ECR.

---

## Features

- **FastAPI Application**: A lightweight and high-performance web framework for building APIs.
- **AWS Lambda Deployment**: Deploy the FastAPI app as a serverless function using AWS Lambda.
- **GitHub Actions CI/CD**: Automate code formatting, testing, building, and deployment workflows.
- **Dockerized Application**: Use Docker to containerize the application for consistent deployment.
- **MongoDB Integration**: Store session history in MongoDB for persistence.
- **Generative AI Models**: Integrate OpenAI and Gemini models for generating responses.

---

## Project Structure

```
|-- config/
|   |-- __init__.py
|   |-- config.py          # MongoDB configuration and connection setup
|
|-- model/
|   |-- __init__.py
|   |-- model.py           # Logic for integrating OpenAI and Gemini models
|
|-- routes/
|   |-- __init__.py
|   |-- routes.py          # API endpoints for query responses, session history, and health checks
|
|-- tests/
|   |-- __init__.py
|   |-- test_app_routes.py # Unit tests for API endpoints
|
|-- .github/
|   |-- workflows/
|   |   |-- ci-cd-pipeline.yaml # GitHub Actions workflow for CI/CD
|
|-- app.py                 # Main FastAPI application entry point
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
|-- .gitignore             # Files and directories to ignore in Git
|-- .env                   # Environment variables (not included in the repo)
|-- .dockerignore          # Files to exclude from Docker builds
|-- Dockerfile             # Dockerfile for containerizing the application
|-- setup.py               # Python package setup
```

---

## How It Works

### 1. FastAPI Application
The FastAPI application is defined in `app.py` and includes the following endpoints:
- **`/query_response`**: Accepts a user query and model type (e.g., OpenAI or Gemini) and returns a generated response.
- **`/session_history`**: Retrieves the last 10 user queries from MongoDB.
- **`/health`**: Returns the health status of the service.

### 2. Generative AI Models
The `model/model.py` file integrates OpenAI and Gemini models to generate responses based on user queries. It also stores session history in MongoDB for persistence.

### 3. MongoDB Integration
The `config/config.py` file sets up a connection to MongoDB, allowing the application to store and retrieve session history.

### 4. Testing
Unit tests are defined in `tests/test_app_routes.py` to ensure the API endpoints work as expected. The tests use `pytest` and mock external dependencies for isolated testing.

### 5. CI/CD with GitHub Actions
The `.github/workflows/ci-cd-pipeline.yaml` file defines a GitHub Actions workflow with the following steps:
- **Code Formatting**: Check code formatting using `black`.
- **Testing**: Run unit tests using `pytest`.
- **Docker Build and Push**: Build a Docker image and push it to AWS ECR.
- **AWS Lambda Deployment**: Update the AWS Lambda function to use the new Docker image.

### 6. Dockerization
The `Dockerfile` defines the steps to containerize the application. The container is built on the AWS Lambda Python runtime and includes all dependencies.

---

## Setup Instructions

### 1. Create a Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
pip install --no-cache-dir -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file with the following variables:
```env
OPENAI_API_KEY=<your_openai_api_key>
GEMINI_API_KEY=<your_gemini_api_key>
MONGODB_URI=<your_mongodb_uri>
MONGODB_DATABASE_NAME=<your_database_name>
MONGODB_SESSION_HISTORY_COLLECTION=<your_collection_name>
```

### 3. Run the Application Locally
Start the FastAPI application:
```bash
uvicorn app:app --reload
```

### 4. Run Tests
Run the unit tests using `pytest`:
```bash
pytest -v tests/test_app_routes.py
```

### 5. Build and Deploy with Docker
Build the Docker image:
```bash
docker build -t fastapi-app .
```

Run the container locally:
```bash
docker run -p 8000:8000 fastapi-app
```

---

## Deployment to AWS Lambda

### 1. Create a Lambda Function on AWS
- Deploy the ECR image to the Lambda function.
- Set the required environment variables in the Lambda function's configuration.

### 2. Configure AWS Credentials
Set up AWS credentials in your GitHub repository secrets:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ECR_REPO`
- `AWS_LAMBDA_FUNCTION_NAME`
- `LATEST_IMAGE_URI`

### 2. GitHub Actions Workflow
Push changes to the `main` branch to trigger the CI/CD pipeline. The workflow will:
1. Format the code.
2. Run tests.
3. Build and push the Docker image to AWS ECR.
4. Update the AWS Lambda function to use the new image.

---

## API Endpoints

### `/query_response`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "user_query": "Tell me about FastAPI",
    "model_type": "OpenAI"
  }
  ```
- **Response**:
  ```json
  {
    "message": "FastAPI is a modern web framework..."
  }
  ```

### `/session_history`
- **Method**: GET
- **Response**:
  ```json
  [
    {"user_query": "What is FastAPI?"},
    {"user_query": "Tell me about Docker"}
  ]
  ```

### `/health`
- **Method**: GET
- **Response**:
  ```json
  {
    "message": "Service Health is Good."
  }
  ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

**Amir Aziz**  
Email: amirds0235@gmail.com