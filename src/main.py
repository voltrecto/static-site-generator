from textnode import TextNode, TextType
import os
import shutil
from utils import generate_page
import sys

basepath = sys.argv[1] if len(sys.argv) > 1 else '/'

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

def generate_all_markdown(source_dir, destination_dir, template_path, basepath):
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".md"):
                from_path = os.path.join(root, file)
                dest_path = from_path.replace(source_dir, destination_dir).replace(".md", ".html")

                dest_dir = os.path.dirname(dest_path)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                
                print(f"Generating HTML for: {from_path}")
                print(f"Output file: {dest_path}")
                generate_page(from_path=from_path, template_path=template_path, dest_path=dest_path, basepath=basepath)


def main():
    print("Starting static site generation...")
    destination_dir = "docs"
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)
    os.makedirs(destination_dir, exist_ok=True)
    copy_static("static", destination_dir)
    generate_all_markdown(source_dir="content", destination_dir=destination_dir, template_path="template.html", basepath=basepath)
    print("Static site generation complete.")

if __name__ == "__main__":
    main()