from textnode import TextNode, TextType, markdown_to_html_node
import os 
import shutil 
import re
import sys

def main():

    if len(sys.argv) >1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    static = "static"
    docs = "docs"

    prepare_public(docs)
    copy_dir(static, docs)

    generate_pages_recursive("content", "template.html", "docs", basepath)

def prepare_public(public_path):
    if os.path.exists(public_path):
        shutil.rmtree(public_path)

    os.mkdir(public_path)

def copy_dir(source_dir, dest_dir):
 
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item) #this looks inside source folder for the item and gives a path - source 

        dest_path = os.path.join(dest_dir, item) #this looks inside the public folder and makes a destination 

        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        
        else:
            os.mkdir(dest_path)
            copy_dir(source_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():

        cleaned_line = line.strip()

        if cleaned_line.startswith("#") and not cleaned_line.startswith("##"):
            return cleaned_line[1:].strip()
        
    raise ValueError("No H1 heading found in the provided markdown.")

def generate_page(from_path, template_path, dest_path, basepath):
    
    print(f"Generating page: {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, "r") as f:
        from_content = f.read()
    
    with open(template_path, "r") as f:
        template_content = f.read()
    
    html_node = markdown_to_html_node(from_content)
    
    string = html_node.to_html()
    
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", string)

    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(template_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item) #this looks inside content folder for the item and gives a path - source 

        dest_path = os.path.join(dest_dir_path, item) #this looks inside the public folder and makes a destination 

        if os.path.isfile(source_path):
            
            if source_path.endswith(".md"):
                
                new_dest = dest_path.replace(".md", ".html")

                generate_page(source_path, template_path, new_dest, basepath)

            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            os.makedirs(dest_path, exist_ok=True)

            generate_pages_recursive(source_path, template_path, dest_path, basepath)
    

if __name__ == "__main__":
    main()