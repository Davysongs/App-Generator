import os
import sys
import zipfile
from openai import OpenAI
import json

# Set your OpenAI API key here
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_file_structure(app_type, requirements):
    prompt = f"Generate a file structure for a {app_type} application with the following requirements: {requirements}. Return the structure as a dictionary where keys are file paths and values are empty strings. The response should not be in form of a markdown object but a text(string) response with json type formatting"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code and content for software applications."},
            {"role": "user", "content": prompt}
        ]
    )
    
    file_structure = response.choices[0].message.content
    print(file_structure)
    return json.loads(file_structure)

def generate_file_content(filepath, app_type, requirements, file_structure):
    prompt = f"Create only the content for the file '{filepath}' in a {app_type} application with the following requirements: {requirements}. The full file structure is: {json.dumps(file_structure, indent=2)}. Return only the file content, without any additional text or explanation."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code and content for software applications."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def create_files_and_directories(base_path, structure, app_type, requirements, full_structure):
    for key, value in structure.items():
        full_path = os.path.join(base_path, key)
        if isinstance(value, dict):
            os.makedirs(full_path, exist_ok=True)
            create_files_and_directories(full_path, value, app_type, requirements, full_structure)
        else:
            if value == "":
                content = generate_file_content(key, app_type, requirements, full_structure)
                with open(full_path, "w") as f:
                    f.write(content)
            else:
                dir_path = os.path.dirname(full_path)
                os.makedirs(dir_path, exist_ok=True)
                content = generate_file_content(value, app_type, requirements, full_structure)
                with open(os.path.join(dir_path, value), "w") as f:
                    f.write(content)

def create_app(app_type, requirements):
    try:
        # Generate file structure
        file_structure = get_file_structure(app_type, requirements)
        
        # Create a temporary directory for the app
        app_dir = f"{app_type}_app"
        os.makedirs(app_dir, exist_ok=True)
        
        # Create files and directories based on the file structure
        create_files_and_directories(app_dir, file_structure, app_type, requirements, file_structure)
        
        # Create a ZIP archive
        zip_filename = f"{app_type}_app.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(app_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, app_dir)
                    zipf.write(file_path, arcname)
        
        # Clean up the temporary directory
        for root, dirs, files in os.walk(app_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(app_dir)
        
        print(f"Application generated and saved as {zip_filename}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <app_type> <requirements>")
        sys.exit(1)
    
    app_type = sys.argv[1]
    requirements = " ".join(sys.argv[2:])
    
    create_app(app_type, requirements)
