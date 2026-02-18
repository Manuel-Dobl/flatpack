def markdown_to_blocks(markdown):
    stripped_string = markdown.strip()
    split_string = stripped_string.split("\n\n")


    cleaned_blocks = []
    for s in  split_string:
        stripped_split = s.strip()
        if stripped_split != "":
            cleaned_blocks.append(stripped_split)
    return cleaned_blocks
