# Use an appropriate base image (e.g., Python if using Python)
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install dependencies (if applicable)
RUN pip install -r requirements.txt

# Install the wait-for-it script
# RUN curl --fail -o /wait-for-it.sh https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh \
#  && chmod +x /wait-for-it.sh \
#  && ls -l /wait-for-it.sh


# Set environment variables
ENV DB_URL=postgres://postgres:postgres@database:5433/Lernassistent
ENV DB_USER=postgres
ENV DB_PASSWORD=postgres
ENV DB_NAME=Lernassistent

# Define the entrypoint to wait for the database to be ready
# ENTRYPOINT ["/wait-for-it.sh", "db:5432", "--", "python3", "run.py"]
CMD ["python3", "./App/app.py"]

