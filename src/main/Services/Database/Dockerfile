# Use the official PostgreSQL image as the base
FROM postgres:latest

# Set environment variables for the database
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=Lernassistent
# Set the PostgreSQL port to 5432

# Expose the database port
EXPOSE 5432

# Optionally, you can copy any initialization scripts you want to run on the database startup
# COPY ./init-scripts /docker-entrypoint-initdb.d/

# Default command is already defined by the PostgreSQL image, no need to define it again
