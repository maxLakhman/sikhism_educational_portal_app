import os
import zipfile

EXCLUDE_DIRS = {'.venv', '__pycache__', '.git'}

def zip_project(zip_name='myproject.zip', base_dir='.'):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, base_dir)
                zipf.write(filepath, arcname)
    print(f"Zipped to {zip_name} excluding {EXCLUDE_DIRS}")

if __name__ == "__main__":
    zip_project()
