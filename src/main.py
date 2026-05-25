from textnode import TextNode, TextType
import os 
import shutil 

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

static = "static"
public = "public"

def prepare_public(static, public):
    if os.path.exists(public):
        shutil.rmtree(public)

    os.mkdir(public)

def copy_dir(static, public):

    content = os.listdir(static)

    source = ""
    destination = ""
    
    
    for item in content:
        source = os.path.join(static, item) #this looks inside source folder for the item and gives a path - source 

        destination = os.path.join(public, item) #this looks inside the public folder and makes a destination 

        if os.path.isfile(source):
            shutil.copy(source, destination)
        else:
            os.mkdir(destination)
            copy_dir(source, destination)

main()
prepare_public(static, public)
copy_dir(static, public)