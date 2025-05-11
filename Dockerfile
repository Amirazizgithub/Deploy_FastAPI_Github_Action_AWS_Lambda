# Use the AWS Lambda base image for Python
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR /fastapi_app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# AWS Lambda handler
CMD ["app.handler"]
