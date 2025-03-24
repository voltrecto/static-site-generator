from textnode import TextNode, TextType
import os
import shutil
from utils import generate_page

def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    print(f"Creating destination directory: {destination}")
    os.mkdir(destination)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} to {destination_path}")
            shutil.copy(source_path, destination_path)
        else:
            copy_static(source_path, destination_path)

def main():
    print("Starting static site generation...")
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.makedirs("public", exist_ok=True)
    copy_static("static", "public")
    generate_page(from_path="content/index.md", template_path="template.html", dest_path="public/index.html")
    print("Static site generation complete.")

if __name__ == "__main__":
    main()