import os
import json
import re

def analyze_repo(root_dir='.'):
    """Scans the repository and extracts structural information."""
    structure = {
        'directories': [],
        'files': [],
        'languages': set(),
        'frameworks': set(),
        'env_vars': set()
    }

    ignore_dirs = {'.git', '.github', '__pycache__', 'node_modules', 'venv', 'env', 'docs'}

    # Simple regexes to detect frameworks/env vars from files
    framework_patterns = {
        'Django': r'django',
        'Flask': r'flask',
        'React': r'react',
        'Express': r'express',
        'FastAPI': r'fastapi'
    }

    env_pattern = re.compile(r'os\.environ\.get\([\'"]([A-Z0-9_]+)[\'"]\)|process\.env\.([A-Z0-9_]+)')

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter ignored directories
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir != '.':
            structure['directories'].append(rel_dir)

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_file = os.path.relpath(file_path, root_dir)
            structure['files'].append(rel_file)

            # Detect language
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.py']: structure['languages'].add('Python')
            elif ext in ['.js', '.jsx', '.ts', '.tsx']: structure['languages'].add('JavaScript/TypeScript')
            elif ext in ['.html']: structure['languages'].add('HTML')
            elif ext in ['.css']: structure['languages'].add('CSS')
            elif ext in ['.java']: structure['languages'].add('Java')
            elif ext in ['.go']: structure['languages'].add('Go')
            elif ext in ['.rs']: structure['languages'].add('Rust')

            # Detect frameworks and env vars
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for framework, pattern in framework_patterns.items():
                        if re.search(pattern, content, re.IGNORECASE):
                            structure['frameworks'].add(framework)

                    for match in env_pattern.findall(content):
                        # match is a tuple like ('VAR_NAME', '') or ('', 'VAR_NAME')
                        var_name = match[0] if match[0] else match[1]
                        if var_name:
                            structure['env_vars'].add(var_name)
            except Exception:
                pass # Skip binary files or unreadable files

    # Convert sets to lists for JSON serialization
    structure['languages'] = list(structure['languages'])
    structure['frameworks'] = list(structure['frameworks'])
    structure['env_vars'] = list(structure['env_vars'])

    with open('repo_structure.json', 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2)

if __name__ == '__main__':
    analyze_repo()
