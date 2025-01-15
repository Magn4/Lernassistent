# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . /app

RUN chmod +x /app/wait-for-it.sh

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd


# Specify the command to run the application

EXPOSE 5003
