import os

directories = [
    "app",
    "app/endpoints",
    "app/utils"
]

files = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/database.py",
    "app/models.py",
    "app/schemas.py",
    "app/crud.py",
    "app/endpoints/configuration.py",
    "app/utils/exceptions.py",
    ".env"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

for file in files:
    open(file, 'a').close()

print("Project structure created successfully.")
