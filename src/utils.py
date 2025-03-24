import os
from pathlib import Path
from block_functions import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    raise Exception("No h1 header found.")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as md_file:
        markdown_content = md_file.read()
    with open(template_path, "r") as template_file:
        template_content = template_file.read()
    title = extract_title(markdown_content)
    try:
        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()
    except ValueError as e:
        print(f"Warning: Error converting markdown to HTML:{e}")
        html_content = f"<p>Error rendering content:{e}</p>"

    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as dest_file:
        dest_file.write(full_html)