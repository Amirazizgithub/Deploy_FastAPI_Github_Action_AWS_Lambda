FROM public.ecr.aws/lambda/python:3.11

# Set working directory to Lambda's default
WORKDIR /var/task

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into the working directory
COPY . .

# Lambda will look for app.handler (i.e., handler in app.py)
CMD ["app.handler"]