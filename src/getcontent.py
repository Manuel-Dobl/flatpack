from markdown_to_html import markdown_to_html_node
import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    else:
        raise Exception("No Heading Detected")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # Read the markdown file at from_path and store the contents in a variable.
    with open(from_path, "r") as f:
        markdown_contents = f.read()

    with open(template_path, "r") as f:
        template_content = f.read()

    node = markdown_to_html_node(markdown_contents)
    html_string = node.to_html()

    title = extract_title(markdown_contents)

    template_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_string
    )

    # write content

    destination = os.path.dirname(dest_path)
    os.makedirs(destination, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    os.makedirs(dest_dir_path, exist_ok=True)
    entries = os.listdir(dir_path_content)
    for entry in entries:
        src_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(src_path):
            if entry.endswith(".md"):
                name_no_ext, _ = os.path.splitext(entry)
                dest_html = os.path.join(dest_dir_path, name_no_ext + ".html")
                generate_page(src_path, template_path, dest_html)
        else:
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_pages_recursive(src_path, template_path, dest_path)
