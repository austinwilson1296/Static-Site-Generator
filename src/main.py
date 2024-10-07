from textnode import *
from htmlnode import *
from helper import *
import os 
import shutil

def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)

    # Loop through all items in the source directory
    for item in os.listdir(source):
        # Create full path for the source item
        source_path = os.path.join(source, item)
        # Create full path for the destination item
        dest_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            # If it's a file, what function would you use to copy it?
            copied_path = shutil.copy(source_path,dest_path)
            # Don't forget to log the path of each file you copy!
            print(copied_path)
        else:
            # If it's a directory, how could you handle it?
            copy_static(source_path,dest_path)
            # Hint: Think about recursion!

def extract_title(markdown):
    with open(markdown,'r') as f:
        content = f.read()
        split_content = content.split('\n')
        for lines in split_content:
            lines = lines.strip()
            if lines.startswith("#"):
                return lines.lstrip('#').strip()
        raise Exception("No title found.")
    
def generate_page(from_path,template_path,dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    
    with open(from_path,'r')as f:
        markdown_content = f.read()

    with open(template_path,'r') as t:
        t_content = t.read()

    file_nodes = markdown_to_html_node(markdown_content).to_html()
    f_title = extract_title(from_path)

    t_content = t_content.replace('{{ Title }}',f_title)
    t_content = t_content.replace('{{ Content }}',file_nodes)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(dest_path,'w') as d:
        d.write(t_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        print(f'source path {source_path}')
        
        
        if os.path.isfile(source_path):
            with open(source_path, 'r') as f:
                markdown_content = f.read()
            
            with open(template_path, 'r') as t:
                t_content = t.read()
                
            file_nodes = markdown_to_html_node(markdown_content).to_html()

            f_title = extract_title(source_path)
            
            t_content = t_content.replace('{{ Title }}', f_title)
            t_content = t_content.replace('{{ Content }}', file_nodes)
            
            relative_path = os.path.relpath(source_path, dir_path_content)
            relative_html_path = os.path.splitext(relative_path)[0] + '.html'
            destination_file = os.path.join(dest_dir_path, relative_html_path)
            print(f'Destination path {destination_file}')
            print(f'relative path {relative_path}')
            print(f'relative path html {relative_html_path}')

            # Ensure the destination directory exists
            os.makedirs(os.path.dirname(destination_file), exist_ok=True)
            
            with open(destination_file, 'w') as html_file:
                html_file.write(t_content)
        
        elif os.path.isdir(source_path):
            relative_subdir = os.path.relpath(source_path, dir_path_content)
            new_dest_dir = os.path.join(dest_dir_path, relative_subdir)
            
            generate_pages_recursive(source_path, template_path, new_dest_dir)

def main():
    if os.path.exists('./public'):
        shutil.rmtree('./public')
    copy_static('./static','./public')
    generate_pages_recursive('./content','./template.html','./public')


if __name__ == "__main__":
    main()
