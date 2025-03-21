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

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_image_list = extract_markdown_images(old_node.text)
        if len(node_image_list) == 0:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        for alt_text, url in node_image_list:
            image_markdown = f"![{alt_text}]({url})"
            text_split = old_node_text.split(image_markdown, 1)
            if text_split[0]:
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))   
            if len(text_split) > 1:
                old_node_text = text_split[1]
            else:
                old_node_text = ""
        if old_node_text:
            new_nodes.append(TextNode(old_node_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        node_link_list = extract_markdown_links(old_node.text)
        if len(node_link_list) == 0:
            new_nodes.append(old_node)
            continue
        old_node_text = old_node.text
        for anchor_text, url in node_link_list:
            link_markdown = f"[{anchor_text}]({url})"
            text_split = old_node_text.split(link_markdown, 1)
            if text_split[0]:
                new_nodes.append(TextNode(text_split[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))   
            if len(text_split) > 1:
                old_node_text = text_split[1]
            else:
                old_node_text = ""
        if old_node_text:
            new_nodes.append(TextNode(old_node_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    node_list = [TextNode(text, TextType.TEXT)]
    split_bold = split_nodes_delimiter(node_list, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_image = split_nodes_image(split_code)
    return split_nodes_link(split_image)