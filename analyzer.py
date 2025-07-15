

import os
import sys
import yaml
from groq import Groq

def get_api_key():
    """Reads the Groq API key from the config.yaml file."""
    try:
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            return config.get("groq_api_key")
    except FileNotFoundError:
        print("Error: config.yaml not found. Please create it with your Groq API key.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading config.yaml: {e}")
        sys.exit(1)

def analyze_code_with_groq(client, file_path, file_content):
    """
    Analyzes Python code using the Groq API.
    If the file is large, it splits the content into chunks.
    """
    # Set a character limit to avoid exceeding the model's context window.
    # 15,000 chars is a safe buffer for an 8192 token limit.
    CHAR_LIMIT = 15000
    
    if len(file_content) <= CHAR_LIMIT:
        # File is small enough to be processed in one go
        prompt = f"""
        Analyze the following Python code from the file '{file_path}':

        ```python
        {file_content}
        ```

        Provide a brief, one-paragraph summary of the file's purpose.
        Then, identify the following:
        - **Main Functions:** List the key functions and their primary roles.
        - **Classes:** List the classes and their responsibilities.
        - **Entry Point:** State whether this file appears to be a potential entry point (e.g., contains `if __name__ == "__main__":`).
        - **Dependencies:** What other files in the project does this file seem to depend on?
        """
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error analyzing {file_path} with Groq: {e}"
    else:
        # File is large, so we process it in chunks
        chunks = [file_content[i:i + CHAR_LIMIT] for i in range(0, len(file_content), CHAR_LIMIT)]
        full_analysis = f"**Note: This file was too large and has been analyzed in {len(chunks)} chunks.**\n\n"
        
        for i, chunk in enumerate(chunks):
            prompt = f"""
            The following is chunk {i+1} of {len(chunks)} for the file '{file_path}'.
            Please analyze this specific chunk of Python code. Focus only on the code provided in this chunk.

            ```python
            {chunk}
            ```

            Provide a brief summary of this chunk's purpose.
            Then, identify the following within this chunk:
            - **Main Functions:** List any functions defined or called.
            - **Classes:** List any classes defined.
            """
            try:
                chat_completion = client.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    model="llama3-8b-8192",
                )
                analysis_chunk = chat_completion.choices[0].message.content
                full_analysis += f"### Analysis of Chunk {i+1}/{len(chunks)}\n\n{analysis_chunk}\n\n"
            except Exception as e:
                full_analysis += f"### Analysis of Chunk {i+1}/{len(chunks)}\n\nError analyzing chunk: {e}\n\n"
        
        return full_analysis

def main():
    """Main function to orchestrate the code analysis."""
    if len(sys.argv) != 2:
        print("Usage: python analyzer.py <directory_path>")
        sys.exit(1)

    target_directory = sys.argv[1]
    if not os.path.isdir(target_directory):
        print(f"Error: Directory not found at '{target_directory}'")
        sys.exit(1)

    api_key = get_api_key()
    if not api_key or api_key == "YOUR_GROQ_API_KEY":
        print("Error: Groq API key not found or not set in config.yaml.")
        sys.exit(1)

    client = Groq(api_key=api_key)
    analysis_report = "# Code Flow Analysis Report\n\n"

    # Find all Python files
    python_files = []
    for root, _, files in os.walk(target_directory):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))

    # Analyze each file
    for file_path in python_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Get AI-based analysis (chunked or full)
            analysis = analyze_code_with_groq(client, file_path, content)
            analysis_report += f"## File: `{file_path}`\n\n{analysis}\n\n"

            # Perform direct analysis for entry points and dependencies,
            # as this is more reliable than AI context, especially for large files.
            entry_point_found = "Yes" if 'if __name__ == "__main__":' in content else "No"
            
            dependencies = []
            for line in content.splitlines():
                if line.strip().startswith("import ") or line.strip().startswith("from "):
                    dependencies.append(line.strip())
            
            analysis_report += "### Direct Code Analysis\n\n"
            analysis_report += f"- **Potential Entry Point:** {entry_point_found}\n"
            
            if dependencies:
                analysis_report += "- **Dependencies (Imports):**\n"
                for dep in dependencies:
                    analysis_report += f"  - `{dep}`\n"
            else:
                analysis_report += "- **Dependencies (Imports):** None found.\n"

            analysis_report += "\n---\n\n"

        except Exception as e:
            analysis_report += f"## File: `{file_path}`\n\nError reading file: {e}\n\n---\n\n"}

    # Write the report
    with open("CODE_FLOW_ANALYSIS.md", "w") as f:
        f.write(analysis_report)

    print("Analysis complete. Report generated at CODE_FLOW_ANALYSIS.md")

if __name__ == "__main__":
    main()

