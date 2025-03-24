import unittest
from utils import extract_title

class TestUtils(unittest.TestCase):
    def test_extract_title(self):
        assert extract_title("# Hello") == "Hello"
        assert extract_title("# Hello World") == "Hello World"
        assert extract_title("# Hello\nWorld") == "Hello"
        
        assert extract_title("#     Spacey Title    ") == "Spacey Title"
        
        try:
            extract_title("No header here")
            assert False, "Should have raised an exception"
        except Exception:
            assert True

if __name__ == "__main__":
    unittest.main()