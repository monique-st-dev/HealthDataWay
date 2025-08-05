# 1. Use a lightweight base image with Python 3.11
FROM python:3.11-slim

# 2. Disable Python cache and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /code

# 4. Copy requirements.txt and install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# 5. Copy the rest of the project files
COPY . /code/