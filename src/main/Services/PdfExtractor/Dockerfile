# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Python project files into the container
COPY . /app

# Install the required Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Flask app port
EXPOSE 5001

# Run the Flask app
CMD ["python", "ExtractPdf.py"]
