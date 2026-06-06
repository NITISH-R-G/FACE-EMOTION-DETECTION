import json
import os

def generate_diagrams():
    """Reads the knowledge graph and generates Mermaid diagrams."""

    # Ensure docs/diagrams dir exists
    os.makedirs('docs/diagrams', exist_ok=True)

    try:
        with open('knowledge_graph.json', 'r', encoding='utf-8') as f:
            graph = json.load(f)
    except FileNotFoundError:
        print("Knowledge graph not found. Run knowledge_graph.py first.")
        return

    # Generate Dependency Graph (Mermaid Flowchart)
    mermaid_code = ["graph TD;"]

    # Add nodes (optional, but good for styling or clickable links later)
    for node in graph['nodes']:
        safe_id = node['id'].replace('.', '_').replace('-', '_')
        label = node['id']
        mermaid_code.append(f"    {safe_id}[\"{label}\"];")
        # Example of adding a click event (requires the file to exist and be accessible via URL in context)
        # We can simulate deep linking
        if node['type'] == 'module':
            file_path = node['id'].replace('.', '/') + ".py"
            mermaid_code.append(f"    click {safe_id} \"{file_path}\" \"View source\";")

    # Add edges
    for edge in graph['edges']:
        source_id = edge['source'].replace('.', '_').replace('-', '_')
        target_id = edge['target'].replace('.', '_').replace('-', '_')
        mermaid_code.append(f"    {source_id} --> {target_id};")

    with open('docs/diagrams/dependency_graph.md', 'w', encoding='utf-8') as f:
        f.write("# Dependency Graph\n\n```mermaid\n")
        f.write("\n".join(mermaid_code))
        f.write("\n```\n")

if __name__ == '__main__':
    generate_diagrams()
