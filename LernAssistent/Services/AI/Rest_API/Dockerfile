# Basis-Image: Verwende OpenJDK
FROM openjdk:21-slim

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die JAR-Datei ins Container-Verzeichnis
COPY LLM_API.jar LLM_API.jar

# Port, der vom Server verwendet wird
EXPOSE 9191

# Startbefehl für die JAR-Datei
CMD ["java", "-jar", "LLM_API.jar"]
