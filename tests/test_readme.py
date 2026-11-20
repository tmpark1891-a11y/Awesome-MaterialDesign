import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")

LOCAL_IMG_RE = re.compile(r'<img\s+[^>]*src="/?(demoRes/[^"]+)"', re.IGNORECASE)
MD_LINK_RE = re.compile(r"\]\(([^)]*)\)")


def read_readme():
    with open(README, encoding="utf-8") as f:
        return f.read()


def exists_with_exact_case(rel_path):
    current = ROOT
    for part in rel_path.split("/"):
        if part not in os.listdir(current):
            return False
        current = os.path.join(current, part)
    return os.path.isfile(current)


class ReadmeLocalImagesTest(unittest.TestCase):
    def setUp(self):
        self.refs = LOCAL_IMG_RE.findall(read_readme())

    def test_readme_references_local_screenshots(self):
        self.assertTrue(self.refs, "expected README to embed images from demoRes/")

    def test_every_local_screenshot_exists_with_exact_case(self):
        missing = sorted({r for r in self.refs if not exists_with_exact_case(r)})
        self.assertEqual(missing, [], "README references missing demoRes files")

    def test_local_screenshots_are_image_files(self):
        allowed = (".png", ".gif", ".jpg", ".jpeg", ".webp", ".svg")
        bad = sorted({r for r in self.refs if not r.lower().endswith(allowed)})
        self.assertEqual(bad, [])


class ReadmeLinksTest(unittest.TestCase):
    def test_links_are_absolute_urls_or_anchors(self):
        targets = MD_LINK_RE.findall(read_readme())
        bad = [t for t in targets if not t.strip().startswith(("http://", "https://", "#"))]
        self.assertEqual(bad, [], "found empty or relative Markdown links")


if __name__ == "__main__":
    unittest.main()
