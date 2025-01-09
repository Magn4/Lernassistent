# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Copy the requirements file to the working directory
COPY requirements.txt /app/
# Copy wait-for-it.sh script and make it executable
COPY wait-for-it.sh /app/
RUN chmod +x /app/wait-for-it.sh

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y netcat-openbsd

# Expose the port the app runs on
EXPOSE 5002
<<<<<<< HEAD

# Command to run the application
CMD ["python", "./Controllers/MainController.py"]
=======
>>>>>>> d7edf03bfcdf47d0065ccee46b98f372c0c3d078
