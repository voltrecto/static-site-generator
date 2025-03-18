import unittest
from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

class TestDelimiter(unittest.TestCase):
    def test_simple(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), 
                    TextNode("code block", TextType.CODE), 
                    TextNode(" word", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_no_delim(self):
        node = TextNode("Plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("Plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_mixed(self):
        node = TextNode("Text with `code` and more text", TextType.TEXT)
        node2 = TextNode("I'm bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and more text", TextType.TEXT),
            TextNode("I'm bold", TextType.BOLD)
        ]
        self.assertEqual(new_nodes, expected)     

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)   

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)   


if __name__ == "__main__":
    unittest.main()