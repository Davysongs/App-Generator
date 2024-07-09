import os
import sys
import zipfile
import openai
import json

# Set your OpenAI API key here
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_file_structure(app_type, requirements):
    prompt = f"Generate a file structure for a {app_type} application with the following requirements: {requirements}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code and content for software applications."},
            {"role": "user", "content": prompt}
        ]
    )
    
    file_structure = response.choices[0].message.content
    print("Raw file structure response:", file_structure)  # Debugging information
    
    try:
        return json.loads(file_structure)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode the file structure response from OpenAI - {e}") from e

def generate_file_content(filename, app_type, requirements, file_structure):
    prompt = f"Create content for a {filename} file in a {app_type} application with the following requirements: {requirements} and file structure: {file_structure}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates code and content for software applications."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def create_app(app_type, requirements):
    try:
        # Generate file structure
        file_structure = get_file_structure(app_type, requirements)
        
        if len(file_structure) > 20:
            raise ValueError("Generated file structure exceeds the maximum file limit of 20")
        
        # Create a temporary directory for the app
        app_dir = f"{app_type}_app"
        os.makedirs(app_dir, exist_ok=True)
        
        # Generate content for each file
        for filename, _ in file_structure.items():
            content = generate_file_content(filename, app_type, requirements, file_structure)
            with open(os.path.join(app_dir, filename), "w") as f:
                f.write(content)
        
        # Create a ZIP archive
        zip_filename = f"{app_type}_app.zip"
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for root, _, files in os.walk(app_dir):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
        
        # Clean up the temporary directory
        for filename in file_structure.keys():
            os.remove(os.path.join(app_dir, filename))
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
