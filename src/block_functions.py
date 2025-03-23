def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        if len(block) > 0:
            final_blocks.append(block.strip())
    return final_blocks

