FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project into the working directory
COPY . ${LAMBDA_TASK_ROOT}

# Lambda will look for app.handler (i.e., handler in app.py)
CMD ["app.handler"]