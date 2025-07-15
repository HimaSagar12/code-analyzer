# How to Use the Code Analyzer

This guide will walk you through setting up and running the Python code analyzer.

## Step 1: Add Your API Key

Before you can use the tool, you must provide your Groq API key.

1.  Open the `config.yaml` file.
2.  Replace the placeholder text `"YOUR_GROQ_API_KEY"` with your actual Groq API key.

## Step 2: Make the Script Executable

Ensure the main run script has the correct permissions to execute. Run this command from your terminal in the `code_analyzer` directory:

```bash
chmod +x run.sh
```

## Step 3: Run the Analysis

Now you are ready to analyze a Python project.

1.  Navigate into the `code_analyzer` directory.
2.  Execute the `run.sh` script, followed by the path to the Python directory you want to analyze.

    ```bash
    ./run.sh /path/to/your/python/project
    ```

    For example, to analyze the analyzer tool itself, you would run:

    ```bash
    ./run.sh .
    ```

## Step 4: View the Report

Once the script finishes, a new file named `CODE_FLOW_ANALYSIS.md` will be generated in the `code_analyzer` directory.

Open this file to see the detailed analysis of your project's code flow.
