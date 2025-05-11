# API_Deploy_Github_Action_AWS_EKS
API Deploy with GitHub Actions &amp; AWS EKS This repository automates the deployment of an API to AWS Elastic Kubernetes Service (EKS) using GitHub Actions. It includes CI/CD workflows for building, testing, and deploying containerized applications efficiently.

# API Deployment with GitHub Actions & AWS ECR & EKS

## 1. Project Structure

|-- config/
|   |-- __init__.py
|   |-- config.py
|
|-- model/
|   |-- __init__.py
|   |-- model.py
|
|-- routes/
|   |-- __init__.py
|   |-- routes.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_app_routes.py
|
|-- .github/
|   |-- workflows/
|   |   |-- ci-cd-pipeline.yaml
|
|-- __init__.py
|-- app.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- .env
|-- .dockerignore
|-- Dockerfile
|-- setup.py

## 2. Create a virtual environment & install dependencies

```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

```bash
pip install --no-cache-dir -r requirements.txt
```

## 3. Set up environment variables

- Create a .env file and configure necessary credentials

MONGO_URI=mongodb://localhost:27017

AWS_ACCESS_KEY=your_aws_access_key

AWS_SECRET_KEY=your_aws_secret_key

## 4. Run the application

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

## 5. Deployment

```bash
docker build -t generative_ai_app:latest .
```

```bash
docker run -d -p 8000:8000 --name generative_ai_app_container generative_ai_app:latest
```


