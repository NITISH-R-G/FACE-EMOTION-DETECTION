import json
import os
from jinja2 import Environment, FileSystemLoader

def generate_readme():
    """Generates the README.md file using a Jinja2 template and repository data."""

    try:
        with open('repo_structure.json', 'r', encoding='utf-8') as f:
            repo_data = json.load(f)
    except FileNotFoundError:
        repo_data = {'languages': [], 'frameworks': [], 'env_vars': [], 'directories': [], 'files': []}

    # Load diagram if exists
    dependency_graph = ""
    try:
        with open('docs/diagrams/dependency_graph.md', 'r', encoding='utf-8') as f:
            # Skip the first few lines of heading and just get the mermaid block
            lines = f.readlines()
            if len(lines) > 2:
                dependency_graph = "".join(lines[2:]) # Skip `# Dependency Graph\n\n`
    except FileNotFoundError:
        pass

    # Template data
    data = {
        'project_name': os.path.basename(os.getcwd()) or 'Repository',
        'languages': repo_data.get('languages', []),
        'frameworks': repo_data.get('frameworks', []),
        'env_vars': repo_data.get('env_vars', []),
        'directories': repo_data.get('directories', []),
        'dependency_graph': dependency_graph
    }

    # Set up Jinja2 environment
    try:
        env = Environment(loader=FileSystemLoader('docs/templates'))
        template = env.get_template('README.md.jinja')
        rendered_readme = template.render(data)
    except Exception as e:
        print(f"Template rendering failed: {e}")
        # Fallback basic template if jinja fails or template not found
        rendered_readme = f"# {data['project_name']}\n\n## Auto-generated README\n\nLanguages: {', '.join(data['languages'])}\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(rendered_readme)

if __name__ == '__main__':
    generate_readme()
