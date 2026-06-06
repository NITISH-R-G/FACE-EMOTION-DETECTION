import os
import json
import re

def build_knowledge_graph(root_dir='.'):
    """Builds a basic knowledge graph of module dependencies."""
    graph = {
        'nodes': [],
        'edges': []
    }

    ignore_dirs = {'.git', '.github', '__pycache__', 'node_modules', 'venv', 'env', 'docs'}

    # Very basic Python import detection
    import_pattern = re.compile(r'^import\s+([a-zA-Z0-9_\.]+)|^from\s+([a-zA-Z0-9_\.]+)\s+import', re.MULTILINE)

    for dirpath, dirnames, filenames in os.walk(root_dir):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]

        for filename in filenames:
            if not filename.endswith('.py'):
                continue

            file_path = os.path.join(dirpath, filename)
            rel_file = os.path.relpath(file_path, root_dir)
            module_name = os.path.splitext(rel_file)[0].replace(os.sep, '.')

            if module_name not in [node['id'] for node in graph['nodes']]:
                 graph['nodes'].append({'id': module_name, 'type': 'module'})

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    for match in import_pattern.findall(content):
                        imported_module = match[0] if match[0] else match[1]

                        # Add node for dependency if it doesn't exist
                        if imported_module not in [node['id'] for node in graph['nodes']]:
                             graph['nodes'].append({'id': imported_module, 'type': 'dependency'})

                        # Add edge
                        edge = {'source': module_name, 'target': imported_module, 'relation': 'imports'}
                        if edge not in graph['edges']:
                            graph['edges'].append(edge)
            except Exception:
                pass

    with open('knowledge_graph.json', 'w', encoding='utf-8') as f:
        json.dump(graph, f, indent=2)

if __name__ == '__main__':
    build_knowledge_graph()
