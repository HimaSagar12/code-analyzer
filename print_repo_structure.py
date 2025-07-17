import os
import argparse

def get_directory_structure(root_dir, exclude_dirs=None, exclude_files=None):
    if exclude_dirs is None:
        exclude_dirs = ['.git', '__pycache__', 'node_modules', '.venv', '.vscode', '.idea', 'build', 'dist']
    if exclude_files is None:
        exclude_files = ['.DS_Store', 'Thumbs.db', 'npm-debug.log', 'yarn-error.log']

    structure_str = ""
    file_contents = ""

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]

        level = dirpath.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        structure_str += f'{indent}{os.path.basename(dirpath)}/
'

        for f in filenames:
            if f in exclude_files:
                continue
            
            file_path = os.path.join(dirpath, f)
            structure_str += f'{indent}    {f}
'
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                file_contents += f"\n--- Contents of {file_path.replace(root_dir, '')} ---\n"
                file_contents += content
                file_contents += "\n--- End of {file_path.replace(root_dir, '')} ---\n\n"
            except Exception as e:
                file_contents += f"\n--- Could not read {file_path.replace(root_dir, '')}: {e} ---\n\n"
    
    return structure_str, file_contents

def main():
    parser = argparse.ArgumentParser(description="Print directory structure and file contents for LLM input.")
    parser.add_argument('path', nargs='?', default='.', 
                        help='The root directory to scan (default: current directory).')
    args = parser.parse_args()

    root_dir = os.path.abspath(args.path)
    
    structure, contents = get_directory_structure(root_dir)

    print("Repository Structure:")
    print(structure)
    print("\nFile Contents:")
    print(contents)

if __name__ == "__main__":
    main()
