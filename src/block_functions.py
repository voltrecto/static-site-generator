from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    final_blocks = []
    for block in blocks:
        if len(block) > 0:
            final_blocks.append(block.strip())
    return final_blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if markdown.startswith("#"):
        for i in range(1, 7):
            if markdown.startswith("#" * i + " "):
                return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif len(lines) > 0:
        is_ordered = True
        for index, line in enumerate(lines):
            prefix = f"{index + 1}. "
            if not line.startswith(prefix):
                is_ordered = False
                break
        if is_ordered:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH