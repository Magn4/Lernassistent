# Use an official OpenJDK runtime as a parent image
FROM openjdk:21-jdk-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the  api key ini file into the container
COPY ./Rest_API/out/artifacts/LLM_API_jar/groqAPIKey.ini /app/groqAPIKey.ini

# Copy the local JAR file into the container
COPY ./Rest_API/out/artifacts/LLM_API_jar/LLM_API.jar /app/LLM_API.jar

# Expose the port the application will run on
EXPOSE 9191

# Command to run the JAR file
CMD ["java", "-jar", "LLM_API.jar"]
