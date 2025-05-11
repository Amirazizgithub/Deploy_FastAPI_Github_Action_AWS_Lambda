from pathlib import Path

# Define the list of files to be created in the project
list_of_files = [
    "__init__.py",
    "config/__init__.py",
    "config/config.py",
    "model/__init__.py",
    "model/model.py",
    "routes/__init__.py",
    "routes/routes.py",
    "tests/__init__.py",
    "tests/test_app_routes.py",
    ".github/workflows/ci-cd-pipeline.yaml",
    "app.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
    ".env",
    ".dockerignore",
    "Dockerfile",
    "setup.py",
]

# Create the directories of the folder and write the files if they do not exist
for file in list_of_files:
    file_path = Path(file)
    if not file_path.exists():
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file, "w") as f:
            f.write("# Path: " + file)
print("Project structure created successfully!")
