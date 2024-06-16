# Project Title: Multi-API Application Generator

## Overview

This project is an advanced application generator that leverages both the OpenAI API and Anthropic's Claude API to create various types of applications. The project takes user input specifying the type of application to generate and any specific requirements, generates a file structure, and populates the files with appropriate content. The generated files are then packaged into a ZIP archive.

## Features

- **User Input**: Prompts the user to specify the type of application and any additional requirements.
- **File Structure Generation**: Uses AI models to generate the file structure for the specified application.
- **File Content Generation**: Populates each file in the structure with content based on the specified requirements.
- **ZIP Packaging**: Packages the generated files into a ZIP archive.
- **Validation**: Optionally validates the generated application to ensure key files are present.

## APIs Used

### OpenAI API
The OpenAI API is used for generating both the file structure and the content of the files based on user input.

### Anthropic's Claude API
The Claude API by Anthropic is an alternative used for the same purposes as the OpenAI API, providing flexibility and additional model options.

## Working Principle

1. **User Input**: The script prompts the user to enter the type of application they want to generate and any specific requirements.
2. **API Selection**: Depending on the script or configuration, either the OpenAI API or the Claude API is used.
3. **File Structure Generation**: The selected API generates the file structure based on the user's input.
4. **File Content Generation**: The selected API generates the content for each file in the structure.
5. **Packaging**: The generated files are packaged into a ZIP archive.
6. **Validation** (Optional): The script validates the generated application to ensure key files (e.g., `main.py`, `index.html`) are present.

## Setup Instructions

### Prerequisites

- Python 3.10.1 or newer
- API keys for both OpenAI and Anthropic's Claude

### Environment Setup

1. **Clone the Repository**
   ```sh
   git clone https://github.com/davysongs/app-generator.git
   cd app-generator
   ```

2. **Create a Virtual Environment**
   ```sh
   python -m venv env
   ```

3. **Activate the Virtual Environment**
   - On macOS/Linux:
     ```sh
     source env/bin/activate
     ```
   - On Windows:
     ```sh
     .\env\Scripts\activate
     ```

4. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

1. **Set Environment Variables**
   - OpenAI API Key:
     ```sh
     export OPENAI_API_KEY='your-openai-api-key'
     ```
   - Anthropic API Key:
     ```sh
     export ANTHROPIC_API_KEY='your-anthropic-api-key'
     ```
   - On Windows:
     ```cmd
     setx OPENAI_API_KEY "your-openai-api-key"
     setx ANTHROPIC_API_KEY "your-anthropic-api-key"
     ```

2. **Optional Environment Variables**
   - Max Files:
     ```sh
     export MAX_FILES=20
     ```
   - Validate Application:
     ```sh
     export VALIDATE_APPLICATION=True
     ```
   - On Windows:
     ```cmd
     setx MAX_FILES 20
     setx VALIDATE_APPLICATION True
     ```

### Running the Script

1. **Run the OpenAI Script**
   ```sh
   python generate_with_openai.py
   ```

2. **Run the Claude Script**
   ```sh
   python generate_with_claude.py
   ```

## Example Usage

### Generating a Web Application

1. Run the script and follow the prompts:
   ```sh
   python generate_with_openai.py
   ```
   - Enter the type of application: `A retro snake game for web`
   - Enter any specific requirements or constraints: `it should be colorful`

2. The script will generate the file structure and content, package the files into a ZIP archive, and optionally validate the application.

## Directory Structure

```
project-root/
├── env/
├── generated_app.zip
├── generate_with_openai.py
├── generate_with_claude.py
├── README.md
└── requirements.txt
```

## Troubleshooting

- **API Errors**: Ensure that your API keys are correctly set as environment variables and that they have the necessary permissions.
- **File Generation Issues**: Check the logs for any errors during file generation and adjust the prompts or retry as necessary.
- **Environment Setup**: Ensure that your virtual environment is activated and dependencies are correctly installed.

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. We welcome contributions that improve functionality, fix bugs, or enhance documentation.

