import logging
import os
import zipfile
from tqdm import tqdm
import anthropic
from dotenv import load_dotenv

# Security: Store API key in environment variable
load_dotenv()

# Security: Store API key in environment variable
anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError("Please set the ANTHROPIC_API_KEY environment variable")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the Anthropic client
client = anthropic.Anthropic(api_key=anthropic_api_key)

def get_user_input():
    """Prompts the user for application type and initial requirements.

    Returns:
        tuple: A tuple containing the application type and initial requirements.
    """
    application_type = input("What type of application do you want to build/generate? ").strip()
    initial_requirements = input("Enter any specific requirements or constraints (optional): ").strip()

    if not application_type:
        raise ValueError("Application type cannot be empty.")

    return application_type, initial_requirements

def generate_file_structure(application_type):
    """Generates the file structure for the application using Anthropic's Claude.

    Args:
        application_type (str): The type of application to generate the file structure for.

    Returns:
        list: A list of file paths within the application structure.
    """
    try:
        prompt = f"\n\nHuman: Please generate the file structure for a {application_type} application.\n\nAssistant:"
        response = client.completions.create(
            model="claude-3-opus-20240229",
            prompt=prompt,
            max_tokens_to_sample=150,
            temperature=0.7
        )
        return response['completion'].strip().split('\n')
    except Exception as e:
        logging.error(f"Error generating file structure: {e}")
        raise

def generate_files_from_structure(file_structure, initial_requirements, max_files=20):
    """Generates the content for each file in the structure using Anthropic's Claude.

    Args:
        file_structure (list): A list of file paths within the application structure.
        initial_requirements (str): The initial requirements provided by the user.
        max_files (int, optional): The maximum number of files to generate. Defaults to 20.

    Returns:
        dict: A dictionary containing file paths as keys and generated content as values.
    """
    files = {}
    for i, file_path in enumerate(tqdm(file_structure, desc="Generating files", unit="file")):
        if i >= max_files:
            logging.warning(f"Maximum file limit of {max_files} reached. Skipping remaining files.")
            break
        prompt = f"\n\nHuman: Please generate the content for {file_path} based on the initial requirements: {initial_requirements}\n\nAssistant:"
        try:
            response = client.completions.create(
                model="claude-3-opus-20240229",
                prompt=prompt,
                max_tokens_to_sample=500,
                temperature=0.7
            )
            files[file_path] = response['completion'].strip()
        except Exception as e:
            logging.error(f"Error generating content for {file_path}: {e}")
            files[file_path] = "Error generating content. Please try again."
    return files

def create_zip(files, zip_name='generated_app.zip'):
    """Creates a ZIP archive containing the generated application files.

    Args:
        files (dict): A dictionary containing file paths as keys and generated content as values.
        zip_name (str, optional): The name of the ZIP archive. Defaults to 'generated_app.zip'.
    """
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file_path, content in files.items():
                zipf.writestr(file_path, content)
        logging.info(f"{zip_name} created successfully in the current directory.")
    except Exception as e:
        logging.error(f"Error creating zip file: {e}")
        raise

def validate_application(files):
    """Validates the generated application files.

    Args:
        files (dict): A dictionary containing file paths as keys and generated content as values.

    Returns:
        bool: True if validation passes, False otherwise.
    """
    # Basic validation example: checking for the presence of a main file (e.g., main.py or index.html)
    main_files = ['main.py', 'index.html']
    for main_file in main_files:
        if any(main_file in file_path for file_path in files):
            logging.info(f"Validation passed: Found {main_file}")
            return True
    logging.warning("Validation failed: Main application file not found.")
    return False

def main():
    """Main function that drives the application generation process."""

    try:
        # Get user input
        application_type, initial_requirements = get_user_input()

        print("Generating file structure...")
        file_structure = generate_file_structure(application_type)

        print("Generating files from structure...")
        max_files = int(os.environ.get("MAX_FILES", 20))
        files = generate_files_from_structure(file_structure, initial_requirements, max_files=max_files)

        print("Creating zip file...")
        create_zip(files)

        # Optional validation
        if os.environ.get("VALIDATE_APPLICATION", "False").lower() in ("true", "1", "yes"):
            if validate_application(files):
                print("Application validation passed.")
            else:
                print("Application validation failed.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
