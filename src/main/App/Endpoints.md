# API Endpoints

This document provides a list and description of all the endpoints available in the main app service.

## Dashboard

### POST /upload_dashboard
- **Description**: Upload a PDF file and extract text for the dashboard.
- **Request Body**:
  - `moduleName` (string): The name of the module.
  - `topicName` (string): The name of the topic.
  - `file` (file): The PDF file to extract text from.
- **Response**:
  - 200: File uploaded successfully with extracted text.
  - 400: Missing required fields or invalid file format.
  - 500: Internal server error.

## PDF Processing

### POST /get_summary
- **Description**: Get a summary of the provided PDF file.
- **Request Body**:
  - `file` (file): The PDF file to summarize.
  - `use_local` (boolean, optional): Whether to use the local AI service (default is false).
  - `title` (string, optional): The title for the summary.
- **Response**:
  - 200: Summary of the PDF file.
  - 400: Missing required fields or invalid file format.
  - 500: Internal server error.

### POST /get_explanation
- **Description**: Get a detailed explanation of the provided PDF file.
- **Request Body**:
  - `file` (file): The PDF file to explain.
  - `use_local` (boolean, optional): Whether to use the local AI service (default is false).
- **Response**:
  - 200: Explanation of the PDF file.
  - 400: Missing required fields or invalid file format.
  - 500: Internal server error.

## File Management

### GET /files/<module_name>/<topic_name>/<filename>
- **Description**: Open a specific file.
- **Response**:
  - 200: The requested file.
  - 404: File not found.
  - 500: Internal server error.

### GET /download_file/<module_name>/<topic_name>/<filename>
- **Description**: Download a specific file.
- **Response**:
  - 200: The requested file for download.
  - 404: File not found.
  - 500: Internal server error.

### POST /create_module
- **Description**: Create a new module.
- **Response**:
  - 200: Module created successfully.
  - 400: Missing required fields.
  - 500: Internal server error.

### POST /create_topic
- **Description**: Create a new topic.
- **Response**:
  - 200: Topic created successfully.
  - 400: Missing required fields.
  - 500: Internal server error.

### POST /upload_file
- **Description**: Upload a file to a specific module and topic.
- **Response**:
  - 200: File uploaded successfully.
  - 400: Missing required fields or invalid file format.
  - 500: Internal server error.

### GET /modules
- **Description**: List all modules.
- **Response**:
  - 200: List of all modules.
  - 500: Internal server error.

### GET /modules/<module_name>/topics
- **Description**: List all topics in a specific module.
- **Response**:
  - 200: List of all topics in the module.
  - 404: Module not found.
  - 500: Internal server error.

### GET /modules/<module_name>/topics/<topic_name>/files
- **Description**: List all files in a specific topic.
- **Response**:
  - 200: List of all files in the topic.
  - 404: Topic not found.
  - 500: Internal server error.

### DELETE /delete_module/<module_name>
- **Description**: Delete a specific module.
- **Response**:
  - 200: Module deleted successfully.
  - 404: Module not found.
  - 500: Internal server error.

### DELETE /delete_topic/<module_name>/<topic_name>
- **Description**: Delete a specific topic.
- **Response**:
  - 200: Topic deleted successfully.
  - 404: Topic not found.
  - 500: Internal server error.

### DELETE /files/<module_name>/<topic_name>/<filename>
- **Description**: Delete a specific file.
- **Response**:
  - 200: File deleted successfully.
  - 404: File not found.
  - 500: Internal server error.

## User Management

### POST /register
- **Description**: Register a new user.
- **Response**:
  - 200: User registered successfully.
  - 400: Missing required fields.
  - 500: Internal server error.

### POST /login
- **Description**: Login a user.
- **Response**:
  - 200: User logged in successfully.
  - 400: Missing required fields.
  - 500: Internal server error.

### GET /users
- **Description**: Get a list of all users.
- **Response**:
  - 200: List of all users.
  - 500: Internal server error.
