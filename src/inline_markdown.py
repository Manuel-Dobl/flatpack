import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)  # one type
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)  # another type
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)  # another type
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("not valid markdown text")

        # parts = ["This is ", "bold", " text"]
        split_nodes = []

        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                # This is regular text
                node = TextNode(parts[i], TextType.TEXT)
                split_nodes.append(node)
            else:
                # This is the delimited text (bold, code, etc.)
                node = TextNode(parts[i], text_type)
                split_nodes.append(node)

        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_image(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_images(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in parts:
            sections = remaining_text.split(f"![{alt}]({url})", 1)

            if sections[0] != "":
                node = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(node)

            node2 = TextNode(alt, TextType.IMAGE, url)
            new_nodes.append(node2)

            remaining_text = sections[1]
        if remaining_text != "":
            node3 = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(node3)

    return new_nodes


def split_nodes_link(old_nodes):

    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = extract_markdown_links(node.text)
        if not parts:
            new_nodes.append(node)
            continue

        remaining_text = node.text
        for alt, url in parts:
            sections = remaining_text.split(f"[{alt}]({url})", 1)

            if sections[0] != "":
                node = TextNode(sections[0], TextType.TEXT)
                new_nodes.append(node)

            node2 = TextNode(alt, TextType.LINK, url)
            new_nodes.append(node2)

            remaining_text = sections[1]
        if remaining_text != "":
            node3 = TextNode(remaining_text, TextType.TEXT)
            new_nodes.append(node3)

    return new_nodes
