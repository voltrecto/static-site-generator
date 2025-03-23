import unittest
from block_functions import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestBlockFunctions(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test invalid heading (no space after #)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
    
    def test_code(self):
        # Test basic code block
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        
        # Test multiline code block
        self.assertEqual(block_to_block_type("```\nline 1\nline 2\n```"), BlockType.CODE)
    
    def test_quote(self):
        # Test single line quote
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
        
        # Test multiline quote
        self.assertEqual(block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)
    
    def test_unordered_list(self):
        # Test single item list
        self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        
        # Test multi-item list
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2\n- Item 3"), BlockType.UNORDERED_LIST)
    
    def test_ordered_list(self):
        # Test single item list
        self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)

        # Test multi-item list
        self.assertEqual(block_to_block_type("1. Item 1\n2. Item 2\n3. Item 3"), BlockType.ORDERED_LIST)


    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()