# Code2flow Integration Usage

This document explains how to use the integrated `code2flow` tool within this repository to generate flowcharts from Python source code.

## Overview

The `code2flow` tool has been modified to:
- Support all Python inheritance types.
- Remove the terminal feature.
- Directly convert `.dot` files to `.png` images.

It is now available as a command-line interface script located at `code2flow/code2flow_cli.py`.

## Prerequisites

Before running `code2flow`, ensure you have the necessary dependencies installed. These were installed when the `code2flow` project was integrated. If you encounter any issues, you might need to manually install `graphviz` and the Python dependencies:

```bash
pkg install -y graphviz
pip install -r code2flow/requirements_dev.txt
```

## How to Run

To generate a flowchart:

1.  **Navigate to the `code2flow` directory within your project:**

    ```bash
    cd /data/data/com.termux/files/home/code_analyzer/code2flow/
    ```

2.  **Execute the `code2flow_cli.py` script:**

    Use the following command structure:

    ```bash
    ./code2flow_cli.py <source_files_or_directories> -o <output_filename.png> [options]
    ```

    -   `<source_files_or_directories>`: One or more paths to your Python source files or directories containing them.
    -   `-o <output_filename.png>`: The desired name for the output PNG image file.
    -   `[options]`: Optional arguments to control the flowchart generation.

    **Example:** To generate a flowchart for `analyzer.py` (located in the parent directory of `code2flow`) and save it as `analyzer_flowchart.png` in the current directory:

    ```bash
    ./code2flow_cli.py ../analyzer.py -o analyzer_flowchart.png --language py
    ```

    **Example with multiple source files:**

    ```bash
    ./code2flow_cli.py ../module1.py ../module2.py -o combined_flowchart.png --language py
    ```

    **Example with a directory:**

    ```bash
    ./code2flow_cli.py ../src/ -o project_flowchart.png --language py
    ```

### Available Options:

-   `--output, -o <path>`: Output image file path (default: `output.png`).
-   `--language <lang>`: Specify the language (e.g., `py` for Python). If omitted, it tries to detect from file extension.
-   `--hide-legend`: Omit the legend from the output.
-   `--no-grouping`: Don't group functions into namespaces in the final output.
-   `--no-trimming`: Show all functions/namespaces whether or not they connect to anything.
-   `--skip-parse-errors`: Skip files that the language parser fails on.
-   `--quiet, -q`: Suppress most logging.
-   `--verbose, -v`: Add more logging.

The generated PNG image will be saved in the directory from which you run the `code2flow_cli.py` script (e.g., `/data/data/com.termux/files/home/code_analyzer/code2flow/` in the examples above).
