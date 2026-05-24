from enum import Enum
from htmlnode import LeafNode
import re


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    

def text_node_to_html_node(text_node):
        
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url} )

    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text } )

    else:
        raise Exception("Invalid TextType")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []

    for nodes in old_nodes:

        if nodes.text_type != TextType.TEXT:
            new_nodes.append(nodes)
            continue

        parts = nodes.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise Exception("invalid markdown")

        for i in range(len(parts)):

            if parts[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:

        # Only process normal text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        images = extract_markdown_images(original_text)

        # If no images, keep original node
        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining_text = original_text

        for image_alt, image_link in images:

            image_markdown = f"![{image_alt}]({image_link})"

            sections = remaining_text.split(image_markdown, 1)

            # Text before image
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # Image node
            new_nodes.append(
                TextNode(image_alt, TextType.IMAGE, image_link)
            )

            # Continue processing the remaining text
            remaining_text = sections[1]

        # Remaining text after last image
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:

        # Only process normal text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        original_text = node.text
        links = extract_markdown_links(original_text)

        # If no images, keep original node
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining_text = original_text

        for link_alt, link_url in links:

            link_markdown = f"[{link_alt}]({link_url})"

            sections = remaining_text.split(link_markdown, 1)

            # Text before image
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            # LINK node
            new_nodes.append(
                TextNode(link_alt, TextType.LINK, link_url))

            # Continue processing the remaining text
            remaining_text = sections[1]

        # Remaining text after last image
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    nodes = split_nodes_image(nodes)
    
    nodes = split_nodes_link(nodes)

    return nodes