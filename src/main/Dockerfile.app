# Use an appropriate base image (e.g., Python if using Python)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install dependencies (if applicable)
RUN pip install -r requirements.txt

# Install the wait-for-it script
RUN curl -o /wait-for-it.sh https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh \
  && chmod +x /wait-for-it.sh

# Set environment variables
ENV DB_URL=postgres://db_admin:password123@db:5432/main_db
ENV DB_USER=db_admin
ENV DB_PASSWORD=password123
ENV DB_NAME=main_db

# Define the entrypoint to wait for the database to be ready
ENTRYPOINT ["./wait-for-it.sh", "db:5432", "--", "python3", "run.py"]
