from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text_split = old_node.text.split(delimiter)
        if len(text_split) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        for i in range(len(text_split)):
            if i % 2 == 0:
                new_nodes.append(TextNode(text_split[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(text_split[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)