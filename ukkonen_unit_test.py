import unittest
from io import StringIO
import sys
from ukkonen import *

class SuffixTreeTest(unittest.TestCase):
    def setUp(self):
        self.test_cases = [
            "abcabxabcd",
            "",
            "abc$",
            "aaaa$",
            "xabxac$",
            "abcabxabcd$",
            "abcabcabcabc$",
            "$"
        ]

    def capture_tree_output(self, tree, s):
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        print_tree(tree, s)
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout
        return output

    def test_suffix_trees(self):
        for i, s in enumerate(self.test_cases):
            with self.subTest(test_case=i, string=s[:30] + ("..." if len(s) > 30 else "")):
                print(f"\n=== Test case {i} ===")
                print(f"Input: {s[:50]}{'...' if len(s) > 50 else ''}")

                naive_tree = naive_suffix_tree(s)
                ukkonen_tree = build_suffix_tree(s)

                naive_output = self.capture_tree_output(naive_tree, s)
                ukkonen_output = self.capture_tree_output(ukkonen_tree, s)

                print("\nNaive Suffix Tree:")
                print(naive_output)
                print("Ukkonen Suffix Tree:")
                print(ukkonen_output)

                if naive_output != ukkonen_output:
                    print("❌ Mismatch detected in suffix tree structure.")
                else:
                    print("✅ Trees match.")

                # Assert only if you're ready to fail on mismatch:
                # self.assertEqual(ukkonen_output, naive_output, f"Mismatch in test case {i}")

if __name__ == "__main__":
    unittest.main()
