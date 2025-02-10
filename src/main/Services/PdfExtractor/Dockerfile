# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    make \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python project files into the container
COPY requirements.txt /app/

# Install the required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./App /app

# Expose the Flask app port
EXPOSE 5001

# Run the Flask app
CMD ["python", "ExtractPdf.py"]
