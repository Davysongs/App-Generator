import os
import openai
import requests
import zipfile

# Ensure you have your API key for OpenAI or any other service you're using
openai.api_key = 'your_openai_api_key_here'

def get_user_input():
    return input("What do you want to build/generate? ")

def generate_file_structure(prompt):
    # Use OpenAI's GPT-3.5 to generate the file structure
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

def generate_files_from_structure(file_structure, initial_requirements):
    files = {}
    for file_path in file_structure:
        prompt = (
            f"Generate the content for {file_path} "
            f"based on the initial requirements: {initial_requirements}"
        )

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": initial_requirements},
                {"role": "user", "content": prompt}
            ]
        )
        files[file_path] = response['choices'][0]['message']['content']
    return files

def create_zip(files, zip_name='generated_app.zip'):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file_path, content in files.items():
            zipf.writestr(file_path, content)
    print(f"{zip_name} created successfully in the current directory.")

def main():
    user_prompt = get_user_input()

    print("Generating file structure...")
    file_structure = generate_file_structure(user_prompt).splitlines()

    print("Generating files from structure...")
    files = generate_files_from_structure(file_structure, user_prompt)

    print("Creating zip file...")
    create_zip(files)

if __name__ == "__main__":
    main()
