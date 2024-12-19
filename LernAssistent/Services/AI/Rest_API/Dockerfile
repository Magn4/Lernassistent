# Basis-Image
FROM openjdk:21-slim

# Arbeitsverzeichnis
WORKDIR /app

# Kopiere die JAR-Datei
COPY LLM_API.jar LLM_API.jar

# Umgebungsvariablen (optional)
ENV SERVER_URL=http://209.38.252.155:11434

# Port freigeben
EXPOSE 9191

# Startbefehl
CMD ["java", "-jar", "LLM_API.jar"]
