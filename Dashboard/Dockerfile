FROM public.ecr.aws/lambda/python:3.11

# Update and install system dependencies
RUN yum update -y && yum install -y git gcc-c++ gcc-gfortran python3-devel

# Setup the working directory
WORKDIR /var/task

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies into the Lambda task folder
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

# Copy your Lambda function code
COPY . ${LAMBDA_TASK_ROOT}

CMD ["lambda-analytics.lambda_handler"]
