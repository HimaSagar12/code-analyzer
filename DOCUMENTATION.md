# Code Analyzer Documentation

## 1. Project Overview

This project is a Python-based tool that analyzes a given directory of Python code and generates a code flow analysis report. It uses the Groq API with the Llama 3 model to understand and summarize the functionality of each Python file.

The primary goal is to provide a clear, high-level understanding of a codebase, identifying potential entry points, key functions, and the overall architecture without manually reading every line of code.

## 2. File Structure

Here is a breakdown of each file in the project:

- **`run.sh`**: The main entry point for the user. This shell script handles dependency installation and executes the Python analyzer. It simplifies the process of running the tool.

- **`analyzer.py`**: The core logic of the application. This script is responsible for reading the target directory, finding all Python files, calling the Groq API for analysis, and generating the final Markdown report.

- **`config.yaml`**: A configuration file to store the Groq API key. This separates the secret key from the source code, which is a security best practice.

- **`requirements.txt`**: Lists the necessary Python packages (`groq`, `pyyaml`) required for the project to run.

- **`.gitignore`**: Prevents sensitive files (like `config.yaml`) and generated reports from being accidentally committed to version control.

- **`CODE_FLOW_ANALYSIS.md`**: The final output file. This report contains the AI-generated analysis of the target codebase.

## 3. Core Functions in `analyzer.py`

The Python script is built around a few key functions:

- **`main()`**: This is the orchestrator. It parses command-line arguments to get the target directory, ensures the API key is configured, walks through the directory to find all `.py` files, and calls the analysis function for each one before writing the final report.

- **`get_api_key()`**: A simple and safe utility function to read the `config.yaml` file and extract the Groq API key. It includes error handling for cases where the file is missing or the key is not set.

- **`analyze_code_with_groq(client, file_path, file_content)`**: This function constructs the prompt that is sent to the Groq API. It takes the code content of a file and asks the AI to provide a summary, identify key functions and classes, and determine if the file is a likely entry point.

## 4. Code Flow Chart

This chart illustrates the execution flow from start to finish:

```mermaid
graph TD
    A[Start: User executes ./run.sh <target_dir>] --> B{Check for target_dir};
    B --> C[Install Dependencies via pip];
    C --> D[Execute python analyzer.py <target_dir>];
    D --> E{main() function starts};
    E --> F[get_api_key() from config.yaml];
    F --> G[Walk target_dir to find all .py files];
    G --> H{Loop through each .py file};
    H --> I[Read file content];
    I --> J[Call analyze_code_with_groq()];
    J --> K[Send prompt to Groq API];
    K --> L[Receive AI analysis];
    L --> M[Append analysis to report string];
    M --> H; % Loop back to the next file
    H -- After all files --> N[Write final report to CODE_FLOW_ANALYSIS.md];
    N --> O[End];
```

## 5. How to Use

1.  **Configure API Key**: Open `config.yaml` and replace `YOUR_GROQ_API_KEY` with your actual Groq API key.

2.  **Make Script Executable**: Ensure `run.sh` is executable by running `chmod +x run.sh`.

3.  **Run Analysis**: From within the `code_analyzer` directory, execute the script and point it to a Python project:

    ```bash
    ./run.sh /path/to/your/python/project
    ```

4.  **View Report**: Once the script finishes, open `CODE_FLOW_ANALYSIS.md` to view the detailed analysis.
