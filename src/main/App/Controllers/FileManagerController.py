import os
from flask import request, jsonify, current_app, send_from_directory
from Database.DatabaseContext import DatabaseContext, Module, Topic, File


class FileManagerController:
    def __init__(self, db_context):
        self.db_context = db_context

    def create_module(self):
        data = request.get_json()
        module_name = data.get('module_name')
        try:
            self.db_context.create_module(module_name)
            return jsonify({"message": f"Module '{module_name}' created successfully."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def create_topic(self):
        data = request.get_json()
        module_name = data.get('module_name')
        topic_name = data.get('topic_name')
        try:
            self.db_context.create_topic(module_name, topic_name)
            return jsonify({"message": f"Topic '{topic_name}' created in module '{module_name}'."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def upload_file(self):
        data = request.form
        module_name = data.get('module_name')
        topic_name = data.get('topic_name')
        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "The file must be in PDF format"}), 400

        # Save the file to the server
        upload_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], module_name, topic_name)
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, file.filename)
        file.save(file_path)

        try:
            self.db_context.upload_file(module_name, topic_name, file.filename, file_path)
            return jsonify({"message": f"File '{file.filename}' uploaded to topic '{topic_name}' in module '{module_name}'."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def open_file(self, module_name, topic_name, file_name):
        try:
            file_path = self.db_context.get_file_path(module_name, topic_name, file_name)
            if not file_path:
                current_app.logger.error(f"File path not found in database for {module_name}/{topic_name}/{file_name}")
                return jsonify({"error": "File not found"}), 404

            # Log the file path
            current_app.logger.info(f"Opening file at path: {file_path}")

            if not os.path.exists(file_path):
                current_app.logger.error(f"File does not exist on the server at path: {file_path}")
                return jsonify({"error": "File does not exist on the server"}), 404

            return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), mimetype='application/pdf')
        except Exception as e:
            current_app.logger.error(f"Error opening file: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def list_modules(self):
        try:
            modules = self.db_context.list_modules()
            return jsonify(modules), 200
        except Exception as e:
            current_app.logger.error(f"Error listing modules: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def list_topics(self, module_name):
        try:
            topics = self.db_context.list_topics(module_name)
            return jsonify(topics), 200
        except Exception as e:
            current_app.logger.error(f"Error listing topics: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def list_files(self, module_name, topic_name):
        try:
            files = self.db_context.list_files(module_name, topic_name)
            return jsonify(files), 200
        except Exception as e:
            current_app.logger.error(f"Error listing files: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def delete_module(self, module_name):
        try:
            self.db_context.delete_module(module_name)
            return jsonify({"message": f"Module '{module_name}' deleted successfully."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete_topic(self, module_name, topic_name):
        try:
            self.db_context.delete_topic(module_name, topic_name)
            return jsonify({"message": f"Topic '{topic_name}' deleted from module '{module_name}'."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete_file(self, module_name, topic_name, file_name):
        try:
            file_path = self.db_context.get_file_path(module_name, topic_name, file_name)
            if not file_path:
                return jsonify({"error": "File not found"}), 404

            # Delete the file from the server
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"Deleted file at path: {file_path}")
            else:
                current_app.logger.error(f"File does not exist on the server at path: {file_path}")

            self.db_context.delete_file(module_name, topic_name, file_name)
            return jsonify({"message": f"File '{file_name}' deleted from topic '{topic_name}' in module '{module_name}'."}), 200
        except Exception as e:
            current_app.logger.error(f"Error deleting file: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    def download_file(self, module_name, topic_name, file_name):
        try:
            file_path = self.db_context.get_file_path(module_name, topic_name, file_name)
            if not file_path:
                current_app.logger.error(f"File path not found in database for {module_name}/{topic_name}/{file_name}")
                return jsonify({"error": "File not found"}), 404

            # Log the file path
            current_app.logger.info(f"Downloading file at path: {file_path}")

            if not os.path.exists(file_path):
                current_app.logger.error(f"File does not exist on the server at path: {file_path}")
                return jsonify({"error": "File does not exist on the server"}), 404

            return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path), as_attachment=True)
        except Exception as e:
            current_app.logger.error(f"Error downloading file: {str(e)}")
            return jsonify({"error": str(e)}), 500