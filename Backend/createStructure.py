import os

# Define the directory structure
directory_structure = {
    "app": {
        "__init__.py": "",
        "models.py": "",
        "auth": {
            "__init__.py": "",
            "routes.py": "",
        },
        "users": {
            "__init__.py": "",
            "routes.py": "",
        },
        "courses": {
            "__init__.py": "",
            "routes.py": "",
        },
        "instructors": {
            "__init__.py": "",
            "routes.py": "",
        },
        "ratings": {
            "__init__.py": "",
            "routes.py": "",
        },
        "comments": {
            "__init__.py": "",
            "routes.py": "",
        },
        "likes": {
            "__init__.py": "",
            "routes.py": "",
        },
        "follows": {
            "__init__.py": "",
            "routes.py": "",
        },
    },
    "migrations": {},
    "requirements.txt": "",
    "config.py": "",
    "run.py": "",
}

# Function to create directories and files
def create_structure(base_path, structure):
    for name, value in structure.items():
        if isinstance(value, dict):
            # Create the directory
            dir_path = os.path.join(base_path, name)
            os.makedirs(dir_path, exist_ok=True)
            # Recurse into the directory
            create_structure(dir_path, value)
        else:
            # Create the file
            file_path = os.path.join(base_path, name)
            with open(file_path, 'w') as file:
                file.write(value)

# Create the directory structure
base_path = './'  # Start at the current directory
create_structure(base_path, directory_structure)

print("Directory structure created successfully.")
