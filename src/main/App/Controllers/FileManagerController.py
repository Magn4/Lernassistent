from flask import request, jsonify
from Database.DatabaseContext import DatabaseContext

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
        file_content = file.read()
        try:
            self.db_context.upload_file(module_name, topic_name, file.filename, file_content)
            return jsonify({"message": f"File '{file.filename}' uploaded to topic '{topic_name}' in module '{module_name}'."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    
    def delete_module(self):
        data = request.get_json()
        module_name = data.get('module_name')
        try:
            self.db_context.delete_module(module_name)
            return jsonify({"message": f"Module '{module_name}' deleted successfully."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    def delete_topic(self):
        data = request.get_json()
        module_name = data.get('module_name')
        topic_name = data.get('topic_name')
        try:
            self.db_context.delete_topic(module_name, topic_name)
            return jsonify({"message": f"Topic '{topic_name}' deleted from module '{module_name}'."}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400