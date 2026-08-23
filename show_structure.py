from pathlib import Path

# Project root = folder where this script is executed
ROOT = Path.cwd()

# Output file
OUTPUT_FILE = ROOT / "project_structure.txt"

# Folders to completely ignore
EXCLUDED_DIRS = {
    "venv",
    ".venv",
    "env",
    ".env",
    "__pycache__",
    ".git",
    ".github",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    "htmlcov",
}

# Files to ignore
EXCLUDED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    "project_structure.txt",
    "show_structure.py",
}

# Unnecessary file extensions
EXCLUDED_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".log",
    ".tmp",
    ".bak",
}


def should_ignore(path: Path):
    # Ignore directories
    if path.is_dir() and path.name in EXCLUDED_DIRS:
        return True

    # Ignore files
    if path.is_file():
        if path.name in EXCLUDED_FILES:
            return True

        if path.suffix.lower() in EXCLUDED_EXTENSIONS:
            return True

    return False


def build_tree(directory: Path, prefix=""):
    lines = []

    try:
        items = [
            item for item in directory.iterdir()
            if not should_ignore(item)
        ]
    except PermissionError:
        return lines

    # Folders first, files second
    items.sort(key=lambda x: (x.is_file(), x.name.lower()))

    for index, item in enumerate(items):
        is_last = index == len(items) - 1

        connector = "└── " if is_last else "├── "
        lines.append(prefix + connector + item.name)

        if item.is_dir():
            new_prefix = prefix + ("    " if is_last else "│   ")
            lines.extend(build_tree(item, new_prefix))

    return lines


# Generate structure
structure = [
    f"Project Structure: {ROOT.name}",
    "",
    ROOT.name + "/"
]

structure.extend(build_tree(ROOT))

# Write to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    file.write("\n".join(structure))

print(f"Project structure created successfully!")
print(f"Output file: {OUTPUT_FILE}")




# from pathlib import Path

# # Project root = folder where this script is executed
# ROOT = Path.cwd()

# # Folders to completely ignore
# EXCLUDED_DIRS = {
#     "venv",
#     ".venv",
#     "env",
#     ".env",
#     "__pycache__",
#     ".git",
#     ".github",
#     ".idea",
#     ".vscode",
#     "node_modules",
#     "dist",
#     "build",
#     ".pytest_cache",
#     ".mypy_cache",
#     ".ruff_cache",
#     ".tox",
#     "htmlcov",
# }

# # Files to ignore
# EXCLUDED_FILES = {
#     ".DS_Store",
#     "Thumbs.db",
#     "desktop.ini",
# }

# # File extensions that are generally not useful for project structure
# EXCLUDED_EXTENSIONS = {
#     ".pyc",
#     ".pyo",
#     ".log",
#     ".tmp",
#     ".bak",
# }

# # Files that are important even if they don't have a normal extension
# IMPORTANT_FILES = {
#     "Dockerfile",
#     "docker-compose.yml",
#     "docker-compose.yaml",
#     "Makefile",
#     "Procfile",
#     ".gitignore",
#     ".dockerignore",
#     ".env.example",
#     "requirements.txt",
#     "README.md",
#     "pyproject.toml",
#     "setup.py",
#     "setup.cfg",
# }


# def should_ignore(path: Path):
#     # Ignore directories
#     if path.is_dir() and path.name in EXCLUDED_DIRS:
#         return True

#     # Ignore files
#     if path.is_file():
#         if path.name in EXCLUDED_FILES:
#             return True

#         if path.suffix in EXCLUDED_EXTENSIONS:
#             return True

#     return False


# def print_tree(directory: Path, prefix=""):
#     try:
#         items = [
#             item for item in directory.iterdir()
#             if not should_ignore(item)
#         ]
#     except PermissionError:
#         return

#     # Sort: folders first, then files
#     items.sort(key=lambda x: (x.is_file(), x.name.lower()))

#     for index, item in enumerate(items):
#         is_last = index == len(items) - 1

#         connector = "└── " if is_last else "├── "

#         print(prefix + connector + item.name)

#         if item.is_dir():
#             new_prefix = prefix + ("    " if is_last else "│   ")
#             print_tree(item, new_prefix)


# if __name__ == "__main__":
#     print(f"\nProject Structure: {ROOT.name}\n")
#     print_tree(ROOT)